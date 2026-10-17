# Research Snapshot — v1.1.1

Historical research notes, retained for provenance. Version and upstream status claims describe the original snapshot and must be rechecked before selecting or installing a provider. This file is not a compatibility test report.

## Executive conclusion

The project should be treated as a **reverse-engineering research agent with an external tool plane and a persistent evidence/corpus plane**.

The most important architecture is now:

`Target → Triage → MCP discovery → capability binding → hypotheses → evidence → experiment → validation → failure diagnosis → corpus update → knowledge promotion`

This avoids the common failure mode of building a large procedural unpacking manual that cannot adapt to tool/version/runtime changes.

## Major 2026 research update: MCP ecosystem

A significant change since the earlier baseline is the emergence of mature MCP integrations around reverse-engineering tools.

### IDA

Hex-Rays now publishes an official IDA MCP server. Its current repository states that it requires IDA 9.4+ with idalib and Python 3.11+, supports stdio/HTTP operation, and is built around IDA Nexus. The repository's latest observed release is `20261008.0.1`. This replaces older third-party IDA MCP projects as the preferred provider.

### x64dbg

Multiple active community x64dbg MCP implementations now exist. The `ouonet/x64dbg-mcp` project exposes debugger, memory, analysis and triage functionality and can auto-detect x32dbg/x64dbg. Other implementations expose larger tool surfaces. The skill therefore treats x64dbg MCP as a **capability class with provider competition**, not a fixed server.

### WinDbg

WinDbg has an MCP feature surface in current builds, and Microsoft public material discusses MCP settings/state. Public documentation is still less uniform than the IDA MCP documentation, while independent DbgEng-based MCP servers provide explicit tool contracts. Therefore the skill records WinDbg MCP as a live-discovery provider and maintains a standalone DbgEng MCP fallback.

### Ghidra

Ghidra remains an official NSA project, with current releases reaching 12.1.4 in the research snapshot. MCP implementations are community-maintained and differ substantially in tool surface and Ghidra-version support. Provider and Ghidra version pinning is therefore mandatory for reproducible cases.

### Binary Ninja

Community MCP integrations now expose Binary Ninja analysis and automation, including decompilation, IL/CFG and database interaction. Because these are not the vendor's sole canonical integration surface, the skill requires health checks and version pinning.

### radare2

The radareorg project maintains `radare2-mcp`. The current observed release was 1.8.8. It supports readonly mode, sandbox lock, fine-grained configuration, and stdio/HTTP operation. It is therefore a strong first-party-project provider for CLI/scriptable binary analysis.

### Frida

Frida's release cadence is fast. The official release index currently shows 17.23.x releases, with 17.23.3 appearing as the latest listed release during the research snapshot. The skill therefore records both Frida and MCP provider versions in runtime cases.

### Android MCP

Community MCP providers now exist for JADX, Apktool, Frida and device control. The important design consequence is that Android analysis can be assembled as a **package/decompiler/runtime/native capability graph** rather than a single "Android MCP".

### Unidbg

Unidbg's own documentation now describes MCP support for debugger and repeatable custom-tool workflows. The skill treats it as controlled native emulation, not as a full Android runtime substitute.

### Filesystem

The official MCP reference filesystem server provides constrained filesystem operations and access controls. It is suitable as a substrate for analysis workspaces when roots are restricted.

## Persistent research assets

v1.1.1 introduces four durable assets:

### Protector Case Corpus
Sample-scoped evidence, tool versions, failure modes, and validation.

### Runtime Compatibility Matrix
Observed relationships among OS/ABI/runtime/tool/MCP/provider/protector versions.

### Evidence Graph
Explicit provenance between source, claim, hypothesis, experiment, observation, artifact, case and conclusion.

### Regression Corpus
Machine-readable cases that protect routing, evidence discipline, provider fallback and safety from regressions.

## Why the corpus matters

The skill should not learn by rewriting prose.

It should learn by accumulating structured observations:

`case → evidence → graph → compatibility → regression → promotion`

This permits:
- nearest-case retrieval;
- version-aware route selection;
- contradiction detection;
- failure-class clustering;
- provider selection based on empirical compatibility;
- regression testing after tool upgrades.

## Current gaps

1. Real protector corpus remains the largest missing asset. It must be populated from actual authorized samples and reproducible public cases.
2. Commercial Android protector coverage remains fragmented and version-sensitive.
3. MCP provider stability varies widely; tool schemas may change faster than native tools.
4. Public documentation for some built-in debugger MCP features lags implementation.
5. Cross-runtime compatibility needs real lab measurements, not assumptions.
6. The evidence graph will become substantially more valuable once hundreds of real observations exist.

## Outdated-risk areas

- treating OEP as the universal objective;
- assuming a memory dump is automatically a valid PE;
- assuming one import reconstruction tool is authoritative;
- Dalvik-centric Android workflows;
- treating DEX on disk as the only code representation;
- treating a packer signature as proof;
- assuming a community MCP tool surface is stable;
- assuming "MCP connected" means the native tool is healthy.

## Conflicts to preserve

### MCP provider competition
Several projects expose the same native tool through MCP. They may differ in:
- tool naming;
- schemas;
- write capabilities;
- transport;
- lifecycle;
- version compatibility;
- security posture.

Do not collapse these into one canonical provider.

### Filesystem MCP version metadata
The public source tree and registry may expose different package-version metadata at different times. The skill therefore records resolved installation version instead of hard-coding one global package version.

### Community protector techniques
Community reports may conflict by protector version, sample configuration, architecture, debugger version or runtime. Store them as scoped cases until corroborated.

## Proposed architecture

```text
                    RESEARCH AGENT
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
       Reasoning      MCP Tool Plane   Web Research
          │              │              │
          │       ┌──────┴──────┐       │
          │       ↓             ↓       │
          │    Static        Runtime   │
          │       │             │       │
          └───────┼─────────────┼───────┘
                  ↓
            Evidence Layer
                  │
        ┌─────────┼──────────┐
        ↓         ↓          ↓
      Cases   Compatibility  Graph
        │         │          │
        └─────────┼──────────┘
                  ↓
             Regression
                  ↓
          Knowledge Promotion
                  ↓
            Better Routing
```

## Release judgment

v1.1.0 is an architectural baseline for real MCP-connected operation.

It is deliberately **not** claiming a complete protector corpus. That corpus must be earned through real evidence.

The correct next growth path is data, not prose:
- authorized sample cases;
- reproducible public cases;
- provider compatibility observations;
- graph edges;
- regression fixtures.

## 2026-10-16 protocol cross-check (v1.5 audit)

- Official MCP Python SDK v2 client guide: https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/client/index.md — Client supports `StdioServerParameters`, Streamable HTTP and `list_tools`/`call_tool`; local installed SDK is **not** available for real-vendor handshake in this build session.
- Official client transports: https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/client/transports.md — custom HTTP clients use `httpx2.AsyncClient`; child process environment is intentionally limited; older SSE is legacy.
- Official MCP tool specification: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/server/tools.mdx — tool annotations and tool descriptions from untrusted servers are NOT authority for granting permissions.

This audit verified the published contract text and local unit/mock behavior; it did **not** validate real third-party MCP server installations, proprietary binaries, protector versions or runtime compatibility.
