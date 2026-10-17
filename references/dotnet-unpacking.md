# .NET Analysis

## Classification
Distinguish:
- .NET Framework / CLR metadata
- modern .NET
- ReadyToRun
- NativeAOT
- mixed managed/native
- single-file/self-contained
- obfuscation/packing

CLR presence does not imply a normal JIT-only execution path.

## Evidence
Look for CLR metadata, managed streams, assembly references, runtime version clues, native code regions, R2R/native images, resources, embedded payloads.

## Workflow
1. identify managed/native composition
2. inspect metadata/IL
3. determine runtime/deployment model
4. identify obfuscation/packing hypotheses
5. observe JIT/runtime only if necessary
6. reconstruct or extract managed artifacts when that is the research goal
7. validate by loading/executing in an authorized environment

## NativeAOT
Treat as native-first when evidence supports NativeAOT. Do not force a managed decompilation workflow onto native code.
