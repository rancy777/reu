# Workflow: android-art-runtime

**Goal:** Version-aware investigation of ART/Dalvik, DEX, CDEX, OAT, ODEX and VDEX artifacts.

**Entry gate:** ART output files or evidence that on-disk DEX differs from the executing representation. Follow `references/workflow-contract.md` for authorization, evidence identity, and exit state.

## Discriminating questions

- Which Android API/ART version and compilation mode?
- Is artifact file-backed, JIT-generated, AOT or interpreted?
- Can the representation be parsed by a version-aware tool?

## Ordered investigation phases

1. **Phase 1:** Record device fingerprint, Android version, API level, runtime, ABI, ART/APEX component version when available and artifact acquisition context.
2. **Phase 2:** Distinguish DEX, CompactDex, OAT, ODEX, VDEX and ART image headers with version-aware parsers; do not use fixed historical offsets blindly.
3. **Phase 3:** Map app class loader, split inputs, profiles and dexopt compilation artifacts (interpretation/JIT/AOT), where observable.
4. **Phase 4:** Correlate runtime function/class evidence with installed modules and code origins without assuming everything exists in one DEX image.
5. **Phase 5:** Use read-only logging/parsing first; scoped dynamic observation requires authorization and known tool/runtime compatibility.
6. **Phase 6:** Validate conclusions against AOSP ART documentation/source matched to the device version and state the version range explicitly.

## Completion, failure and fallback

**Validated exit condition:** Source → runtime representation provenance model, including precise Unknowns for unsupported ART layouts.

**Failure diagnosis:**

- Parser version mismatch should not be mislabeled as encrypted DEX.
- No VDEX/OAT file can be normal for certain runtime states and device builds.

**Alternative route:**

- AOSP source comparison, JNI/native code analysis, managed reflection or independent DEX parser.

## Minimum report fields

`target_hash`, `input_representation`, `platform`, `architecture`, `runtime_version`, `protection_hypotheses`, `evidence_ids`, `counter_evidence`, `tool/provider_versions`, `observation_timeline`, `failed_tests`, `validated_result`, `limitations`, `sources`, `next_step`.

Do not upgrade sample-scoped outcomes to canonical protector behavior. If dynamic prerequisites are missing, stop at an actionable plan and mark runtime claims `Needs verification`.
