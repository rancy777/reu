# VMProtect 3.8.4 x64: one virtualized pure function

This case uses `VMProtectBeginVirtualization("ReuChallengeTransform")` and `VMProtectEnd()` around a seven-round uint32 transform. VMProtect recognized the marker as **Virtualization**, and the original arithmetic body was replaced by a VM entry sequence.

The working recovery reads **the protected PE and its real x64dbg trace**. It does not read the C++ algorithm or original EXE. Triton replays 21,849 instructions, preserves the symbolic `ECX` input and emits LLVM IR. LLVM 22.1 compiles that IR to 53 straight-line x64 instructions with no calls or imports. The DLL is 2,048 bytes. The 4,608-byte EXE is a separately source-built CLI harness, linked to the recovered object; it is not a reconstructed copy of the whole protected EXE.

[Illustrated case report](../../docs/cases/vmprotect-3.8.4-virtualized-x64.md) · [Acceptance data](evidence/acceptance.json) · [Artifact identities](evidence/case-record.json)

## Rebuild the native demo without VMProtect

Requires **Windows x64, Python 3.11 x64 on PATH, Visual Studio C++ x64 build tools and a Windows SDK**. From the downloaded project's root:

```powershell
powershell -NoProfile -File .\examples\vmprotect-3.8.4-virtualized-x64\source\rebuild_demo.ps1
```

The script creates `runtime-artifacts/vmp-native-demo`, installs only `llvmlite==0.50.0` in its own environment, compiles the published IR, links a native DLL and CLI harness, and runs 45 behavior checks on an EXE copied alone under another name. It does not read `challenge.cpp` during compilation. The independent behavior oracle uses the reference algorithm only for validation.

The output contains `recovered/native/reu-recovered.dll`, `recovered/native/reu-recovered.exe`, `evidence/demo-build.json` and `evidence/demo-behavior.json`. To inspect the functional dialog afterwards, run `runtime-artifacts/vmp-native-demo/recovered/native/reu-recovered.exe --show`.

An existing output directory is refused. Choose a new directory with `-OutputDirectory D:\Experiments\reu-native-demo-2` if needed. Compiler versions can affect binary hashes; the receipt records actual hashes. This is compilation and behavioral validation of the recorded recovery result, **not fresh devirtualization, exhaustive proof, or a new 128-input comparison against the protected program**.

The [recorded fresh demo run](evidence/native-demo-check.json) passed 45/45 checks from a directory containing spaces. Both binaries matched the accepted recovery hashes, and attempting to reuse that directory was rejected without modifying its accepted outputs.

## Working directory for a full experiment

Copy the complete example into a new ignored directory before using the remaining commands, so build products and new evidence do not overwrite published source records. From the project root:

```powershell
if (Test-Path .\runtime-artifacts\vmp-function-reproduction) { throw 'Choose a fresh working directory' }
New-Item -ItemType Directory .\runtime-artifacts -Force | Out-Null
Copy-Item -LiteralPath .\examples\vmprotect-3.8.4-virtualized-x64 -Destination .\runtime-artifacts\vmp-function-reproduction -Recurse
Set-Location .\runtime-artifacts\vmp-function-reproduction
python -m venv .venv
.venv\Scripts\python -m pip install -r source\requirements.txt
```

All following commands run in that copied case directory. The source distribution excludes the recorded protected executable and SDK. A fresh protected build needs a fresh trace and reviewed addresses; the supplied trace only matches the exact artifact hash in the case record.

To compile the published IR manually:

```powershell
New-Item -ItemType Directory recovered\native -Force
.venv\Scripts\python source\compile_recovered.py recovered\recovered.ll recovered\native
.\source\link_recovered.ps1
```

`compile_recovered.py` compiles only the recorded IR. `recovered_harness.cpp` contains CLI handling, fixed test vectors and a call to the recovered function; it contains no implementation of the protected transform.

## Build and protect a new sample

Provide your own licensed VMProtect installation and matching SDK. Proprietary SDK headers, import libraries and DLLs are local dependencies and are excluded from this source package. Replace the example path below with the directory containing your SDK header, `VMProtectSDK64.lib` and `VMProtectSDK64.dll`.

```powershell
.\source\build.ps1 -SdkDirectory C:\Tools\VMProtect\SDK
```

Load the resulting original EXE in VMProtect. Confirm that the marker is listed as **Virtualization**. The recorded project uses `Options=0` to isolate function virtualization and keeps VM complexity at 20%. It disables packing, memory/import/resource protection and debugger/VM detection. It does not reproduce the earlier default-packing case.

The original unprotected EXE requires `VMProtectSDK64.dll` next to it. The protected and recovered EXEs do not. Each VMP compilation generates a different protected artifact; do not mix a trace from one build with another build.

## Record and replay the protected function

The successful run used x64dbg release **2026.05.27**, through `headless.exe`, because the graphical frontend had a Qt plugin conflict. After initialization and system/entry breakpoints completed, it stopped at export RVA `0x1150` for `--value 42`. The caller return RVA was `0x142F`. Remove software breakpoints before recording instruction bytes.

Trace text fields, separated by `|`:

```text
{cip}|{mem;16@cip}|{rax}|{rbx}|{rcx}|{rdx}|{rsi}|{rdi}|{rbp}|{rsp}|{r8}|{r9}|{r10}|{r11}|{r12}|{r13}|{r14}|{r15}|{eflags}|{mem;16@rsp}
```

Use `TraceSetLog`, `TraceSetLogFile` and `ticnd "cip==mod.main()+142F",.200000` only after the function-entry stop is confirmed. The recorded native trace has 21,850 rows, including the caller-return state; 21,849 instructions are replayed. The original capture also had two unsupported memory-format fields; they were removed without modifying the retained fields. [Normalization receipt](evidence/trace-normalization.json).

For the exact recorded protected EXE (SHA-256 in `case-record.json`), supplied in the local experiment bundle:

```powershell
.venv\Scripts\python source\replay_native.py evidence\native-function.trace.txt recovered\replayed --binary protected\reu-challenge.virtualized.exe --stop 7ff70a07142f
```

The replay has case-specific Windows x64 ABI, export RVA and return-state assumptions. It synchronizes concrete register/stack state from the native trace, rejects symbolic-state disagreements and rejects control-flow mismatches. It is not a generic VMP handler lifter. No symbolic path constraints were recorded for this pure function; that is not a general path-coverage proof.

## Accept or reject the result

```powershell
.venv\Scripts\python source\verify_recovery.py --dll recovered\native\reu-recovered.dll --exe recovered\native\reu-recovered.exe --protected protected\reu-challenge.virtualized.exe --out evidence\fresh-acceptance.json
```

The verifier runs 100,008 deterministic native input checks, 128 comparisons against the protected EXE, PE/control-flow checks, and 45 CLI checks after copying the EXE alone to a temporary directory. It prints the Chinese success verdict only after those checks pass. Altering one byte of the recovered XOR immediate was correctly rejected under `python -O`.

A full-domain Z3 equivalence attempt returned **unknown after 120 seconds**. The result is sampled verification, not exhaustive proof over every uint32 value. Input-dependent branches, memory side effects, Ultra mode, other VM versions, arbitrary executables and real MCP-provider compatibility remain unvalidated.
