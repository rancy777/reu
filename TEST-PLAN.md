# Test and Acceptance Plan

## A. Offline (run now)

1. Compile all Python files; inspect JSON, YAML and JSONL syntax.
2. File triage harmless synthesized PE32+ (native / CLR metadata) / ELF / DEX / APK / AAB.
3. Real stdio process launch of **harmless local MCP mock**, protocol initialize, tools/list pagination, tool invocation and raw observation capture.
4. Refuse fake `readOnlyHint` on `writeMemory`, `startHook`; refuse HTTP no-TLS remote; validate actual tool JSON Schema.
5. Verify case duplicate rejection, graph referential integrity, compatibility scope and no automatic knowledge promotion.
6. Run deterministic regression subset and explicitly surface remaining manual assertions.
7. Root `re-skill --help`, standard Skill metadata, safe local Skill installation, clean wheel installation, ZIP SHA-256 integrity and no bundled secrets/binaries.

## B. Real host (not run now; future acceptance checklist)

- Windows VM: IDA GUI/headless, x64dbg and WinDbg connected; verify tool schema drift, architecture, sandbox, process lifecycle, output sizes and crash recovery.
- Linux VM: radare2, Ghidra, REMnux/PE-sieve variants; verify stdio/Streamable-HTTP, auth and tool isolation.
- Android emulator/authorized device: ADB, JADX, Frida, Unidbg MCP; verify API level/ABI/runtime, test safe fixture, handle crash/no-process state and legacy SSE compatibility.
- Protectors: independently authored/authorized UnPackMe/CrackMe with known ground truth; record sample hash, exact protector version/config, repeated runs and fail states.
- Repeat cross-platform vendor-specific MCP tests on approved, pinned versions. No claim of end-to-end readiness until these pass.

## Release-blocking criteria

- All offline code and corpus schema tests pass. Base environments may skip the two SDK-specific tests; the separate SDK fixture job must run them successfully. Real-provider cases remain deferred and are not represented by these fixtures.
- The 16-record automated regression dataset passes strict mode; the 8-record research dataset remains separately reported.
- No malformed JSONL, missing schema or broken install artifacts.
- Side-effect tool blocked by default and authorization requires explicit distinct flags.
- No invented runtime compatibility or sample-specific protector version.
- ZIP tested and SHA256 recorded in external verification report.
