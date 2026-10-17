# MCP Source Registry

This registry records upstream repositories used by the Skill's MCP integration layer.

| Provider | Upstream | Role | Status |
|---|---|---|---|
| IDA | HexRaysSA/ida-mcp | official IDA MCP | recommended |
| x64dbg | ouonet/x64dbg-mcp | debugger MCP | recommended after health check |
| WinDbg | glslang/windbg-mcp | DbgEng/WinDbg MCP | candidate/recommended after health |
| Ghidra | LaurieWired/GhidraMCP | Ghidra MCP | candidate |
| Ghidra headless | SumTuusDeus/ghidra-mcp | PyGhidra MCP | experimental/candidate |
| Binary Ninja | unichk/binaryninja-mcp | Binary Ninja MCP | candidate |
| radare2 | radareorg/radare2-mcp | first-party r2 MCP | recommended |
| Frida | majimboo/rexd-frida-mcp | typed Frida runtime MCP | candidate |
| Frida mobile | cbxss/frida-mcp | mobile Frida MCP | candidate |
| Unidbg | zhkl0228/unidbg | project MCP debugger | recommended when emulation fits |
| JADX | zinja-coder/jadx-ai-mcp + jadx-mcp-server | JADX plugin + server | recommended |
| Apktool | zinja-coder/apktool-mcp-server | Apktool MCP | recommended after version gate |
| APKiD | android-security-engineer/APKiDSkills | Android packer/protector triage | recommended |
| MobSF | plur1bu5/mobsf-mcp | Android SAST/DAST/Frida aggregator | optional |
| REMnux | REMnux/remnux-mcp-server | isolated malware toolkit | optional-recommended |
| Reversecore | ondrong/reversecore_mcp | broad binary/security aggregator | optional |
| revula | president-xd/revula | broad reverse engineering aggregator | optional |
| angr | sandbornm/angr_mcp | symbolic execution | experimental |
| DIE | lazy-importer/D.I.E-MCP | DIE wrapper | optional |
| Scylla-rs | NekoRem/scylla-rs | experimental PE reconstruction MCP | experimental |

## Verification

The repository URLs above are external dependencies. Before a production deployment, re-open the upstream repository/release/security page and update:
- current release
- commit
- requirements
- security advisories
- transport/auth behavior

Do not treat this registry as proof that an upstream implementation remains current.

## MCP protocol/runtime baseline

- Official MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk
- Current v2 release observed during the 2026-10-16 research pass: v2.3.0.
- The runtime targets the v2 line (`mcp>=2.3,<3`) and records the actual installed SDK version at deployment time.
