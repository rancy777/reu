"""Call the official Scylla DLL against this benchmark's paused process.

API reference: x64dbg/Scylla, vs13, Scylla/FunctionExport.cpp.
No code or sections are copied from the unprotected reference executable.
"""
import argparse
import ctypes as c
from ctypes import wintypes as w
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--dll', type=Path, required=True)
parser.add_argument('--pid', type=int, required=True)
parser.add_argument('--base', type=lambda x: int(x, 0), required=True)
parser.add_argument('--oep', type=lambda x: int(x, 0), required=True)
parser.add_argument('--output-dir', type=Path, required=True)
parser.add_argument('--gui', action='store_true')
args = parser.parse_args()
dll = c.WinDLL(str(args.dll.resolve(strict=True)))
size_t = c.c_size_t
dll.ScyllaVersionInformationW.restype = w.LPCWSTR
report = {'pid': args.pid, 'base': hex(args.base), 'oep': hex(args.oep),
          'scylla_version': dll.ScyllaVersionInformationW(), 'attempts': []}
if args.gui:
    dll.ScyllaStartGui.argtypes = [w.DWORD, c.c_void_p, size_t]
    dll.ScyllaStartGui.restype = c.c_int
    raise SystemExit(dll.ScyllaStartGui(args.pid, args.base, args.oep))

output_dir = args.output_dir.resolve(strict=True)
dump_path = output_dir / 'reu-challenge.dump.exe'
if dump_path.exists():
    raise SystemExit('Dump exists; refusing to overwrite')
dll.ScyllaDumpProcessW.argtypes = [size_t, w.LPCWSTR, size_t, size_t, w.LPCWSTR]
dll.ScyllaDumpProcessW.restype = w.BOOL
report['dump_ok'] = bool(dll.ScyllaDumpProcessW(args.pid, None, args.base, args.oep, str(dump_path)))
if report['dump_ok']:
    dll.ScyllaIatSearch.argtypes = [w.DWORD, c.POINTER(size_t), c.POINTER(w.DWORD), size_t, w.BOOL]
    dll.ScyllaIatSearch.restype = c.c_int
    dll.ScyllaIatFixAutoW.argtypes = [size_t, w.DWORD, w.DWORD, w.LPCWSTR, w.LPCWSTR]
    dll.ScyllaIatFixAutoW.restype = c.c_int
    for advanced in (False, True):
        start, size = size_t(), w.DWORD()
        code = dll.ScyllaIatSearch(args.pid, c.byref(start), c.byref(size), args.oep, advanced)
        attempt = {'advanced': advanced, 'search_code': code, 'iat': hex(start.value), 'iat_size': size.value}
        if code == 0 and start.value and size.value:
            fixed = output_dir / ('reu-challenge.advanced.exe' if advanced else 'reu-challenge.fixed.exe')
            if fixed.exists():
                raise SystemExit('Fixed candidate exists; refusing to overwrite')
            attempt['fix_code'] = dll.ScyllaIatFixAutoW(start.value, size.value, args.pid, str(dump_path), str(fixed))
            attempt['candidate'] = str(fixed)
        report['attempts'].append(attempt)
(output_dir.parent / 'evidence' / 'scylla-dump.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report))
raise SystemExit(not report['dump_ok'])
