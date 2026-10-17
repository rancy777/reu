# Contributing

Contributions are welcome, especially reproducible research and provider integrations.

## Development

```bash
python -m pip install -e '.[test]'
python -m pytest -q runtime/tests -ra
```

Optional MCP integration tests:

```bash
python -m pip install -e '.[mcp,test]'
python -m pytest -q runtime/tests -ra
```

The test suite must never require a commercial protected sample, a live Android device, or a proprietary debugger license.

## Research contributions

New reverse-engineering claims should include:

1. exact target platform and architecture;
2. tool and tool version;
3. protector/packer/obfuscator and version when known;
4. environment details;
5. observations and expected observations;
6. source provenance;
7. applicable scope and known limitations;
8. whether the result is sample-specific, version-specific, or independently reproduced.

A forum post can be valuable evidence, but it is not automatically canonical knowledge.

## MCP provider contributions

Provider additions should include:

- upstream repository;
- license;
- provider/native-tool distinction;
- transport;
- discovered capability examples;
- minimum/observed versions;
- security review notes;
- whether the provider is official, community, aggregator, experimental, or quarantined;
- a regression fixture where practical.

Never add credentials, private endpoints, proprietary binaries, or executable samples to the repository.

## Pull requests

Keep changes focused. Update `CHANGELOG.md` for user-visible behavior, provider policy, schema, or workflow changes. Run the full test suite and release verification before requesting review.

## Offline acceptance and packaging

Run `re-skill regress --strict --file corpus/regression/automated.jsonl`. Keep research results from `corpus/regression/research.jsonl` separate; its strict run currently returns 2. Changes to acceptance scope must preserve and explain existing assertions.

Skill installation is covered by `runtime/tests/test_installation.py`; fresh wheel installation is checked by `python scripts/check_install.py --wheel-dir /path/to/wheels`. See [Releasing](docs/releasing.md) and [Verification](docs/verification.md).

After changing source, configuration, documentation or assets, refresh `MANIFEST.json` before committing:

```bash
python scripts/release.py --root . --zip /path/outside/the/checkout/reu-source.zip
python scripts/release.py --root . --verify
```

CI checks the committed manifest before rebuilding it, so a stale inventory or digest fails. Keep build outputs outside the source tree or in ignored `runtime-artifacts/`. Case files under `examples/` preserve exact bytes through `.gitattributes`; avoid changing line endings in hashed source, traces or recovered IR. Record intentional evidence changes with their new identities.
