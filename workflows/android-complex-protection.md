# Workflow: android-complex-protection

**Goal:** Analyze multi-layer mobile protection without assuming universal DEX dump or anti-Frida bypass.

**Entry gate:** Multiple package/native/ART/anti-analysis mechanisms supported by distinct evidence. Follow `references/workflow-contract.md` for authorization, evidence identity, and exit state.

## Discriminating questions

- Which layer mediates access to protected code?
- Is the discrepancy caused by protection or the instrumenting environment?
- What is the minimum authorized measurement needed?

## Ordered investigation phases

1. **Phase 1:** Construct layered map: package → bootstrap → loader → ART/DEX/native payload → runtime transformation → protected routines → application behavior.
2. **Phase 2:** Enumerate independently supported signals of RASP, integrity, anti-debug, anti-hook, root detection, emulator detection and custom linkers; label self-reports untrusted.
3. **Phase 3:** With explicit authorization and strong isolation, compare baseline, instrumented and version-matched environments to separate protection from tool failure.
4. **Phase 4:** Observe dynamic libraries, memory regions, exception signals and class/native method behavior with minimal side effects; avoid broad instrument-all operations.
5. **Phase 5:** When code virtualization is suspected, build a sample-specific dispatcher/handler/VM state hypothesis and test semantics with bounded traces, not a purported general solution.
6. **Phase 6:** Set stop criteria for destructive effects, uncertain authorization, unknown dependencies or unverified outputs; present safer static/behavior alternatives.

## Completion, failure and fallback

**Validated exit condition:** Layer-specific protection assessment, failure diagnosis, evidence graph and scoped result; `Unknown` accepted.

**Failure diagnosis:**

- Anti-Frida attribution without neutral baseline is unsupported.
- False/hidden module listings require independent views, not a direct bypass claim.

**Alternative route:**

- Native static analysis, ART version research, isolated emulation, protocol/behavioral characterization.

## Minimum report fields

`target_hash`, `input_representation`, `platform`, `architecture`, `runtime_version`, `protection_hypotheses`, `evidence_ids`, `counter_evidence`, `tool/provider_versions`, `observation_timeline`, `failed_tests`, `validated_result`, `limitations`, `sources`, `next_step`.

Do not upgrade sample-scoped outcomes to canonical protector behavior. If dynamic prerequisites are missing, stop at an actionable plan and mark runtime claims `Needs verification`.
