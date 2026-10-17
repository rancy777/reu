# Workflow: windows-triage

**Goal:** Identify Windows PE architecture, managed/runtime branch, suspicious structural indicators and analysis goals.

**Entry gate:** PE signature validated or the user provides well-formed structural outputs. Follow `references/workflow-contract.md` for authorization, evidence identity, and exit state.

## Discriminating questions

- PE32 or PE32+, x86/x64/ARM64?
- CLR metadata, mixed mode or native?
- Are imports/sections/TLS/relocations/overlay/entry point consistent?
- Does packer evidence outlive independent parser verification?

## Ordered investigation phases

1. **Phase 1:** Record SHA-256 and provenance; do not execute unknown PE on the host. Establish PE32/PE32+, machine, image base, entry RVA, data-directory count.
2. **Phase 2:** Inspect section raw-vs-virtual bounds, alignment, entry location, RWX permissions, and high entropy with sampled-size context. Treat nonstandard names as inconclusive.
3. **Phase 3:** Inventory import/export/delay-import, TLS, relocations, exception directory, load config, debug directory, resources, overlay and certificate region.
4. **Phase 4:** Classify native, CLR/IL, ReadyToRun possibility, NativeAOT possibility and mixed-mode uncertainty; route .NET separately when metadata warrants.
5. **Phase 5:** Compare DIE/packer signatures with independent parsing; collect readable strings and capability evidence (FLOSS/capa/YARA) but mark results potentially incomplete when packed.
6. **Phase 6:** Build hypotheses for packing, optimization, custom loader, false positives and virtualization when supported; choose the cheapest discriminating observation.

## Completion, failure and fallback

**Validated exit condition:** Triage report includes architecture, representations, evidence IDs, conflicting hypotheses, tool version and next workflow.

**Failure diagnosis:**

- Malformed PE: preserve offsets and avoid forcibly repairing original artifact.
- DIE disagreement: record rule version and independent parser results; do not pick a winner by popularity.
- High entropy alone: mark heuristic, not confirmed packing.

**Alternative route:**

- PE spec and hex-level analysis; read-only pefile/LIEF/PE-bear comparison.

## Minimum report fields

`target_hash`, `input_representation`, `platform`, `architecture`, `runtime_version`, `protection_hypotheses`, `evidence_ids`, `counter_evidence`, `tool/provider_versions`, `observation_timeline`, `failed_tests`, `validated_result`, `limitations`, `sources`, `next_step`.

Do not upgrade sample-scoped outcomes to canonical protector behavior. If dynamic prerequisites are missing, stop at an actionable plan and mark runtime claims `Needs verification`.
