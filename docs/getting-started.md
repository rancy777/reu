# Getting Started

There are two independent pieces: the **Skill** supplies instructions and references; the **runtime** supplies the `re-skill` CLI. Installing one does not install the other or any third-party analysis tool.

## Install the Skill

Requires Python 3.11+. From the downloaded source root:

```bash
python scripts/install_skill.py
```

This creates a self-contained copy at `~/.agents/skills/reverse-engineering-unpacking`, the [Codex user Skill location](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills). The destination name matches the Skill's frontmatter. No runtime dependencies, providers, or targets are launched.

The installer refuses an existing destination and never overwrites local edits. Review and remove an old copy yourself before reinstalling. Changes to the source do not update an installed copy automatically.

For another host's Skill directory, pass its full destination folder:

```bash
python scripts/install_skill.py --destination /path/to/skills/reverse-engineering-unpacking
```

Discovery behavior for other hosts must be checked against their documentation. Codex detects local Skill changes automatically; restart it if the entry does not appear. Invoke `$reverse-engineering-unpacking` in Codex CLI/IDE, or select the skill through the host's Skill picker.

Keep the complete installed directory. Its workflows, references, configuration templates, and runtime sources resolve relative to `SKILL.md`.

## Install runtime

Requires Python 3.11+. Create an isolated environment in the source root.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\re-skill.exe route --input runtime/examples/triage.sample.json
```

### Linux / macOS

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -e .
./.venv/bin/re-skill route --input runtime/examples/triage.sample.json
```

These commands do not require shell activation. The routing example consumes synthetic metadata and keeps the protection status `Unknown`.

For later commands, use the same environment's `re-skill` executable. An agent outside this project can invoke its absolute path. A host with its own connected MCP tools may use the Skill without installing this runtime.

## Inspect a file

Replace the example path with a file you are authorized to inspect:

```bash
re-skill triage --file ./sample.exe --route
re-skill system-probe
```

Triage hashes and inspects the file without executing it. The host probe checks PATH and Python module availability; it does not start analysis tools. Structural indicators are observations, not malware verdicts or proven protector identities.

## Configure an MCP provider

Install the optional SDK into the same Python environment:

```bash
python -m pip install -e '.[mcp]'
```

Copy `runtime/config/providers.ready-to-install.json` to `providers.json`. All template entries are disabled. Install and review a native tool and its provider separately, configure the real executable/arguments, review the registry entry, and explicitly enable the provider. See [Provider Setup](../integrations/PROVIDER-SETUP.md).

```bash
re-skill doctor --config ./providers.json
```

`doctor` is offline. Missing executables or blocked launchers return a nonzero status with a reason; fix the path/configuration before discovery. A template is not an installed provider.

```bash
re-skill discover --config ./providers.json --registry ./integrations/mcp-provider-registry.yaml --output discovery.json
```

Discovery launches enabled, registry-approved providers. Adapter planning and calls use live tools and schemas; see [Runtime](../runtime/README.md). Follow each provider's upstream setup instructions; repeating its validation is not a project release prerequisite. The separate [packing](cases/vmprotect-3.8.4-x64.md) and [function-virtualization](cases/vmprotect-3.8.4-virtualized-x64.md) experiments used native tools and do not establish a new local MCP compatibility result.

## Run offline acceptance

Install test dependencies in the environment, then run:

```bash
python -m pip install -e '.[test]'
python -m pytest -q runtime/tests -ra
re-skill regress --strict --file corpus/regression/automated.jsonl
```

The automated dataset contains 16 fully executable records. Research checks are separate:

```bash
re-skill regress --file corpus/regression/research.jsonl
re-skill regress --strict --file corpus/regression/research.jsonl
```

The research dataset retains 5 PARTIAL and 3 MANUAL results. Its strict run intentionally exits with code `2`. New research records enter that dataset and require review before entering automated acceptance.

For current run evidence, see [Verification](verification.md). For archive and wheel checks, see [Releasing](releasing.md).
