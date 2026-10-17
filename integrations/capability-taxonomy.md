# Capability Taxonomy

The agent selects capabilities, not product names.

| Capability ID | Purpose | Typical providers/tools |
|---|---|---|
| `artifact.fs` | constrained file read/write/list/hash | Filesystem MCP |
| `artifact.exec` | execute installed CLI tools | Shell/command MCP |
| `research.web` | web search/open/source retrieval | web/search capability |
| `pe.triage` | PE format/arch/header/section/import triage | DIE, PE-bear, PEStudio, pefile, LIEF |
| `pe.static` | disassembly/decompilation/xrefs/types | IDA, Ghidra, Binary Ninja, radare2 |
| `pe.runtime` | Windows user-mode runtime observation | x64dbg, WinDbg |
| `pe.memory` | process memory/module/region observation | x64dbg, WinDbg, PE-sieve, Frida |
| `pe.reconstruct` | dump/import/reconstruction evidence | Scylla, PE-sieve, manual PE tooling |
| `dotnet.metadata` | CLR/metadata/IL analysis | IDA, Ghidra, .NET tooling |
| `dotnet.runtime` | JIT/R2R/NativeAOT/runtime behavior | debugger, profiler, runtime tools |
| `android.package` | APK/AAB/split/package inventory | adb, bundletool, apktool |
| `android.dex` | DEX/smali/decompilation | JADX, apktool, baksmali |
| `android.runtime` | ART/ClassLoader/runtime observation | Frida, LLDB, adb |
| `android.native` | ELF/SO/JNI/native analysis | IDA, Ghidra, Binary Ninja, radare2 |
| `android.device` | device/emulator/process/log/package control | adb/mobile MCP |
| `android.instrumentation` | runtime hooks/memory/modules | Frida MCP |
| `native.elf` | ELF headers/segments/relocations/symbols | Ghidra, IDA, radare2, readelf |
| `decompiler` | source-like representation | IDA, Ghidra, Binary Ninja, JADX |
| `emulation` | controlled CPU/native execution | Unidbg, Unicorn |
| `strings` | static/decoded/stack/tight strings | FLOSS, native strings |
| `capability-detection` | behavior/capability hypotheses | capa |
| `rule-scanning` | signature/rule matching | YARA, APKiD, DIE |
| `session.observe` | normalize session metadata | all interactive providers |
| `session.validate` | validate target/output identity | all providers |
| `evidence.raw` | preserve raw output/artifact references | filesystem/provider resources |

## Capability matching algorithm

1. Exact semantic match.
2. Tool description/schema confirms operation.
3. Health check succeeds.
4. Target/application version is compatible or explicitly unknown.
5. Provider security posture is acceptable.
6. Prefer read-only provider if it can answer the question.
7. Use a second independent provider when the claim is high-impact or disputed.

## Provider fallback

Example:

`pe.static`

- Primary: IDA MCP
- Fallback 1: Ghidra MCP
- Fallback 2: Binary Ninja MCP
- Fallback 3: radare2 MCP
- Fallback 4: native CLI/static tooling via shell

Do not switch silently when results disagree. Record the provider transition as an evidence-graph event.
