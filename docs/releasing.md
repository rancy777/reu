# Releasing

A source archive or wheel produced locally is a validation artifact until it has a committed, traceable source state and an authorized release.

## Offline gate

From an isolated Python 3.11+ environment:

```bash
python -m pip install -e '.[test,mcp]' build
python -m pytest -q runtime/tests -ra
re-skill regress --strict --file corpus/regression/automated.jsonl
```

This includes a harmless local MCP fixture through the official SDK. It does not connect to third-party reverse-engineering providers. The 8 research records remain separately reported, not promoted by a green offline gate.

## Wheel

Use an empty output directory outside the source tree:

```bash
python -m build --wheel --outdir /path/to/output/wheels
python scripts/check_install.py --wheel-dir /path/to/output/wheels
```

The checker requires exactly one wheel, creates a clean environment, installs the wheel with its declared dependencies, checks packaged schemas/version, and runs the CLI from outside the checkout. It installs no providers and executes no target.

## Source archive

Use an output path outside the checkout:

```bash
python scripts/release.py --root . --zip /path/to/output/reverse-engineering-unpacking-1.5.0.zip
python scripts/release.py --root . --verify --zip /path/to/output/reverse-engineering-unpacking-1.5.0.zip
```

The build refreshes `MANIFEST.json` and emits the archive's SHA-256 sidecar. Verify file inventory, hashes, CRCs, path containment, and member contents. No target binaries, credentials, symlinks, or local runtime artifacts belong in the archive.

Refresh and commit the manifest together with source changes. CI verifies the committed manifest before generating a new archive. Keep archives and their `.sha256` sidecars outside the checkout; these are outputs rather than source inputs. Experiment files under `examples/` retain exact bytes across platforms so recorded evidence hashes remain valid.

## GitHub workflows

[CI](../.github/workflows/ci.yml) configures Windows/Ubuntu Python 3.11–3.14 tests, a strict automated regression gate, official-SDK fixture checks, clean wheel installation, committed-source integrity checks, and a Windows public-IR native demo rebuild. It can also run manually. The final `CI passed` job requires every preceding job to succeed.

Successful CI runs retain the verified source archive/checksum, wheels and native-demo JSON evidence for 14 days as Actions artifacts. These are CI outputs associated with the run's exact source commit; they are not an automatic GitHub Release. Third-party actions are pinned to full commit SHAs and tracked by Dependabot.

[Release](../.github/workflows/release.yml) calls the complete CI workflow and waits for its jobs before publishing a tag. It requires the tag to equal `v` plus the package version, builds outside the checkout, checks source and wheel integrity, and rejects tracked-file changes. The default token has read-only repository access; only the publication job receives write access. Keep case-specific scope in release notes. Repeating third-party provider validation is not a release prerequisite.

Publishing requires separate authorization. Before publishing, record the canonical repository/ref, full source SHA, clean working state, commands, configuration, output paths, hashes, and actual CI results. Inspect the current checkout with `git remote -v`, `git branch --show-current`, `git rev-parse HEAD`, and `git status --short`. A local initial commit becomes a formal remote baseline only after the intended remote/ref is confirmed and synchronized; do not label local configuration checks as a successful remote Actions run.
