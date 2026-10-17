"""Rebuild this one self-owned, non-virtualized benchmark from its memory dump.

This is a case-specific reconstruction, NOT a generic VMProtect unpacker.
Input code/data comes only from the Scylla dump. The reference EXE is not read.
OEP was supplied by the benchmark's known build metadata. Import call sites
were identified by disassembly/arguments and corroborated with API tracing.
"""
import argparse
import ctypes
import hashlib
import json
from pathlib import Path
import struct
import lief
import pefile

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--scylla-dll', required=True, type=Path)
args = parser.parse_args()
DUMP = ROOT / 'unpacked' / 'reu-challenge.dump.exe'
STAGE = ROOT / 'unpacked' / 'reu-challenge.imports.exe'
OUTPUT = ROOT / 'unpacked' / 'reu-challenge.unpacked.exe'
if STAGE.exists() or OUTPUT.exists():
    raise SystemExit('Refusing to overwrite reconstruction artifacts')

# Each region is one six-byte import call replaced by the protector.
# Addresses are RVAs in this exact benchmark, not signatures for other files.
sites = {
    0x1074: ('KERNEL32.dll', 'GetStdHandle'),
    0x1091: ('KERNEL32.dll', 'WriteFile'),
    0x1120: ('KERNEL32.dll', 'GetStdHandle'),
    0x113D: ('KERNEL32.dll', 'WriteFile'),
    0x11F8: ('KERNEL32.dll', 'GetCommandLineA'),
    0x1399: ('USER32.dll', 'MessageBoxW'),
    0x13A7: ('KERNEL32.dll', 'ExitProcess'),
    0x1434: ('KERNEL32.dll', 'ExitProcess'),
    0x1440: ('KERNEL32.dll', 'ExitProcess'),
}
binary = lief.PE.parse(DUMP)
if binary is None:
    raise SystemExit('Cannot parse Scylla dump')
removed = [section.name for section in binary.sections if section.virtual_address >= 0x4000]
for name in removed:
    binary.remove_section(name, clear=True)
binary.remove_all_imports()
for directory in binary.data_directories:
    if directory.type != lief.PE.DataDirectory.TYPES.EXCEPTION_TABLE:
        directory.rva = directory.size = 0
binary.optional_header.imagebase = 0x140000000
binary.optional_header.addressof_entrypoint = 0x11F0
binary.optional_header.sizeof_image = 0x4000
binary.optional_header.checksum = 0
for section in binary.sections:
    # remove_section may expand its predecessor across the deleted RVA range.
    # This benchmark's three retained sections each occupy one 4 KiB page.
    section.virtual_size = 0x1000
    section.characteristics = 0x60000020 if section.name == '.text' else 0x40000040
for library in sorted({library for library, name in sites.values()}):
    imported = binary.add_import(library)
    for name in sorted({name for dll, name in sites.values() if dll == library}):
        imported.add_entry(name)

config = lief.PE.Builder.config_t()
config.imports = True
for name in ('debug', 'exports', 'resources', 'relocations', 'tls', 'load_configuration', 'overlay'):
    setattr(config, name, False)
binary.write(STAGE, config)

rebuilt = pefile.PE(str(STAGE))
iat = {(lib.dll.decode(), entry.name.decode()): entry.address - rebuilt.OPTIONAL_HEADER.ImageBase
       for lib in rebuilt.DIRECTORY_ENTRY_IMPORT for entry in lib.imports}
patches = []
for rva, imported in sorted(sites.items()):
    before = rebuilt.get_data(rva, 6)
    if not (before[0] == 0xE8 or (0x50 <= before[0] <= 0x57 and before[1] == 0xE8)):
        raise SystemExit(f'Unexpected protected call form at {rva:#x}: {before.hex()}')
    after = b'\xff\x15' + struct.pack('<i', iat[imported] - (rva + 6))
    rebuilt.set_bytes_at_rva(rva, after)
    patches.append({'rva': hex(rva), 'api': '!'.join(imported), 'before': before.hex(), 'after': after.hex(),
                    'evidence': 'API trace and/or manual argument/call-site analysis; behavior checked separately'})
rebuilt.OPTIONAL_HEADER.CheckSum = rebuilt.generate_checksum()
rebuilt.write(str(OUTPUT))
scylla = ctypes.WinDLL(str(args.scylla_dll.resolve(strict=True)))
scylla.ScyllaRebuildFileW.argtypes = [ctypes.c_wchar_p, ctypes.c_int, ctypes.c_int, ctypes.c_int]
scylla.ScyllaRebuildFileW.restype = ctypes.c_int
if not scylla.ScyllaRebuildFileW(str(OUTPUT), False, True, False):
    raise SystemExit('Scylla PE layout normalization failed')
# LIEF rebuilds the import descriptors but leaves directory 12 empty for a new
# IAT. Publish its actual contiguous range as well as the descriptor directory.
compacted = pefile.PE(str(OUTPUT))
iat_addresses = [entry.address - compacted.OPTIONAL_HEADER.ImageBase
                 for library in compacted.DIRECTORY_ENTRY_IMPORT for entry in library.imports]
compacted.OPTIONAL_HEADER.DATA_DIRECTORY[12].VirtualAddress = min(iat_addresses)
compacted.OPTIONAL_HEADER.DATA_DIRECTORY[12].Size = max(iat_addresses) + 16 - min(iat_addresses)
compacted.OPTIONAL_HEADER.CheckSum = compacted.generate_checksum()
compacted.write(str(OUTPUT))
report = {
    'scope': 'Case-specific loader and import reconstruction; no selected virtualized functions',
    'input': str(DUMP), 'input_sha256': hashlib.sha256(DUMP.read_bytes()).hexdigest(),
    'output': str(OUTPUT), 'output_sha256': hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
    'original_executable_read': False, 'known_oep_rva': '0x11f0',
    'removed_sections': removed, 'import_call_patches': patches,
    'tools': {'lief': lief.__version__, 'pefile': pefile.__version__, 'layout_normalizer': 'ScyllaRebuildFileW'},
    'validation': 'Pending external behavior and structural checks',
}
(ROOT / 'evidence' / 'reconstruction.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'output':str(OUTPUT),'bytes':OUTPUT.stat().st_size,'patched_calls':len(patches)}))
