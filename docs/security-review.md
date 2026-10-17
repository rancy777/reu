# Security Review Notes — v1.5.0

Review date: **2026-10-16**. These are project-maintained review notes, not an independent assessment or certification. Historical findings below describe the v1.4/v1.5 source review. Current executable checks and their limits are recorded in [Verification](verification.md). Real-provider and protected-sample validation are deferred.

## Review summary

v1.4.0 shipped executable MCP code but had **material security and correctness gaps**. v1.5.0 addresses code-review findings and adds test coverage; deployment of arbitrary third-party MCP providers remains unsafe without sandboxing and independent code review. This is an offline-reviewed engineering candidate, not production approval for an Internet-connected analysis workstation.

## Findings and dispositions

| ID | Severity | Finding in v1.4.0 | Repair in v1.5.0 | Verification |
|---|---|---|---|---|
| SEC-01 | Critical | Provider could be launched during discovery even if quarantined/absent from registry; direct call did not enforce registry approval | Verify Registry approval **before** starting provider, and mandatory `call --registry` check | blocked-provider and direct-call unit tests |
| SEC-02 | High | MCP client silently downgraded to narrower homegrown protocol transport if official SDK missing | Official `mcp>=2.3,<3` required by default; isolated test/lab must explicitly opt into `--wire` | missing-SDK negative test and subprocess fixture |
| SEC-03 | High | Unredacted tool results could be automatically persisted | Only bounded, best-effort redacted previews stored by default. `--store-raw` is explicit, size-limited, 0600 files with SHA-256 | secret-handling and file mode tests |
| SEC-04 | High | Registry capabilities or malicious tool descriptions could be mistaken for proven operations | Automatic mapping requires observed named tool operation; descriptions remain lower-confidence hints | injection-like description test and provider ranking fixture |
| SEC-05 | High | Unknown tools, package-manager MCP launchers and mutable operations needed tighter boundaries | Separate execute/mutate/destructive gates; block shell interpreters; package-manager launcher requires recorded supply-chain review; command/script-bearing *read-like* tool schemas fail closed | authorization tests and launcher tests |
| SEC-06 | High | Untrusted MCP inputSchema could trigger remote `$ref` or expensive regexp evaluations | Schema and argument limits; reject `$ref`, `$dynamicRef`, regex patterns; require object schema at root | hostile schema fixture tests |
| SEC-07 | Medium | Tool parameters/schema validation errors could print secret user values to CLI | Generic `ValidationError` message without arguments | captured-output assertion |
| SEC-08 | Medium | MCP `tools/list` before `tools/call` had no call path timeout; oversized responses could exhaust memory | Bound listing with configured timeout and enforce 64 MiB response cap even without raw-output storage | async timeout and large-result tests |
| DATA-01 | High | Corpus append was not process safe: duplicate IDs and partial reads possible | Advisory cross-process single-host lock, fsync, validation, duplicate guard and symlink/path defenses | threaded writers test, path tests |
| DATA-02 | High | Evidence graph generated nodes not consistently matching node schema | Generate schema-conformant node records and verify all shipped JSONL | complete schema-registry test |
| DATA-03 | Medium | Multi-file updates are not atomic; compatibility evidence could be wrongly reused | Graph repair dry-run/apply, conservative version-specific compatibility gate; never reconstruct missing evidence automatically | interrupted write, compatibility mismatch tests |
| REASON-01 | High | Source count could imply independence without provenance review | Explicit human review of source independence, reproductions, experiment IDs; still no automated canonical promotion | source dependence tests |
| ROUTE-01 | Medium | Plain ELF `.so` could be routed to Android only because of the suffix | Only Android-specific signals route to Android native; otherwise generic ELF | native routing tests |
| DOC-01 | Medium | Some routed workflow files absent or under-specified | Added and expanded all routed workflows with entry, observations, failure, validation and stop conditions | all-routed-path test |
| TEST-01 | High | Several regression rows only had undocumented prose assertions | Declarative checks without eval; strict CLI gate fails on partial/manual | 24 rows, deterministic runner, strict exit test |

## Earlier recorded checks

- `PYTHONPATH=runtime python -m pytest -q runtime/tests`: **67 passed, 1 skipped, 12 subtests passed**.
- Mock MCP subprocess (not a real RE tool) executed via `doctor`, `discover --wire`, and `call --wire` with user authorization policy; persisted successful observation, raw-output hash, 2 graph nodes and 1 edge.
- `regress`: **16 PASS / 5 PARTIAL / 3 MANUAL / 0 FAIL**; `--strict` exits with **2** because the latter eight items are not fully automated.
- Wheel `reverse_engineering_unpacking_runtime-1.5.0-py3-none-any.whl` built and installed into an isolated target; `re_skill.__version__ == '1.5.0'`; **7 bundled JSON schemas** found.
- Source ZIP validated using `scripts/release.py --verify`, SHA-256 and member-by-member ZIP equality (see [current verification](verification.md)).

## Trust boundaries remaining

1. **Actual installed MCP Server code is not trusted or sandboxed** by client authorization. A malicious provider can perform actions during startup, before any `tools/call`. Deploy under isolated OS identities/VMs with restricted files, network, secrets, and no direct host access. Registry status and `supply_chain_review_id` are operator attestations, not proof.
2. Tool name inference is conservative but **not proof of read-only behavior**. Server authors control names and implementations. For high-risk contexts restrict operations with separately reviewed/pinned provider adapters and OS sandbox policies.
3. Best-effort redaction is **not DLP**; arbitrary source text or embedded secrets may still leak. For sensitive analysis, disable storing raw responses, isolate the corpus, and avoid unapproved remote MCP servers.
4. JSONL advisory locks work for cooperative writers on a **single host**, not NFS or distributed agents. Multi-file operations are not atomic. For serious multi-agent ingestion, use a transactional database (SQLite for one host; PostgreSQL for multi-host), backed up with migration/recovery tests.
5. `--authorized-target` is explicit operator consent, **not externally verified legal authorization**. Do not treat it as a cryptographic or compliance proof.
6. Official MCP SDK 2.3.0 stdio has now been tested against a harmless local fixture; **real IDA/Frida/JADX providers remain untested**. HTTP+auth, legacy SSE, provider schema differences, and desktop debugger versions need separate staging.
7. RAG/source retrieval and knowledge update are workflow+data contracts, not continuously running web crawlers or trained model updates. This package never claims autonomous code repair or guaranteed unpacking.
8. The 14 documented workflows do not prove protection-specific effectiveness. No genuine protected executable/APK was executed in this review, and runtime-compatibility corpus contains **zero measured cross-version cases**.

## Review boundary

- No blocked or unknown provider may be launched; unknown/mutating tools denied without explicitly reviewed authorization.
- Offline unit and schema tests and the strict automated dataset must pass. The separate research dataset retains PARTIAL/MANUAL results and is not certified by that gate.
- ZIP/manifest/wheel integrity should be verified at every release; do not auto-install third-party upstream MCP servers from unpinned tags.

## Primary standards

- Model Context Protocol specification: https://modelcontextprotocol.io/specification/2025-06-18/server/tools — tool annotations are hints, not trustworthy authority.
- Official Python client: https://py.sdk.modelcontextprotocol.io/client/ — `Client`, `list_tools`, `call_tool`, error/transport model.
- MCP protocol schema: https://github.com/modelcontextprotocol/python-sdk/blob/main/schema/2026-07-28.json — tool `inputSchema`, `CallToolResult`, pagination requirements.
