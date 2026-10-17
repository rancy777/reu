# Workflow: windows-custom-packer

**Goal:** Unknown/customized loaders, staged mappings, protection code or sample-specific runtime transformations.

**Entry gate:** No reliable packer-version signature, or conventional unpacking cannot explain runtime behavior. Follow `references/workflow-contract.md` for authorization, evidence identity, and exit state.

## Discriminating questions

- Is execution mediated by a custom loader or multiple stages?
- What APIs/relocations or mapping semantics does the loader emulate?
- Which changes are stable across repeated controlled runs?

## Ordered investigation phases

1. **Phase 1:** Model loader, stage transitions, module origins and memory allocations from structural evidence; avoid assigning a commercial brand by resemblance.
2. **Phase 2:** Plan controlled observations of memory map changes, module loads, region permissions, API resolution, thread start addresses and initialization paths.
3. **Phase 3:** With authorization, capture timeline at a few narrowly selected boundaries and correlate bytes with observed executable regions.
4. **Phase 4:** Use disassembly, CFG comparison, bounded emulation or data-flow analysis to test a specific loader hypothesis, not to blindly automate arbitrary code execution.
5. **Phase 5:** Distinguish code compression, runtime decryption, overlays, resource payloads, shellcode, injection and virtualization; record counter-evidence.
6. **Phase 6:** Validate the minimal recovered representation and keep all results sample-scoped until independently reproduced.

## Completion, failure and fallback

**Validated exit condition:** Loader/payload lifecycle mapped with cited observations and testable failure/alternative branches.

**Failure diagnosis:**

- Anti-analysis symptoms may be tool/environment bugs: re-establish baseline before attributing intent.
- Multiple decoded stages: preserve stage hashes and timestamps rather than overwriting a single dump.

**Alternative route:**

- Program slicing, emulator/memory traces, manual high-level semantic recovery; explicit `Unknown` when not recoverable.

## Minimum report fields

`target_hash`, `input_representation`, `platform`, `architecture`, `runtime_version`, `protection_hypotheses`, `evidence_ids`, `counter_evidence`, `tool/provider_versions`, `observation_timeline`, `failed_tests`, `validated_result`, `limitations`, `sources`, `next_step`.

Do not upgrade sample-scoped outcomes to canonical protector behavior. If dynamic prerequisites are missing, stop at an actionable plan and mark runtime claims `Needs verification`.
