# Toolchain and MCP Selection

The Skill selects **capabilities**, then binds them to a native tool and optionally an MCP provider.

| Task | Preferred backend | MCP examples | CLI fallback |
|---|---|---|---|
| PE triage | DIE / pefile / LIEF | APKiD for Android; DIE MCP; Reversecore/REMnux | `diec`, Python |
| PE static | IDA / Ghidra / BN / r2 | Hex-Rays IDA MCP; Ghidra MCP; Binary Ninja MCP; r2 MCP | native CLI/scripts |
| Windows debugging | x64dbg / WinDbg | x64dbg MCP; windbg-mcp | manual GUI |
| PE memory | debugger / PE-sieve | x64dbg/WinDbg MCP | native debugger |
| Import reconstruction | Scylla / PE tooling | Scylla-style MCP only when runtime assumptions match | Scylla + scripts |
| .NET decompilation | IDA / ILSpy | IDA MCP; ILSpy MCP | ILSpyCmd |
| Android packer ID | APKiD | `apkid-mcp` | `apkid-ai-cli` |
| Android Java/Kotlin | JADX | JADX-AI-MCP | JADX CLI |
| Android package/resources | Apktool | Apktool MCP | apktool CLI |
| Android runtime | Frida | typed Frida MCP | frida CLI/scripts |
| Android native | IDA / Ghidra / r2 | corresponding MCPs | CLI/headless |
| Native emulation | Unidbg / angr | Unidbg MCP; angr MCP | project APIs |
| Malware toolkit | REMnux | REMnux MCP | native REMnux commands |
| YARA/capa/FLOSS | native tools | aggregator MCP when useful | direct CLI |

## Rules

1. Do not install an MCP because it exists; install it because its capability contract is useful.
2. Prefer direct upstream providers over aggregators for high-confidence evidence.
3. Aggregators are useful for breadth, but wrapped-engine outputs retain the underlying engine's provenance.
4. For a disputed conclusion, change **modality**, not just provider wrapper.
5. Record native tool version separately from MCP version.
6. Preserve raw output and hashes where policy permits.
