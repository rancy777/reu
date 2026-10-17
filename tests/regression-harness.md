# Regression Harness

## Purpose

Prevent the skill from becoming more knowledgeable but less reliable.

## Required suites

1. Routing
2. Classification
3. Evidence discipline
4. MCP provider discovery
5. Provider fallback
6. Failure diagnosis
7. Compatibility handling
8. Corpus schema validation
9. Safety
10. Report completeness

## Determinism

A regression should not depend on:
- current wall-clock time;
- random provider ordering;
- unpinned external releases;
- mutable public sample URLs.

When live web research is required, assert process behavior rather than exact ranking.

## Provider regression

For each pinned provider:
- initialize;
- list tools;
- map capabilities;
- health check;
- run a harmless fixture;
- normalize output;
- compare expected structural properties.

## Corpus regression

Validate every JSONL record against its schema.

Check:
- unique IDs;
- valid edge endpoints;
- no orphaned required evidence references;
- no secret-like strings;
- no raw private sample content.

## Promotion regression

A finding that lacks required corroboration must never become canonical solely because the corpus grew.

## Release gate

Fail release if:
- a critical routing case regresses;
- a schema becomes invalid;
- a provider marked recommended is unavailable without fallback;
- a safety regression appears;
- an old fact is silently overwritten.

## Declarative regression rows (v1.5)

New rows can specify `input.executor` = `route`, `diagnose`, `compatibility`, or `tool-effect`, and `input.data` as an object. `expected.checks` is an array of `{path, op, value}` where `op` is `eq`, `ne`, `contains`, `not-contains`, `subset`, or `exists`. The runner intentionally contains **no Python eval/execution**. Unknown executors are errors, not automatically passed test cases.

Rows lacking deterministic assertions remain `MANUAL`; mixed rows are `PARTIAL`; neither counts as `PASS`. Record test identifiers, fixture input and observed output before changing a Provider adapter.

## Offline acceptance scope

Use `re-skill regress --strict --file corpus/regression/automated.jsonl` for the 16 fully executable records. The separate `research.jsonl` retains 5 PARTIAL and 3 MANUAL records and must not be presented as strict success. The test suite checks that all 24 IDs are preserved without overlap. Empty datasets and duplicate IDs fail.
