# Workflow: windows-basic-unpacking

**Goal:** Investigate conventional runtime code decompression/decryption where a mapped representation may differ from disk.

**Entry gate:** Strongly supported runtime transformation hypothesis; task is authorized and appropriate isolation is available. Follow `references/workflow-contract.md` for authorization, evidence identity, and exit state.

## Discriminating questions

- What representation is needed: functions, memory image or runnable PE?
- When does code become available?
- Is the observed entry point loader/OEP/TLS/runtime generated?

## Ordered investigation phases

1. **Phase 1:** Preserve static baseline and record protected file hash, OS, ABI and toolchain. Agree on research output format before executing.
2. **Phase 2:** With explicit authorization, observe process creation, memory mappings, private executable pages, protection transitions, imports, and early callbacks in a disposable VM.
3. **Phase 3:** Correlate changed regions and execution traces with a candidate unpacked code boundary. Treat candidate OEP as one hypothesis, not proof of completion.
4. **Phase 4:** Capture only the representation necessary for research; record capture time, mapping base, page characteristics and output digest.
5. **Phase 5:** If a reconstructed PE is needed, separately verify headers, RVA/raw section mapping, IAT/delay imports, relocations, TLS, exception and load-config metadata.
6. **Phase 6:** Re-open the capture in an independent static analyzer and compare control/data flow or behavior in an isolated environment when approved.

## Completion, failure and fallback

**Validated exit condition:** Validated reconstruction or explicitly scoped recovered representation with independent evidence and limitations.

**Failure diagnosis:**

- Dump does not start: test IAT, section mapping, base relocations, TLS, exception directory and runtime dependencies separately.
- Observed entry unstable: suspect staged loader or runtime-generated code, not necessarily failed OEP detection.

**Alternative route:**

- Memory-region analysis rather than runnable PE; escalate custom loader or virtualization workflow.

## Minimum report fields

`target_hash`, `input_representation`, `platform`, `architecture`, `runtime_version`, `protection_hypotheses`, `evidence_ids`, `counter_evidence`, `tool/provider_versions`, `observation_timeline`, `failed_tests`, `validated_result`, `limitations`, `sources`, `next_step`.

Do not upgrade sample-scoped outcomes to canonical protector behavior. If dynamic prerequisites are missing, stop at an actionable plan and mark runtime claims `Needs verification`.
