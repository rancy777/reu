# Changelog

## Unreleased

- Strengthened CI with pinned action SHAs, committed-manifest checks, a Windows native-demo rebuild, verified build artifacts, job timeouts and a required aggregate result.
- Fixed Release output placement and tag/version matching; preserved byte-identified experiment files across Git checkouts.
- Added a fresh-directory native demo rebuild from the published recovered IR, with an isolated EXE behavior check; clarified that it does not perform a new devirtualization or protected-program comparison.
- Added a visible native-tool result and a bilingual FAQ; corrected full-experiment working-directory instructions and a stale validation-status statement.
- Added standard Skill frontmatter and a portable local installer that preserves existing installations.
- Documented separate Skill registration and runtime installation, with isolated Windows/Linux commands and explicit host-discovery scope.
- Added Windows/Ubuntu CI across Python 3.11–3.14, official-SDK local fixture checks, and clean wheel-install acceptance.
- Split the original 24 regression records into 16 automated and 8 research records without changing their assertions; strict CI gates the automated dataset.
- Reject empty regression datasets and duplicate IDs.
- Restrict wheel package discovery to `re_skill`; exclude local provider configuration, discovery output, and runtime artifacts from source/Skill packaging.
- Replaced scored self-reviews and release claims with [project status](docs/project-status.md), [verification records](docs/verification.md), [security review notes](docs/security-review.md), and [release instructions](docs/releasing.md).
- Refined the bilingual README with theme-aware branding, actual CLI routing excerpts, and a mobile layout.
- Added an owned VMProtect 3.8.4 x64 default-packing case with C++ sources, real tool screenshots, 45 behavior checks and 14 structural checks; its known-OEP and manual import-repair scope is explicit.
- Added one SDK-marked VMProtect 3.8.4 pure-function semantic reconstruction with real x64dbg trace, Triton replay, 53 native instructions, 100,008 input checks and screenshots. CLI harness source was rebuilt separately; a full-domain SMT attempt timed out.
- Real third-party MCP providers, arbitrary-program devirtualization and broader protected-sample coverage remain unverified.

## 1.5.0 — 2026-10-16 — engineering candidate

- Added reviewed provider-startup policy, registry checks, separate operation authorization gates, schema/response limits, and output redaction.
- Added single-host corpus locking, ID deduplication, path checks, graph-repair diagnostics, and version-scoped compatibility checks.
- Expanded platform workflows and deterministic regression checks.
- Added Python packaging, source manifests, GitHub workflows, documentation, contribution/security policies, and visual assets.
- Earlier local offline run recorded 67 passed and 1 skipped. That result did not establish real-provider compatibility; see [current verification](docs/verification.md).

## 1.4.0 — 2026-10-16 — initial local executable baseline

- Added stdio protocol fixtures, provider discovery, normalized observations, file triage, corpus schema, evidence graph, and wheel packaging.
- Earlier offline run recorded 34 passed and 1 skipped.

## 1.3.0 — initial runtime baseline

- Added the first Python tool plane, discovered provider contracts, and research data planes.
