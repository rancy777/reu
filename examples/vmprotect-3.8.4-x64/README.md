# VMProtect 3.8.4 x64 benchmark sources

This directory contains the sources for the [documented single-sample experiment](../../docs/cases/vmprotect-3.8.4-x64.md). It is a benchmark-assisted, case-specific loader/import reconstruction, not a general VMProtect unpacker or devirtualizer.

The C++ program performs a deterministic 32-bit computation, checks eight known vectors, prints arbitrary-input results, and has explicit failure paths. It does not access the network or user files. `--show` displays a functional self-test dialog. A passing dialog alone does not establish unpacking.

## Build your own reference

Copy the example into an ignored working directory before running the build:

```powershell
New-Item -ItemType Directory .\runtime-artifacts -Force | Out-Null
if (Test-Path .\runtime-artifacts\vmp-reproduction) { throw 'Choose a new working directory' }
Copy-Item -LiteralPath .\examples\vmprotect-3.8.4-x64 -Destination .\runtime-artifacts\vmp-reproduction -Recurse
& .\runtime-artifacts\vmp-reproduction\source\build.ps1
python .\runtime-artifacts\vmp-reproduction\source\validate_behavior.py .\runtime-artifacts\vmp-reproduction\original\reu-challenge.exe --output .\runtime-artifacts\vmp-reproduction\evidence\original-behavior.json
```

The build requires Visual Studio C++ x64 tools and a Windows SDK. The recorded experiment used MSVC **19.44.35215**, SDK **10.0.22621.0**, `/O2 /GS- /GR- /Brepro`, no CRT, and ASLR/NX linker flags. The original hash is recorded in the case report. Other toolchains can produce different code layouts.

The build refuses to overwrite an existing reference EXE. Keep the original, protected sample, VMP project, dumps, and candidates in separate subdirectories.

## Protect and investigate

Use your separately installed VMProtect 3.8.4 to create a protected copy. In this case, compression, memory protection, import protection and resource protection were enabled; debugger/VM detection were off; **no protected functions were selected**. Save the actual project and preserve its hash. VMProtect-generated code can differ between builds.

Follow the case report to distinguish the packed entry point, the known original entry point, a runtime dump, and a runnable reconstruction. x64dbg and Scylla are external tools and are not distributed here. The official x64dbg GUI encountered a Qt plugin conflict on the recorded host; analysis used its bundled `headless.exe` and Scylla's official DLL API instead.

`scylla_dump.py` requires a paused benchmark PID, its actual module base, and an observed OEP. It records ordinary and advanced IAT search failures as failures. Its `--gui` option opens the real Scylla interface for inspection.

`rebuild_case.py` reads only the runtime dump. It uses this benchmark's known OEP (`0x11f0`), three retained section ranges, and **nine manually identified import-call sites**. Four API/call-site relationships were directly corroborated by the normal self-test trace; the remaining paths were identified from disassembly/arguments and checked by numeric, failure-path and GUI execution. It does not rediscover these sites in arbitrary programs. Inspect and re-establish all assumptions for another build; successful execution is not a substitute for this review.

Install the analysis libraries in an isolated environment, then run the case-specific reconstruction only after placing a reviewed dump at `unpacked/reu-challenge.dump.exe`:

```powershell
python -m venv .\runtime-artifacts\vmp-reproduction\.venv
& .\runtime-artifacts\vmp-reproduction\.venv\Scripts\python.exe -m pip install -r .\runtime-artifacts\vmp-reproduction\source\requirements.txt
& .\runtime-artifacts\vmp-reproduction\.venv\Scripts\python.exe .\runtime-artifacts\vmp-reproduction\source\rebuild_case.py --scylla-dll C:\Tools\x64dbg\release\x64\Scylla.dll
& .\runtime-artifacts\vmp-reproduction\.venv\Scripts\python.exe .\runtime-artifacts\vmp-reproduction\source\validate_structure.py
& .\runtime-artifacts\vmp-reproduction\.venv\Scripts\python.exe .\runtime-artifacts\vmp-reproduction\source\verify_case.py
```

The reconstruction refuses to overwrite candidates. `validate_structure.py` verifies the precise recorded layout, retained bytes, nine call repairs, new imports, checksum and absence of references to removed protector sections. `verify_case.py` runs fresh structural checks, copies the final EXE alone into an empty directory under another name, runs all behavior checks, and verifies that every report identifies the same unchanged artifact. It prints `脱壳验证成功` only when those checks pass; otherwise it prints failure and exits nonzero. The behavior oracle tests 40 numeric inputs, the eight-vector self-test, an explicit failure path, and three invalid-input cases: **45 checks total**.

No original EXE, protected EXE, memory dump, proprietary SDK or analysis-tool binary is included in the source distribution. Full local artifacts remain under `runtime-artifacts/`; only the selected, sanitized result records and genuine screenshots accompany the report.
