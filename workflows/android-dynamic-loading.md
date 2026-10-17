# Workflow: android-dynamic-loading

**Goal:** Attribute dynamic DEX/class or native library loading and materialization to a specific runtime stage.

**Entry gate:** DexClassLoader/InMemoryDexClassLoader/dynamic feature or custom loader evidence exists. Follow `references/workflow-contract.md` for authorization, evidence identity, and exit state.

## Discriminating questions

- What loader and process owns the code?
- When is code available and how is it represented?
- Which observations distinguish dynamic feature delivery from encrypted code?

## Ordered investigation phases

1. **Phase 1:** Build timeline process start → split/module delivery → loader creation → payload availability → class resolution/invocation → cleanup.
2. **Phase 2:** Correlate on-disk DEX, asset/resource payload and observed buffers without assuming every memory region is reconstructible as DEX.
3. **Phase 3:** Choose read-only API/runtime observation first; confirm Frida/ART/ABI/device baseline before attributing an attach crash to anti-hooking.
4. **Phase 4:** When authorized, observe loader names/parent relationships, class-resolution events, memory mapping changes and JNI/native dispatch as needed.
5. **Phase 5:** Record each artifact as file-backed, buffer-backed, anonymous executable, generated, or unknown with timestamp and SHA-256 where possible.
6. **Phase 6:** Validate recovered content with independent DEX/ELF parsers; report classes missing due to timing or splits explicitly.

## Completion, failure and fallback

**Validated exit condition:** Time-scoped loader and code-materialization map backed by sample observations.

**Failure diagnosis:**

- Frida attach crash: compare without instrumentation, version/ABI match, ART logs and native tombstone.
- No on-disk DEX: consider in-memory loader, feature module or native-only code.

**Alternative route:**

- ART-level observation, read-only logs, native loader trace, static cross-layer analysis.

## Minimum report fields

`target_hash`, `input_representation`, `platform`, `architecture`, `runtime_version`, `protection_hypotheses`, `evidence_ids`, `counter_evidence`, `tool/provider_versions`, `observation_timeline`, `failed_tests`, `validated_result`, `limitations`, `sources`, `next_step`.

Do not upgrade sample-scoped outcomes to canonical protector behavior. If dynamic prerequisites are missing, stop at an actionable plan and mark runtime claims `Needs verification`.
