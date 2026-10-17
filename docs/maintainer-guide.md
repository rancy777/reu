# Maintainer Guide

## Adding a new MCP provider

1. Add it to `integrations/mcp-upstream-catalog.yaml`.
2. Add a reviewed execution entry to `integrations/mcp-provider-registry.yaml`.
3. Record native tool and provider identities separately.
4. Record transport, versions, license, and observed requirements.
5. Add a provider adapter profile only for stable, observed tool names.
6. Add a security note and a regression fixture.
7. Do not count two wrappers around the same native engine as independent evidence.

## Adding a new research claim

Use an Evidence Card and record:

- platform;
- file type;
- architecture;
- protector/packer and version if known;
- prerequisites;
- observation;
- source;
- source date;
- scope;
- limitations;
- confidence.

A source may support a claim without being strong enough to promote that claim to canonical knowledge.

## Promotion rule

Canonical knowledge requires provenance, scope, and validation. The system must preserve disagreement and uncertainty rather than overwriting them.

## Release checklist

- [ ] `python -m pytest -q runtime/tests -ra` on the supported CI matrix
- [ ] `re-skill regress --strict --file corpus/regression/automated.jsonl` passes
- [ ] Research regressions remain separately reported; PARTIAL/MANUAL are not marked PASS
- [ ] Skill metadata and installed references pass the installation tests
- [ ] Clean wheel installation passes `scripts/check_install.py`
- [ ] provider registry contains no accidental secrets or private endpoints
- [ ] source links are reachable or explicitly marked unavailable
- [ ] versions are recorded where version-sensitive
- [ ] README claims match [Verification](verification.md) and [Project Status](project-status.md)
- [ ] `scripts/release.py` build and verify pass
- [ ] archive contains no executable samples, symlinks, credentials, or build caches

See [Releasing](releasing.md) for exact packaging commands and authorization boundaries.
