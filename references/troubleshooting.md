# Troubleshooting / Failure Diagnosis

## Failure taxonomy

1. Target failure
2. Environment failure
3. Tool failure
4. MCP provider failure
5. Version/compatibility failure
6. Timing/state failure
7. Evidence insufficiency
8. Hypothesis failure

## "Dumped PE does not start"

Check, in order:
- target identity/hash;
- PE header/architecture;
- section virtual/raw mapping;
- import table/IAT reconstruction;
- relocations;
- TLS callbacks;
- Load Config;
- exception/unwind metadata;
- capture state/timing;
- runtime-generated/decrypted code still required;
- self-integrity;
- external runtime dependencies.

Do not conclude that OEP identification proves reconstruction completeness.

## "Debugger attach crashes target"

Competing hypotheses:
- anti-debugging;
- provider/debugger incompatibility;
- wrong architecture;
- instrumentation timing;
- target instability;
- missing runtime dependency;
- integrity/self-check.

Discriminate using a controlled fixture, alternate debugger/provider, and non-invasive observations.

## "Frida attach crashes app"

Check:
- client/server version;
- ABI;
- Android API/ART;
- spawn vs attach;
- hook timing;
- native crash;
- integrity checks;
- anti-instrumentation evidence.

Do not label it anti-Frida without evidence.

## "No DEX on disk"

Check:
- APK/AAB/split inventory;
- encrypted/compressed assets;
- ClassLoader activity;
- runtime-loaded DEX;
- memory mappings;
- ART state.

Absence from the original package is not proof of absence at runtime.

## "Tool says protector X"

Treat as a hypothesis.
Cross-check:
- signature source/version;
- section layout;
- imports;
- runtime behavior;
- independent cases.

## MCP-specific failure

If tool exists but call fails:
1. inspect provider health;
2. verify native tool/session;
3. inspect schema mismatch;
4. check version;
5. try fallback provider;
6. record provider failure separately from target failure.

Never blame the sample for an MCP transport/schema failure.
