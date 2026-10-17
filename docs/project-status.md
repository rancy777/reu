# Project Status

Version: **1.5.0 engineering candidate**. This page records scope and outstanding work; it is not a rating or certification.

| Area | Current evidence | Boundary |
| --- | --- | --- |
| Git baseline | Canonical private repository [rancy777/reu](https://github.com/rancy777/reu), formal branch `main`; local `main` tracks `origin/main` | Compare full local/remote SHAs after fetching; historical experiment records retain their original pre-Git provenance |
| Skill packaging | Standard name/description frontmatter; portable copy installer and dependency checks | Host discovery locations are documented; no claim that every agent host was exercised |
| Python runtime | Local Windows Python 3.11 tests, including official MCP SDK 2.3.0 against a harmless local fixture | No third-party reverse-engineering provider was connected |
| Automated regressions | 16 records form a strict offline gate | Covers deterministic policy and routing behavior |
| Research regressions | 8 separate records retain 5 PARTIAL and 3 MANUAL results | Not counted as fully automated acceptance |
| CI | [Remote Actions runs](https://github.com/rancy777/reu/actions/workflows/ci.yml?query=branch%3Amain): Windows/Ubuntu × Python 3.11–3.14; SDK fixture, wheel installs, committed-manifest gate, Windows native demo, artifacts and aggregate result | Results belong to each run's exact commit; a successful earlier run does not certify later changes |
| Target triage | Structural PE/DEX/ELF/package triage and documented investigation workflows | Triage and routing do not establish successful unpacking |
| VMP packing experiment | One [owned VMP 3.8.4 x64 reconstruction](cases/vmprotect-3.8.4-x64.md); 45 behavior and 14 structural checks passed | Known OEP and nine manually identified import-call repairs; no selected virtualized functions |
| VMP function-virtualization experiment | One [SDK-marked pure-function recovery](cases/vmprotect-3.8.4-virtualized-x64.md); 53 native instructions, 100,008 input checks and 128 protected-program comparisons | Separately source-built CLI harness; full-domain proof remains unknown. No arbitrary-program devirtualization or real-MCP compatibility claim |

Exact commands and run results are in [Verification](verification.md). Review [security notes](security-review.md) before enabling a provider, and [corpus status](../corpus/STATUS.md) before interpreting research coverage.

## Deferred work

- Broader authorized sample experiments, including input-dependent branches, non-pure virtualized functions and independently established entry points; the two scoped owned experiments do not cover them.
- Windows VM and Android runtime fixtures for those tool-specific workflows.
- Independent security assessment, if a deployment requires one.

These tasks need their own environments and acceptance evidence. The current offline gate does not stand in for them.

## Third-party provider scope

Use existing MCP providers according to their upstream setup and validation records. Repeating upstream provider validation is not a project release prerequisite or a scheduled task. The evidence table still distinguishes this project's native-tool experiments from its MCP SDK fixture; this policy does not add a new local compatibility result.
