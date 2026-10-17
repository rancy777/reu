# MCP Provider Regression Cases

## Goal

Verify that provider upgrades do not silently change capability bindings, evidence semantics, or security posture.

| Case | Setup | Expected |
|---|---|---|
| MCP-001 | IDA official installed | binds `pe.static` and reports IDA/MCP versions |
| MCP-002 | x64dbg provider installed with x64 target | binds `pe.runtime`; architecture matches |
| MCP-003 | x64dbg provider installed with x86 target | binds x32 debugger path or reports missing x86 capability |
| MCP-004 | WinDbg 32-bit worker absent | native analysis may work; .NET/SOS limitation explicitly reported |
| MCP-005 | JADX plugin/server mismatch | health check fails; no silent binding |
| MCP-006 | Apktool MCP <=3.0.0 | provider quarantined |
| MCP-007 | APKiD installed | Android packer/protector scan returns structured evidence envelope |
| MCP-008 | Frida provider has no device | runtime binding reports missing target, no invented result |
| MCP-009 | aggregator + direct engine both enabled | outputs marked same-modality; no false corroboration |
| MCP-010 | provider has unresolved critical advisory | automatic selection blocked |
| MCP-011 | provider HTTP bound to non-loopback without auth | security gate fails |
| MCP-012 | provider upgrade changes tool schema | re-run health + affected regression cases before promotion |

## Promotion gate

A provider may move from candidate to recommended only when all applicable cases pass and the version/commit is recorded.
