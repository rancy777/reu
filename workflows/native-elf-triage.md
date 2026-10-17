# Workflow: native-elf-triage

**Goal:** Native ELF binaries, generic Linux shared objects, and bare `.so` files not proven to belong to Android.

**Entry gate:** ELF magic is confirmed; platform context is missing or not Android. Follow `references/workflow-contract.md` for authorization, evidence identity, and exit state.

## Discriminating questions

- What are ELF class, endian, machine, type, build-ID and interpreter?
- Which PT_LOAD and dynamic segments exist?
- Do symbols, relocations, TLS and constructor init paths require deeper inspection?

## Ordered investigation phases

1. **Phase 1:** Hash and identify ELF class, endian, architecture, program/section headers and entry point using independent parsers.
2. **Phase 2:** Inventory PT_DYNAMIC/NEEDED/RPATH/RUNPATH, exported symbols, relocations, TLS and exception/unwind metadata when present.
3. **Phase 3:** Relate observed imports and executable permissions to the application context; treat strips and unusual entropy as clues only.
4. **Phase 4:** Determine if this SO is Android JNI by explicit provenance (APK split, Android ABI, JNI), not the `.so` suffix.
5. **Phase 5:** Use Ghidra/IDA/radare2 only as needed for data-flow/CFG evidence; dynamic instrumentation needs an authorized isolated runtime.

## Completion, failure and fallback

**Validated exit condition:** Scoped ELF capability map and native/Android routing with provenance.

**Failure diagnosis:**

- Missing section table is valid for many ELF files; use program headers.
- Wrong ABI leads to disassembler errors; re-check machine/endian.

**Alternative route:**

- Generic ELF spec analysis; native function emulation with a small reproducible environment.

## Minimum report fields

`target_hash`, `input_representation`, `platform`, `architecture`, `runtime_version`, `protection_hypotheses`, `evidence_ids`, `counter_evidence`, `tool/provider_versions`, `observation_timeline`, `failed_tests`, `validated_result`, `limitations`, `sources`, `next_step`.

Do not upgrade sample-scoped outcomes to canonical protector behavior. If dynamic prerequisites are missing, stop at an actionable plan and mark runtime claims `Needs verification`.
