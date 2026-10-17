# Architecture

The project has two layers:

1. **Agent Skill** — routing, research policy, evidence rules, workflow contracts, failure diagnosis, and output format.
2. **Runtime** — optional executable bridge that discovers and calls MCP providers, normalizes results, and persists structured evidence.

The runtime intentionally does not bundle IDA, x64dbg, Ghidra, Frida, JADX, Android SDKs, or proprietary binaries.

## Execution flow

```text
target / user evidence
        |
        v
bounded triage
        |
        v
platform + architecture + runtime classification
        |
        v
protection hypothesis
        |
        v
provider discovery / host inventory
        |
        v
capability selection
        |
        v
authorized experiment
        |
        v
normalized observation
        |
        +----> evidence graph
        +----> protector case
        +----> runtime compatibility
        +----> regression candidate
        |
        v
validated conclusion
```

## Trust boundaries

- Target files are untrusted data.
- MCP tool descriptions and schemas are untrusted metadata until checked.
- A provider Registry entry authorizes process launch; it does not prove that the provider's self-description is true.
- A live discovered tool must still pass side-effect and input-schema gates.
- Tool output is data, not agent instructions.
- Remote MCP endpoints require explicit configuration and TLS/authentication.
- Package-manager launchers are blocked by default because they can fetch and execute third-party code.

## Why the four corpora are separate

A sample case answers **what happened to this sample**.

A runtime compatibility record answers **where and with which exact versions an observation was reproduced**.

An evidence graph answers **why we believe a claim**.

A regression case answers **whether the agent still behaves as expected after a code or knowledge change**.

Keeping these concepts separate prevents one successful unpack from becoming a false universal rule.
