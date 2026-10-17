# Workflow: windows-virtualization

**Goal:** Investigate virtualization-based protection and distinguish it from ordinary packing.

**Entry gate:** Multiple static and/or dynamic observations suggest VM dispatch/handlers/context transitions. Follow `references/workflow-contract.md` for authorization, evidence identity, and exit state.

## Discriminating questions

- What evidence supports an interpreter or VM?
- Which native regions feed virtualized code and which are ordinary functions?
- What semantics can be independently validated?

## Ordered investigation phases

1. **Phase 1:** Map ordinary PE/runtime state first and define the protected functions/paths.
2. **Phase 2:** Inspect indirect control flow, candidate dispatcher/handler tables, encoded state, unusual CFG and data-flow patterns as hypotheses, not universal signatures.
3. **Phase 3:** In an authorized lab, correlate candidate dispatcher execution with runtime traces and compare multiple inputs to distinguish dispatcher from standard event loops.
4. **Phase 4:** Model a *sample-specific* instruction/state transition relation and record which routines remain native or virtualized.
5. **Phase 5:** Use bounded emulation or symbolic execution only for a measurable property (reachable branches, state variable, input-output behavior).
6. **Phase 6:** Validate recovered semantics against observed execution traces or known test vectors. Never claim that a memory dump alone has removed virtualization.

## Completion, failure and fallback

**Validated exit condition:** Sample-scoped VM/handler model or validated semantics for requested code paths, with explicit unknown regions.

**Failure diagnosis:**

- A dense indirect call graph alone is not proof of virtualization.
- Version/config changes may invalidate all prior handler descriptions.

**Alternative route:**

- Black-box behavioral characterization, data-flow/taint analysis, manual CFG recovery.

## Minimum report fields

`target_hash`, `input_representation`, `platform`, `architecture`, `runtime_version`, `protection_hypotheses`, `evidence_ids`, `counter_evidence`, `tool/provider_versions`, `observation_timeline`, `failed_tests`, `validated_result`, `limitations`, `sources`, `next_step`.

Do not upgrade sample-scoped outcomes to canonical protector behavior. If dynamic prerequisites are missing, stop at an actionable plan and mark runtime claims `Needs verification`.
