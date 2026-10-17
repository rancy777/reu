# Corpus Status — 2026-10-16 / v1.5.0

These datasets are separate, with different truth standards:

| Asset | Current known inventory | What it proves |
|---|---|---|
| `protector-cases/index.jsonl` | **1** public educational CrackMe case metadata entry; SHA256 and specific Protector version `Unknown` | Only that a public page describes a case. NOT independently validated unpacking. |
| `protector-family-index.jsonl` | **14** mechanism family metadata cards | Family/category/source discovery, NOT 14 sample cases. |
| `runtime-compatibility/index.jsonl` | **0** experimental observations | No verified OS/API/Frida/Protector compatibility claims yet. |
| `evidence-graph/nodes.jsonl`, `edges.jsonl` | Seed public-source/case references | Cross-referencing source/observation/case, NOT runtime ground truth. |
| `regression/automated.jsonl` | **16** fully executable regression records | Strict offline acceptance for deterministic policies, not protector-specific successful unpacking. |
| `regression/research.jsonl` | **8** research regression records: 5 PARTIAL, 3 MANUAL | Retains the remaining research assertions; strict mode exits 2. |

For real analysis the agent should append provenanced observations, validated provider versions, actual sample hashes, environment facts, experiment outcomes, failures, and independent sources. Only run `promote-check` after enough corroboration; it NEVER automatically marks material `Canonical`.

## v1.5 persistence caveats

JSONL writes now use a host-local advisory lock and ID deduplication. Multi-file evidence graph updates remain eventually consistent: crash recovery must be explicit via `graph-repair`. No real compatibility experiment data has been fabricated; absence of a record remains `Unknown`. All example research claims remain **case-scoped**.

The two regression files retain all 24 original records without changing their assertions. New definitions enter the research dataset pending review. Real-provider and protected-sample validation remain deferred.
