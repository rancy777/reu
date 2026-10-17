# Workflow: android-triage

**Goal:** Identify Android package layout, compiler/obfuscator signals, runtime context and analysis branch.

**Entry gate:** APK/AAB/APKS or trustworthy package/manifest/DEX/ELF analysis evidence. Follow `references/workflow-contract.md` for authorization, evidence identity, and exit state.

## Discriminating questions

- Single APK, split or bundle?
- Which DEX/SO belongs to each module and ABI?
- R8/ProGuard obfuscation, runtime packer or native loader?

## Ordered investigation phases

1. **Phase 1:** Hash source and inventory container members safely without executing or extracting untrusted contents by default.
2. **Phase 2:** For AAB/APKS/splits, map modules, base/configuration/dynamic-feature splits and target device configuration before concluding a component is absent.
3. **Phase 3:** Record package/version, min/target SDK, signing characteristics, manifest components, permissions and debuggable flag.
4. **Phase 4:** Inventory classes*.dex, secondary DEX, native SOs and ABI paths per split; track duplicate/overridden resources.
5. **Phase 5:** Compare APKiD fingerprint with JADX/Apktool structural evidence. Distinguish optimization/renaming, code packing, DEX encryption and native RASP.
6. **Phase 6:** Choose DEX, dynamic loader, JNI/native, ART runtime or complex protection workflow from observed evidence; establish device/ART/Frida compatibility before instrumentation.

## Completion, failure and fallback

**Validated exit condition:** Package/module/ABI inventory, reasoned protection hypotheses and next workflow with evidence IDs.

**Failure diagnosis:**

- Manifest/resource decoder disagrees: compare tool versions and raw package structure.
- A single split misses DEX/SO: inspect related modules before inferring hidden code.

**Alternative route:**

- Bundletool-driven module inventory on approved fixtures; no device run needed for structural triage.

## Minimum report fields

`target_hash`, `input_representation`, `platform`, `architecture`, `runtime_version`, `protection_hypotheses`, `evidence_ids`, `counter_evidence`, `tool/provider_versions`, `observation_timeline`, `failed_tests`, `validated_result`, `limitations`, `sources`, `next_step`.

Do not upgrade sample-scoped outcomes to canonical protector behavior. If dynamic prerequisites are missing, stop at an actionable plan and mark runtime claims `Needs verification`.
