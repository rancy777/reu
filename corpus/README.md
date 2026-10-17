# Research Corpus

This directory is the durable learning substrate for the skill.

## Four stores

### 1. Protector Case Corpus
`protector-cases/`

One JSON object per line. Each record is scoped to a concrete sample or public case.

### 2. Runtime Compatibility Matrix
`runtime-compatibility/`

One JSON object per line. Each record describes an observed compatibility relation.

### 3. Evidence Graph
`evidence-graph/nodes.jsonl`
`evidence-graph/edges.jsonl`

Nodes represent claims, observations, sources, experiments, artifacts, cases, tools, versions, runtimes and workflows.

Edges represent provenance and logical relationships.

### 4. Regression Corpus
`regression/`

Deterministic cases used to prevent routing and reasoning regressions.

## Data rules

- JSONL is append-friendly and diff-friendly.
- Schemas live under `corpus/schemas/`.
- Use stable IDs; never recycle an ID.
- Hash sensitive artifacts; do not embed private samples.
- Record legal/provenance status.
- Use UTC timestamps in ISO-8601.
- Preserve `source_ids` and `evidence_ids`.
- Use `Unknown` / `Needs verification` instead of fabricated values.
- Do not store secrets, credentials, personal data, or commercial license material.

## Promotion pipeline

`raw observation → evidence card → case → corroborated research → canonical knowledge`

A case can be valuable without becoming canonical knowledge.

## Corpus quality gates

A case is regression-eligible only if:
- target identity is stable;
- tool/MCP versions are recorded;
- expected observation is deterministic or tolerance-bounded;
- success/failure criteria are explicit.

A compatibility record is canonical only if its test conditions are complete.

A graph edge must have a reason/provenance.

## Initial corpus status

The v1.1.0 package intentionally does **not** fabricate protector cases. It provides schemas, indexes, graph contracts, and regression fixtures. Real cases should enter only after actual analysis or verifiable public research.
