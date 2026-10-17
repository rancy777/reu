# Runtime

Install from the source root with `python -m pip install -e .`. The optional MCP client is `.[mcp]`; offline tests use `.[test]`. See [Getting Started](../docs/getting-started.md) for isolated Windows and Linux installation.

Installing the CLI does not register the agent Skill. Use `python scripts/install_skill.py` from the source root for that separate step.

## Commands

| Command | Purpose | Side effects |
| --- | --- | --- |
| `system-probe` | Inspect PATH and Python module metadata | No provider/target launch |
| `doctor` | Check configured executables and transport policy | No connection |
| `triage --file ... --route` | Hash, classify, and route a file | Reads target; does not execute it |
| `route --input ...` | Route supplied metadata | Reads input JSON |
| `discover` | Discover enabled, registry-approved providers and tools | Launches/connects to providers |
| `adapter-plan` | Bind an intent to discovered tool names/schemas | No invocation |
| `call` | Invoke a provider tool | Separate observe/execute/mutate/destructive gates |
| `diagnose` | Return hypotheses and next observations | No experiment execution |
| `regress` | Run a selected regression dataset | Synthetic/policy checks only |

Use `re-skill --help` for corpus query, ingestion, and graph commands.

## MCP client and storage

Normal discovery/calls require the official MCP SDK v2. The constrained stdio `--wire` transport is explicit and reserved for fixtures/labs. Providers are installed separately, require registry approval, and are never silently downloaded.

A harmless local server in `tests/fixtures/mock_mcp_stdio.py` exercises the client protocol. It does not emulate a debugger, device, or protector.

Tool output is bounded to 64 MiB. A redacted preview and SHA-256 are stored by default when a workspace is selected. `--store-raw` explicitly stores complete output, which can contain secrets or proprietary material.

## Regression datasets

```bash
re-skill regress --strict --file corpus/regression/automated.jsonl
re-skill regress --file corpus/regression/research.jsonl
```

The first dataset is the 16-case strict offline CI gate. The second retains 8 research records (5 PARTIAL, 3 MANUAL); strict research mode returns `2`. Empty datasets and duplicate IDs are rejected. Newly ingested regression definitions go to the research dataset pending review.

Case similarity is retrieval, not validation. Multi-file graph updates remain eventually consistent; `graph-repair` reports missing nodes and `--apply` repairs nodes without inventing edges.

See [Verification](../docs/verification.md) for local results and [Project Status](../docs/project-status.md) for deferred real-tool work.
