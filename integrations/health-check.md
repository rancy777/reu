# MCP / Tool Health Check

## Required output

```yaml
provider:
native_tool:
provider_version:
native_tool_version:
host_os:
architecture:
transport:
session:
status: healthy|degraded|unavailable
capabilities:
  - capability_id
checks:
  - name:
    status:
    observation:
    evidence_id:
```

## Generic checks

1. provider responds to initialization;
2. target file/session can be identified;
3. native tool executable/plugin can be identified;
4. architecture is known;
5. read-only probe succeeds;
6. output schema is stable enough to normalize;
7. timeouts are bounded;
8. logs/errors are retrievable;
9. local-only endpoint is used when remote access is unnecessary.

## Static-analysis checks

- open fixture
- identify format
- identify architecture
- enumerate sections/segments
- enumerate functions or symbols
- decompile one known function if supported

## Debugger checks

- identify debugger version
- identify target architecture
- create/attach to an authorized harmless fixture
- read registers or process metadata
- read a known memory region
- verify pause/resume semantics
- verify session survives a normal exception/stop event

## Android checks

- `adb` sees intended device/emulator
- API level and ABI are recorded
- package manager query works
- app/process identity is confirmed
- log collection works
- Frida device/session identity matches target
- Frida client/server versions are recorded
- no assumption of root is made

## Failure interpretation

- provider unavailable → use fallback provider
- native tool unavailable → install/fix native tool
- schema mismatch → provider adapter issue
- architecture mismatch → target/provider mismatch
- permission denied → authorization/environment issue
- target crash → not automatically anti-analysis
- timeout → distinguish target hang, provider hang, debugger state, and tool timeout

Health checks must produce evidence, not just "OK".
