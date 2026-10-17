# Workflow: android-split-aab

**Goal:** Identify AAB/split module contents before any DEX/ELF inference.

**Entry gate:** AAB, APKS or known multi-APK package, with target device/module context known or Unknown. Follow `references/workflow-contract.md` for authorization, evidence identity, and exit state.

## Discriminating questions

- Base vs dynamic feature vs config split?
- Which device configuration produced installed APKs?
- Where do each class, resource and ABI-specific library originate?

## Ordered investigation phases

1. **Phase 1:** Hash and list source AAB/APKS metadata and modules using bounded archive inventory; never assume it is a standalone APK.
2. **Phase 2:** Record base/module manifest files, package metadata and split dependency relations; use official bundletool as a read-only structural reference where possible.
3. **Phase 3:** If generation/install is authorized, pin bundletool version and device specification and record the generated APK-set digest; avoid using arbitrary real-user device data.
4. **Phase 4:** Index each DEX/SO/resource by (bundle hash, module, split, path, ABI) and detect duplicate or overridden classes.
5. **Phase 5:** Correlate observed process/runtime package with actual installed splits; a missing component in base is not a hidden payload by itself.
6. **Phase 6:** Route managed bytecode to android-dex and native code to android-native with split provenance attached.

## Completion, failure and fallback

**Validated exit condition:** Reproducible module/split/ABI map with versioned inputs and correct child workflows.

**Failure diagnosis:**

- No classes in base: check dynamic feature delivery.
- SO absent in one ABI split: check device ABI and package splits.
- Nonstandard APK-set format: preserve exact original and mark tool support `Needs verification`.

**Alternative route:**

- Android Developers App Bundle Format and bundletool documentation, read-only ZIP metadata.

## Minimum report fields

`target_hash`, `input_representation`, `platform`, `architecture`, `runtime_version`, `protection_hypotheses`, `evidence_ids`, `counter_evidence`, `tool/provider_versions`, `observation_timeline`, `failed_tests`, `validated_result`, `limitations`, `sources`, `next_step`.

Do not upgrade sample-scoped outcomes to canonical protector behavior. If dynamic prerequisites are missing, stop at an actionable plan and mark runtime claims `Needs verification`.
