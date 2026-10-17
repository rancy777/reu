# Workflow: windows-dotnet

**Goal:** Analyze managed, mixed-mode, ReadyToRun and NativeAOT-related PE behavior separately from native packing.

**Entry gate:** CLR/metadata evidence, managed code signals, or a runtime model requiring .NET-specific classification. Follow `references/workflow-contract.md` for authorization, evidence identity, and exit state.

## Discriminating questions

- Is CLR metadata present and loadable?
- Which framework/runtime/deployment mode is involved?
- Are IL, native ReadyToRun and NativeAOT representations distinguishable?

## Ordered investigation phases

1. **Phase 1:** Record PE structure, CLR directory, metadata streams, assembly manifest and target runtime; account for assemblies bundled in single-file deployment.
2. **Phase 2:** Use ILSpy/managed metadata views when IL is available; compare IL names, resources and call paths without assuming renaming implies packing.
3. **Phase 3:** Check obfuscation signs separately: IL rewriting, encryption, anti-tamper, metadata transformations, runtime assembly loading.
4. **Phase 4:** For ReadyToRun, map native and IL evidence without assuming every method was precompiled; for NativeAOT, prefer native CFG and symbols since normal IL reflection assumptions may not hold.
5. **Phase 5:** For runtime reconstruction, first define target assembly and state; only observe/debug under authorization and preserve original vs recovered module identity.
6. **Phase 6:** Validate recovered metadata/types/IL or native semantics using independent parsers.

## Completion, failure and fallback

**Validated exit condition:** Specific .NET representation identified and appropriate decompiler/runtime workflow chosen; output includes runtime/version caveats.

**Failure diagnosis:**

- ILSpy cannot load: consider NativeAOT/mixed-mode or corrupt metadata before claiming a protector.
- Assembly dump lacks expected types: consider dynamic load/single-file deployment or staging.

**Alternative route:**

- Analyze native code with Ghidra/IDA; document unknown runtime instead of guessing.

## Minimum report fields

`target_hash`, `input_representation`, `platform`, `architecture`, `runtime_version`, `protection_hypotheses`, `evidence_ids`, `counter_evidence`, `tool/provider_versions`, `observation_timeline`, `failed_tests`, `validated_result`, `limitations`, `sources`, `next_step`.

Do not upgrade sample-scoped outcomes to canonical protector behavior. If dynamic prerequisites are missing, stop at an actionable plan and mark runtime claims `Needs verification`.
