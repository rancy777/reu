# MCP Discovery and Binding

## Objective

Turn an arbitrary host MCP configuration into a deterministic reverse-engineering toolchain.

## Phase 1 — Discover

Inspect:
- server names
- tool names
- descriptions
- JSON schemas
- resources
- prompts
- tool annotations
- transport
- server metadata/version when exposed

Do not call a state-changing operation merely to discover it.

## Phase 2 — Normalize

Map each discovered tool to semantic capability IDs from `capability-taxonomy.md`.

Examples:
- a tool described as "list loaded modules" → `session.observe`
- a tool that reads process memory → `pe.memory` or `android.instrumentation`
- a tool that decompiles a function → `decompiler`
- a tool that lists APK classes → `android.dex`

Store:
- `provider_id`
- `server_name`
- `tool_name`
- `capability_id`
- `read_only`
- `destructive`
- `target_scope`
- `version`
- `discovered_at`

## Phase 3 — Health check

Before analysis:
- verify provider connectivity;
- verify native tool availability;
- verify target architecture;
- verify active session/target identity;
- verify expected output shape;
- verify permissions;
- verify version compatibility if known.

A healthy MCP server with a broken native application is not a healthy analysis provider.

## Phase 4 — Rank providers

Suggested ranking:
1. official + compatible + maintained
2. first-party project + compatible + maintained
3. community + compatible + reproducible
4. generic CLI wrapper
5. manual route

Tie-breakers:
- read-only support
- deterministic/headless operation
- structured output
- version pinning
- narrow tool surface
- local-only transport
- active maintenance
- independent evidence support

## Phase 5 — Bind

Create a session binding:

```yaml
provider: ida.hexrays.official
capabilities:
  - pe.static
  - decompiler
tool_versions:
  ida: "resolved-at-runtime"
  mcp: "resolved-at-runtime"
target:
  sha256: "<hash>"
  architecture: "x64"
  representation: "original"
```

## Phase 6 — Execute and normalize

Every tool call becomes an observation record:
- operation
- provider
- tool
- input reference
- output reference
- timestamp
- target/session identity
- status
- stderr/error
- completeness
- derived observations

The agent may summarize tool output for reasoning, but should retain a raw reference when feasible.

## Provider disagreement

If IDA says one thing and Ghidra says another:
- do not average;
- preserve both observations;
- inspect representation and analysis settings;
- test the disputed fact with a third modality;
- create a contradiction edge;
- resolve only when evidence supports resolution.

## Provider upgrade

When a provider/native tool changes:
1. record old and new versions;
2. run provider health tests;
3. replay affected regression cases;
4. compare normalized outputs;
5. do not silently rewrite historical case results.
