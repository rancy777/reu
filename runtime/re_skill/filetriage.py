"""Bounded, strictly read-only file-type triage. Never executes or extracts a target.

This is structural identification, not a malware verdict or packer classifier.
All high-entropy and section-name signals are *observations*, not conclusions.
"""
from __future__ import annotations

import hashlib
import math
import struct
import zipfile
from pathlib import Path
from typing import Any

MACHINES = {0x14c: 'x86', 0x8664: 'x64', 0x1c0: 'ARM', 0x1c4: 'ARMv7', 0xaa64: 'ARM64'}
ELF_MACHINES = {3: 'x86', 62: 'x64', 40: 'ARM', 183: 'ARM64', 8: 'MIPS'}
MAX_ENTRIES = 100_000
MAX_UNCOMPRESSED = 2 * 1024 ** 3


def _u16(buf: bytes, off: int) -> int:
    if off < 0 or off + 2 > len(buf):
        raise ValueError(f'truncated u16 at {off}')
    return struct.unpack_from('<H', buf, off)[0]


def _u32(buf: bytes, off: int) -> int:
    if off < 0 or off + 4 > len(buf):
        raise ValueError(f'truncated u32 at {off}')
    return struct.unpack_from('<I', buf, off)[0]


def _entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = [0] * 256
    for b in data:
        counts[b] += 1
    n = len(data)
    return round(-sum((c/n) * math.log2(c/n) for c in counts if c), 3)


def _pe(path: Path, head: bytes, size: int) -> dict[str, Any]:
    res: dict[str, Any] = {'format': 'pe', 'platform': 'windows', 'indicators': [], 'warnings': []}
    if len(head) < 64:
        res['warnings'].append('truncated DOS header')
        return res
    off = _u32(head, 0x3c)
    if off > 16 * 1024 * 1024 or off + 24 > size:
        res['warnings'].append('invalid/truncated e_lfanew')
        return res
    with path.open('rb') as f:
        f.seek(off)
        sig_header = f.read(24)
        if sig_header[:4] != b'PE\x00\x00':
            res['warnings'].append('MZ present, but PE signature absent')
            return res
        machine, nsec, _, _, _, opt_size, _ = struct.unpack_from('<HHIIIHH', sig_header, 4)
        res['architecture'] = MACHINES.get(machine, f'unknown-0x{machine:04x}')
        res['section_count'] = nsec
        if nsec > 256:
            res['warnings'].append('implausible section count')
            return res
        opt = f.read(opt_size)
        if len(opt) != opt_size or len(opt) < 2:
            res['warnings'].append('truncated optional header')
            return res
        magic = _u16(opt, 0)
        res['pe_kind'] = {0x10b: 'PE32', 0x20b: 'PE32+'}.get(magic, 'Unknown')
        if magic not in (0x10b, 0x20b):
            res['warnings'].append('nonstandard optional header magic')
            return res
        if len(opt) >= 20:
            res['entrypoint_rva'] = f'0x{_u32(opt, 16):08x}'
        dirs_start = 96 if magic == 0x10b else 112
        dirs_count_off = 92 if magic == 0x10b else 108
        if len(opt) >= dirs_count_off + 4:
            count = _u32(opt, dirs_count_off)
            res['data_directory_count'] = count
            if count > 14 and dirs_start + 15*8 <= len(opt):
                clr_rva, clr_size = struct.unpack_from('<II', opt, dirs_start + 14*8)
                res['clr'] = bool(clr_rva and clr_size)
                res['dotnet'] = res['clr']
            elif count > 14:
                res['warnings'].append('declared CLR directory is truncated')
        res['sections'] = []
        for idx in range(nsec):
            raw = f.read(40)
            if len(raw) < 40:
                res['warnings'].append('truncated section table')
                break
            name = raw[:8].split(b'\x00', 1)[0].decode('ascii', 'replace')
            vsz, va, rawsz, rawptr = struct.unpack_from('<IIII', raw, 8)
            characteristics = struct.unpack_from('<I', raw, 36)[0]
            item: dict[str, Any] = {
                'name': name, 'rva': f'0x{va:x}', 'virtual_size': vsz,
                'raw_offset': rawptr, 'raw_size': rawsz,
                'readable': bool(characteristics & 0x40000000),
                'writable': bool(characteristics & 0x80000000),
                'executable': bool(characteristics & 0x20000000),
            }
            if rawsz > 0 and rawptr <= size and rawsz <= size - rawptr:
                pos = f.tell()
                f.seek(rawptr)
                # Heuristic only; sampling avoids loading arbitrary huge sections.
                item['entropy_sample'] = _entropy(f.read(min(rawsz, 256 * 1024)))
                f.seek(pos)
                if item['entropy_sample'] > 7.4 and rawsz >= 4096:
                    res['indicators'].append({'kind': 'high-entropy-section', 'section': name, 'certainty': 'heuristic'})
            elif rawsz:
                res['warnings'].append(f'section {name!r} has out-of-bounds raw data')
            if item['writable'] and item['executable']:
                res['indicators'].append({'kind': 'rwx-section', 'section': name, 'certainty': 'structural'})
            res['sections'].append(item)
    return res


def _zip(path: Path) -> dict[str, Any]:
    res: dict[str, Any] = {'format': 'zip', 'platform': 'unknown', 'indicators': [], 'warnings': []}
    try:
        with zipfile.ZipFile(path) as z:
            infos = z.infolist()
            if len(infos) > MAX_ENTRIES:
                return {**res, 'warnings': ['archive entry count exceeds safety cap'], 'entry_count': len(infos)}
            total = sum(i.file_size for i in infos)
            res['entry_count'] = len(infos)
            res['total_uncompressed_bytes'] = total
            if total > MAX_UNCOMPRESSED:
                res['warnings'].append('archive advertised uncompressed size exceeds safety cap')
            if any(i.file_size > 1_000_000 and i.compress_size and i.file_size / i.compress_size > 1000 for i in infos):
                res['warnings'].append('extreme compression ratio; do not extract without isolation')
            names = [i.filename for i in infos]
            s = set(names)
            dex = sorted(n for n in names if n.endswith('.dex'))[:500]
            so = sorted(n for n in names if n.endswith('.so'))[:500]
            if 'AndroidManifest.xml' in s:
                res.update(format='apk', platform='android')
            elif 'base/manifest/AndroidManifest.xml' in s or any(n.endswith('/manifest/AndroidManifest.xml') for n in names):
                res.update(format='aab', platform='android')
            elif 'toc.pb' in s and any(n.endswith('.apk') for n in names):
                res.update(format='apks', platform='android')
            res['dex_files'] = dex
            res['native_libraries'] = so
            res['package_samples'] = names[:20]
            if res['format'] == 'apk' and not dex:
                res['indicators'].append({'kind': 'no-dex-in-container', 'certainty': 'structural', 'note': 'may be resource-only, native-only, split, or dynamically loaded; not proof of a packer'})
    except (zipfile.BadZipFile, EOFError, OSError) as e:
        res['warnings'].append(f'ZIP metadata parse error: {type(e).__name__}')
    return res


def inspect_file(path: str | Path, max_size: int = 512 * 1024**2) -> dict[str, Any]:
    target = Path(path)
    if not target.is_file() or target.is_symlink():
        raise ValueError('target must be an existing regular non-symlink file')
    size = target.stat().st_size
    if size > max_size:
        raise ValueError(f'target size {size} exceeds read-only analysis cap {max_size}')
    digest = hashlib.sha256()
    with target.open('rb') as f:
        head = f.read(4096)
        digest.update(head)
        while chunk := f.read(1024 * 1024):
            digest.update(chunk)
    base: dict[str, Any] = {
        'filename': target.name, 'size': size, 'sha256': digest.hexdigest(),
        'format': 'unknown', 'architecture': 'Unknown', 'indicators': [],
        'warnings': [], 'executable_was_run': False,
    }
    if head.startswith(b'MZ'):
        base.update(_pe(target, head, size))
    elif head.startswith(b'\x7fELF') and len(head) >= 20:
        endian = '<' if head[5] == 1 else '>' if head[5] == 2 else None
        if endian:
            machine = struct.unpack_from(endian + 'H', head, 18)[0]
            base.update(format='elf', platform='native', architecture=ELF_MACHINES.get(machine, f'unknown-{machine}'),
                        elf_class={1:'ELF32',2:'ELF64'}.get(head[4], 'Unknown'),
                        elf_type=struct.unpack_from(endian + 'H', head, 16)[0])
        else:
            base['warnings'].append('invalid ELF endian flag')
    elif head.startswith(b'dex\n') and len(head) >= 8:
        base.update(format='dex', platform='android', dex_version=head[4:7].decode('ascii', 'replace'))
    elif head.startswith(b'cdex'):
        base.update(format='cdex', platform='android')
    elif head.startswith(b'vdex'):
        base.update(format='vdex', platform='android')
    elif head.startswith(b'PK\x03\x04') or zipfile.is_zipfile(target):
        base.update(_zip(target))
    return base
