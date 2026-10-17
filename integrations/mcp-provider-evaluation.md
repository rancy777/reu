# MCP Provider Evaluation Protocol

## Why this exists

GitHub contains many reverse-engineering MCP implementations. The Skill must not equate "exists on GitHub" with "safe, correct, maintained, or interchangeable."

Evaluate each provider on six axes:

| Axis | Question |
|---|---|
| Provenance | Is it vendor/first-party, established community, or unknown? |
| Maintenance | Are commits/releases/issues active and coherent? |
| Security | Is there a SECURITY.md, published advisory history, auth, path confinement, and safe transport? |
| Determinism | Can it run headless/stdio and produce structured output? |
| Scope | Does it expose the minimum capability needed or a dangerous super-set? |
| Reproducibility | Can the native tool + MCP provider versions be pinned and replayed? |

### Provider score is not truth

A provider may score highly and still produce an incorrect analysis. Tool output is evidence, not ground truth.

## Default acceptance gates

A provider can enter `recommended` only if:
- repository is identifiable and source is available;
- license is visible;
- installation prerequisites are explicit;
- transport security is understood;
- target workspace boundaries are known;
- health check can be performed without mutating the target;
- version/commit can be recorded;
- at least one regression fixture can exercise the advertised capability.

If a gate is unknown, status is `candidate`, not `recommended`.

## Security gate

Block or quarantine a provider when:
- a known critical advisory is unresolved or cannot be mapped to a fixed release;
- it exposes unauthenticated non-loopback control of a debugger/device;
- it can access arbitrary host paths outside the analysis workspace;
- it mixes prompt content with privileged host instructions without trust boundaries;
- installation pulls mutable code without a pin and no integrity verification is possible.

## Overlap rule

If provider A wraps provider B's engine:
- A + B are not independent evidence modalities.
- Use A for orchestration and B for direct validation, but do not count them as independent corroboration.

Examples:
- Reversecore's Radare2 result + radare2 MCP result = one Radare2 modality.
- MobSF's Frida result + direct Frida result = one Frida modality.
- JADX MCP + direct JADX CLI = one JADX modality.

## Version record

Always store:

```yaml
provider:
provider_version:
provider_commit:
native_tool:
native_tool_version:
host_os:
host_arch:
target_arch:
runtime:
transport:
```

Unknown fields stay `Unknown`; never infer them.
