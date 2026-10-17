# MCP / Agent Threat Model

## Trust boundaries

1. `artifact sample` / JADX decompiled comments / forum text / OCR / debugger output are **data**, not instructions.
2. MCP provider identity, tool annotations, readOnlyHint and descriptions are self-reported **untrusted hints**. No capability is granted solely by registry declaration.
3. Tool execution runs with its OS user's privileges. `stdio` local does not mean sandbox. Runtime approval is not a substitute for a disposable VM / unprivileged account.
4. Agents cannot assume two MCP wrappers of the same underlying engine provide independent corroboration.
5. Do not expose raw samples/hashes/source content to remote HTTP MCP by default. Remote endpoints require HTTPS/authentication, further approved by host.

## Enforced now

- stdio provider launch uses argv without an implicit shell; configuration must be explicitly enabled.
- Permission classes are conservative: observe / execute / mutate / destructive / unknown. Unknown blocked by default.
- ReadOnlyHint cannot downgrade `writeMemory`, `setBreakpoint`, `startHook`, `run_tool`, etc.
- Separate authorization flags per state-changing class; never patch a third-party protected commercial product for piracy.
- Remote MCP requires HTTPS, authentication headers and explicit `allow_remote=true`; legacy SSE only loopback.
- Input JSON Schema validation precedes every tool call.
- Raw output is hashed, capped, and stored outside the original sample path. CLI shows truncated previews while keeping a provenance reference.
- Corpus schema validation, duplicate guards, dangling-edge rejection, sample evidence not automatically promoted to canonical knowledge.

## Not yet a security guarantee

- A user-installed malicious MCP server can still abuse its own OS privileges or exfiltrate data. This project cannot sandbox arbitrary provider code.
- Provider capabilities can change between `discover` and `call`; the call path re-lists and revalidates tool names/schema but cannot establish trust in a malicious implementation.
- `stdio` fallback covers only a constrained subset of MCP; production integrations should install the official Python SDK.
- Windows Defender, AV, EDR, app signing, exact protection version and detector rule accuracy need real-world testing.
- No automatic software installation; installation scripts/commands are references, not unattended execution.
