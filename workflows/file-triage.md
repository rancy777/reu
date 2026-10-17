# Workflow: file-triage

**Goal:** Unknown or conflicting magic numbers, malformed files, deceptive extensions, or unsupported input.

**Entry gate:** Input is a file or incomplete tool result and no trusted format has been established. Follow `references/workflow-contract.md` for authorization, evidence identity, and exit state.

## Discriminating questions

- Can the input be hashed without execution?
- What magic/headers/embedded members support each candidate file type?
- Are extension, metadata and parser outputs inconsistent?

## Ordered investigation phases

1. **Phase 1:** Preserve name, byte length, acquisition path, SHA-256 and OS/stat provenance. Do not run or unpack embedded members.
2. **Phase 2:** Run read-only structural parsers or `re-skill triage` and compare file magic; prefer true format over filename.
3. **Phase 3:** If the input is a container, list entries with size/compression caps, never auto-extract unknown entries.
4. **Phase 4:** If parsers disagree, save both results, version information and offsets; keep `Unknown` until supporting evidence is obtained.
5. **Phase 5:** Route to PE, .NET, Android package, DEX, native ELF, or manual format research only after positive identification.

## Completion, failure and fallback

**Validated exit condition:** Sufficient structural evidence for a platform/type route; or a precise `Unknown` with discriminating next test.

**Failure diagnosis:**

- Damaged header; test another parser without claiming a protector.
- Archive size or nesting cap exceeded; stop and use isolated forensic tooling.

**Alternative route:**

- Read bytes and signature only; offline file-format specification research.

## Minimum report fields

`target_hash`, `input_representation`, `platform`, `architecture`, `runtime_version`, `protection_hypotheses`, `evidence_ids`, `counter_evidence`, `tool/provider_versions`, `observation_timeline`, `failed_tests`, `validated_result`, `limitations`, `sources`, `next_step`.

Do not upgrade sample-scoped outcomes to canonical protector behavior. If dynamic prerequisites are missing, stop at an actionable plan and mark runtime claims `Needs verification`.
