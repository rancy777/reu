# Runtime Compatibility Engine

Compatibility is an observed relation, not a permanent property.

Dimensions:
- host OS
- architecture/ABI
- native tool version
- MCP provider/version
- debugger backend
- runtime (CLR/ART/etc.)
- Android API
- device/emulator
- target/protector version

## States

- compatible
- partially-compatible
- incompatible
- unknown
- needs-verification

## Recording rule

A compatibility claim must include:
- exact conditions;
- observed capability;
- observed result/failure;
- evidence IDs;
- date;
- source if externally documented.

Do not infer compatibility from:
- similar version numbers;
- a successful install;
- a successful unrelated sample;
- provider marketing text alone.

## Upgrade handling

When a tool/provider/runtime changes:
- do not mutate old records;
- create a new compatibility observation;
- compare results;
- mark the old record superseded only if evidence shows it is no longer applicable.
