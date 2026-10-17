# Normalized Tool Contract

MCP provider APIs vary. The agent normalizes them into semantic operations.

## Operation families

### Target
- `target.identify`
- `target.open`
- `target.close`

### Static
- `static.metadata`
- `static.sections`
- `static.imports`
- `static.exports`
- `static.strings`
- `static.functions`
- `static.decompile`
- `static.xrefs`
- `static.callgraph`

### Runtime
- `runtime.attach`
- `runtime.spawn`
- `runtime.pause`
- `runtime.resume`
- `runtime.step`
- `runtime.modules`
- `runtime.threads`
- `runtime.registers`
- `runtime.memory-read`
- `runtime.memory-search`
- `runtime.trace`

### Reconstruction
- `reconstruct.capture`
- `reconstruct.dump`
- `reconstruct.imports`
- `reconstruct.validate`

### Android
- `android.device`
- `android.package`
- `android.splits`
- `android.dex-inventory`
- `android.class-search`
- `android.decompile`
- `android.logcat`
- `android.runtime-modules`
- `android.native-jni`

### Emulation
- `emulator.load`
- `emulator.run`
- `emulator.break`
- `emulator.memory`
- `emulator.trace`

### Evidence
- `evidence.capture`
- `evidence.export`
- `evidence.hash`

## Contract

Each provider adapter should map its native MCP tool to:

```yaml
operation:
provider:
native_tool:
target:
representation:
inputs:
outputs:
status:
side_effects:
version:
raw_output_ref:
normalized_observation:
```

## Side-effect classes

- `read`
- `observe`
- `execute`
- `mutate`
- `destructive`

The agent should prefer the lowest side-effect class that can answer the question.

## Completeness

A normalized result must say whether output is:
- complete
- truncated
- paginated
- sampled
- error
- unknown

This prevents partial MCP responses from being mistaken for complete target state.
