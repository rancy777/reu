# Workflow: android-native

**Goal:** Analyze ELF SO and JNI cross-layer behavior, including native protection and custom linker paths.

**Entry gate:** SO library with confirmed Android package/runtime provenance, JNI imports or native execution evidence. Follow `references/workflow-contract.md` for authorization, evidence identity, and exit state.

## Discriminating questions

- ABI and ELF program headers?
- JNI_OnLoad/export versus RegisterNatives dynamic mapping?
- Is loaded module view consistent with maps and linker state?

## Ordered investigation phases

1. **Phase 1:** Map package split and ABI to the actual SO file; SHA-256 source and decompiler database.
2. **Phase 2:** Inspect ELF segments, dynamic dependencies, relocation types, PLT/GOT, init arrays, TLS and unwinding metadata where applicable.
3. **Phase 3:** Link Java/Kotlin native declarations to JNI_OnLoad, RegisterNatives and native function addresses; distinguish generated wrappers from business code.
4. **Phase 4:** Under authorization, compare linker-loaded modules, /proc maps, executable private regions and call stacks when module enumeration is incomplete or misleading.
5. **Phase 5:** Use Unidbg/Unicorn only to isolate a specific JNI/native question and document mocked JavaVM/syscall behavior; validate on genuine target runtime before generalizing.
6. **Phase 6:** Record outputs as functions/CFG/behavior/ELF capture and verify with independent parsers or instrumented observations.

## Completion, failure and fallback

**Validated exit condition:** JNI/native call map, mechanism hypotheses and validated representation with environment provenance.

**Failure diagnosis:**

- Missing exports may be normal dynamic registration; inspect actual JNI registration.
- Unidbg succeeds but device differs: treat as model/environment mismatch and revalidate.

**Alternative route:**

- Native static CFG, LLDB in approved lab, ART/JNI cross-layer correlation.

## Minimum report fields

`target_hash`, `input_representation`, `platform`, `architecture`, `runtime_version`, `protection_hypotheses`, `evidence_ids`, `counter_evidence`, `tool/provider_versions`, `observation_timeline`, `failed_tests`, `validated_result`, `limitations`, `sources`, `next_step`.

Do not upgrade sample-scoped outcomes to canonical protector behavior. If dynamic prerequisites are missing, stop at an actionable plan and mark runtime claims `Needs verification`.
