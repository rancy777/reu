# Workflow: android-dex

**Goal:** Understand DEX/Smali/Java/Kotlin code, obfuscation versus packing, and recovered representation validity.

**Entry gate:** DEX present on disk, or runtime evidence indicates a DEX representation is or was materialized. Follow `references/workflow-contract.md` for authorization, evidence identity, and exit state.

## Discriminating questions

- DEX version and checksum/structure valid?
- Which classes/methods are real vs decompiler artifacts?
- Are name obfuscation and runtime encryption separate?

## Ordered investigation phases

1. **Phase 1:** Record each DEX hash, source module/split, version, header validity, method/class counts and dependency context.
2. **Phase 2:** Correlate JADX pseudocode with Smali and raw DEX indices for suspicious methods; handle synthetic Kotlin/R8 transformations separately.
3. **Phase 3:** Trace class references and ClassLoader usage; label encrypted buffers/dynamic loading as hypotheses until observed.
4. **Phase 4:** If runtime DEX exists, track loader identity, buffer/file origins, mapping time and class-resolution events in an authorized isolated app runtime.
5. **Phase 5:** Compare captured DEX parser validation, method signatures and class inventory against runtime observations; do not silently patch or re-sign the source package.
6. **Phase 6:** Report whether output is a read-only inventory, recovered DEX representation, or only equivalent behavior.

## Completion, failure and fallback

**Validated exit condition:** Validated DEX/class-method representation or precisely scoped unresolved loader hypothesis.

**Failure diagnosis:**

- JADX decompile fails but Smali parses: use low-level bytecode evidence rather than attributing protection.
- Runtime classes missing: re-check correct class loader, split and instrumentation time.

**Alternative route:**

- Smali-level CFG, native JNI analysis, ART runtime workflow.

## Minimum report fields

`target_hash`, `input_representation`, `platform`, `architecture`, `runtime_version`, `protection_hypotheses`, `evidence_ids`, `counter_evidence`, `tool/provider_versions`, `observation_timeline`, `failed_tests`, `validated_result`, `limitations`, `sources`, `next_step`.

Do not upgrade sample-scoped outcomes to canonical protector behavior. If dynamic prerequisites are missing, stop at an actionable plan and mark runtime claims `Needs verification`.
