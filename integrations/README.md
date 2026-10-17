# MCP Integration Layer

This directory defines how the Skill discovers, evaluates, binds, and safely uses existing reverse-engineering MCP providers.

## Important design decision

The Skill **does not vendor or silently download third-party MCP servers**.

Instead it:
1. discovers MCP servers already installed in the host;
2. maps their advertised tools to semantic capabilities;
3. evaluates provenance/security/compatibility;
4. selects a provider;
5. runs health checks;
6. records provider/native-tool versions;
7. normalizes outputs into evidence;
8. keeps upstream references and version pins for reproducibility.

This lets users install the tools they actually want while the Skill remains maintainable.

## Preferred upstream strategy

Use existing upstream MCP implementations when they are mature enough:

- IDA → official Hex-Rays IDA MCP.
- radare2 → radareorg/radare2-mcp.
- x64dbg → maintained community provider after health/security check.
- WinDbg → DbgEng/WinDbg MCP after local health check.
- Ghidra → pinned community provider.
- Binary Ninja → pinned community provider.
- Frida → narrow typed provider; mobile-specific provider when device operations are needed.
- JADX → JADX-AI-MCP + JADX-MCP-Server.
- Apktool → maintained provider with security-version gate.
- APKiD → APKiDSkills `apkid-mcp` for Android packer/protector triage.
- Unidbg → project MCP debugger/custom-tool mode.
- REMnux → isolated malware-analysis execution backend.
- Broad aggregators → optional convenience layer, never an independent evidence modality for tools they merely wrap.

## Native CLI fallback

Do **not** force an MCP wrapper for every command-line utility.

For DIE, PE-bear, PEStudio, FLOSS, capa, YARA, Scylla, PE-sieve, pefile/LIEF scripts, adb, bundletool, baksmali/smali and similar tools, a constrained `artifact.exec` provider is often more reproducible than a thin third-party MCP wrapper.

## Provider classes

- **Official** — vendor publishes the MCP.
- **First-party project** — native project ecosystem publishes the MCP.
- **Community** — independent implementation.
- **Aggregator** — combines multiple native tools.
- **Generic** — shell/filesystem bridge.

## Provider acceptance

A provider is not accepted merely because its repository exists.

See:
- `mcp-upstream-catalog.yaml`
- `mcp-provider-evaluation.md`
- `mcp-installation-policy.md`
- `discovery-and-binding.md`
- `health-check.md`
- `security-policy.md`

## Evidence rule

MCP output is **Tool Evidence / Observation**.

If two MCPs wrap the same engine, they are not independent corroboration.

Example:
`Reversecore → Radare2` + `radare2-mcp → Radare2` = one Radare2 evidence modality.
