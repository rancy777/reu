# Local Verification Record

Date: **2026-10-16**. Version: **1.5.0 engineering candidate**.

These results describe local engineering checks from **2026-10-16**. The later [owned VMProtect 3.8.4 x64 packing case](cases/vmprotect-3.8.4-x64.md) and [pure-function virtualization case](cases/vmprotect-3.8.4-virtualized-x64.md), recorded on **2026-10-17**, each have their own native-tool evidence and scope. Real-provider compatibility remains unverified. This is not an independent assessment or a production release.

## Source and environment

- Source directory: `D:\Reu`.
- Repository / branch / full HEAD / formal remote baseline: unavailable; this source directory has no `.git`.
- Working state: locally modified source, used only for temporary validation.
- Host: Windows, Python 3.11.9.
- Isolated environment: `C:\Users\lenvon\AppData\Local\Temp\reu-onboarding-8ed4e16ce45c4f02b1e325639f1de5f5\venv`.
- Declared test extra and official MCP SDK **2.3.0** installed in that environment.
- No proprietary analysis software, third-party MCP provider, device, or protected sample was exercised.

## Checks

| Check | Result | Meaning |
| --- | --- | --- |
| Python tests with official SDK | **74 passed** | Offline policy, triage, storage, Skill installation, and local mock protocol tests |
| Python tests without SDK (clean wheel environment) | **72 passed / 2 skipped** | Only the two SDK-specific tests skip |
| Strict automated regressions | **16 PASS; exit 0** | 16 fully executable records; no manual assertions removed |
| Research regressions | 5 PARTIAL / 3 MANUAL; strict exits 2 | Retains unverified research assertions |
| Official SDK fixture | PASS | Real SDK connects to a harmless local protocol mock; not a real RE provider |
| Skill format | **PASS** | Required metadata and installed folder name |
| Fresh wheel installation | **PASS** | Version, seven schemas, console entry point, and routing outside the source tree |
| Source archive / manifest | **PASS** | File inventory, member bytes, hashes, and archive integrity |
| Workflow static validation | **PASS, actionlint 1.7.12** | CI and release YAML checked locally |
| GitHub Actions | Configured, not run remotely | Windows/Ubuntu matrix and packaging jobs need an actual repository run |

## Reproduce

From the source root in an isolated Python environment:

```bash
python -m pip install -e '.[test,mcp]' build
python -m pytest -q runtime/tests -ra
re-skill regress --strict --file corpus/regression/automated.jsonl
re-skill regress --file corpus/regression/research.jsonl
re-skill regress --strict --file corpus/regression/research.jsonl
```

The last command must return `2` while the research assertions remain unverified. CI gates the automated dataset and separately tests the research status; it does not label all research as passed.

Skill-copy and wheel commands:

```bash
python scripts/install_skill.py --destination /path/to/test/skills/reverse-engineering-unpacking
python -m build --wheel --outdir /path/to/test/wheels
python scripts/check_install.py --wheel-dir /path/to/test/wheels
```

See [Releasing](releasing.md) for source archive commands. Local artifacts are kept outside the source tree under the temporary validation directory. No commit, push, merge, deployment, tag, or GitHub release was performed.

## Temporary build artifacts

All artifacts are local validation outputs, not published releases.

- Wheel source: `C:/Users/lenvon/AppData/Local/Temp/reu-onboarding-8ed4e16ce45c4f02b1e325639f1de5f5/source-check/reverse-engineering-unpacking`, a complete source copy made by the Skill installer. The runtime sources and packaging configuration match `D:/Reu`.
- Wheel build: isolated Python 3.11, `python -m build --wheel --outdir C:/Users/lenvon/AppData/Local/Temp/reu-onboarding-8ed4e16ce45c4f02b1e325639f1de5f5/clean-wheels`.
- Wheel output: `clean-wheels/reverse_engineering_unpacking_runtime-1.5.0-py3-none-any.whl` under the temporary validation directory.
- Source archive source: `D:/Reu`; command: `python scripts/release.py --root . --zip C:/Users/lenvon/AppData/Local/Temp/reu-onboarding-8ed4e16ce45c4f02b1e325639f1de5f5/reverse-engineering-unpacking-validation.zip`, followed by the same command with `--verify`.
- Source archive output and SHA-256 sidecar: `reverse-engineering-unpacking-validation.zip` and `.zip.sha256` under the temporary validation directory.
- Build configuration: runtime-only wheel package, seven JSON schemas, no bundled native tools. Source inventory excludes caches, local provider/discovery configuration, runtime output, and local Skill installations.
- Branch / HEAD / formal baseline: unavailable for both source locations; these are uncommitted local validation states. A formal release still requires committed provenance and separate publication authorization.

## Coverage boundaries

The local mock supplies deterministic function lists and pseudocode. It proves SDK transport/client plumbing only. The seed corpus still contains zero measured third-party tool compatibility observations.

Linux and other Python versions are configured in CI, not claimed as locally tested. See [Project Status](project-status.md) for deferred work, and [Security Review Notes](security-review.md) for historical findings and remaining trust boundaries.

## 2026-10-17: virtualized pure-function follow-up

A separate [VMProtect 3.8.4 SDK-marked function experiment](cases/vmprotect-3.8.4-virtualized-x64.md) recorded 21,849 native trace instructions, recovered a symbolic expression, compiled 53 standalone x64 instructions, and passed 100,008 input checks, 128 protected-program comparisons and 45 isolated harness checks. A mutated native constant was rejected. Source/IR rebuilds were byte-identical. A 120-second full-domain SMT attempt returned unknown; there is no exhaustive-equivalence or whole-program recovery claim. The runtime test suite counts above are a separate historical record.

## 2026-10-17: public native demo rebuild

The [demo rebuild script](../examples/vmprotect-3.8.4-virtualized-x64/source/rebuild_demo.ps1) was run from `D:/Reu` with a fresh output directory containing spaces. It created a new Python 3.11 x64 environment, installed llvmlite 0.50.0, compiled the published recovered IR and linked the CLI harness. The renamed EXE alone passed **45/45 behavior checks**. DLL and EXE hashes matched the accepted recovery. A second invocation against the same directory was rejected without changing the accepted outputs. [Command, source identity, output paths, hashes and result](../examples/vmprotect-3.8.4-virtualized-x64/evidence/native-demo-check.json).

This checks the public compilation path; it does not repeat trace recovery, the 100,008 native input checks, or the 128 protected-program comparisons. No proprietary SDK or VMProtect installation is required for this demo.

## 2026-10-17: Git bootstrap and CI preparation

Git was initialized in `D:/Reu` on `main` after the earlier experiments. Their historical records correctly retain their original absence of Git provenance. The initial snapshot excludes proprietary SDK files, target binaries, caches, environments and runtime artifacts. Canonical remote/ref selection remains pending; no remote Actions result is claimed here.

A fresh Python 3.11 environment at `runtime-artifacts/github-baseline-20261017/venv`, created without system site packages, installed `.[test,mcp]` and `build`. It passed **74 tests**, **16 strict automated regression records**, wheel building and isolated wheel installation. An earlier attempt using an old environment failed two SDK tests because it inherited system MCP 1.27.2; the clean environment installed the declared MCP 2.3.0 dependency. This is an environment correction, not a compatibility fallback or a new third-party provider test.

Both workflow files passed **actionlint 1.7.12** after checksum verification of the official release. The workflows now verify the committed manifest before rebuilding, place source ZIPs/checksums outside the checkout, pin third-party actions, enforce tag/version agreement and collect CI artifacts. The Windows public-IR demo is part of CI. Exact experiment bytes under `examples/` are preserved through Git attributes; ordinary source/doc line endings use LF.

The source builder now emits LF-only manifest/checksum files on every platform. Two added release regressions check deterministic archives, byte-identical CRLF evidence, and rejection of stale source manifests. After these additions, the full fresh-environment suite passed **76 tests**.

The initial local commit was `6944c3f20eca4ac18bf613d9279196e33a0fa289`. A separate clone passed manifest verification, but its full suite exposed a Windows first-lock race: one of 12 concurrent writers could attempt the initialization-byte write after another writer acquired the lock. That initial commit is not recorded as accepted. The initialization write was removed because Windows permits locking beyond EOF; no compatibility fallback was added. The concurrency test now starts 12 writers together across eight fresh-file rounds. After the fix, the full suite again passed **76 tests**. The fix is a subsequent commit, preserving the initial history.

## 2026-10-17: formal GitHub baseline and remote CI

The canonical repository is [rancy777/reu](https://github.com/rancy777/reu), created **private** at the owner's request. The formal branch is `main`; local `main` tracks `origin/main`. Historical pre-Git experiment receipts are retained as historical records, rather than rewritten to imply they originated from a later commit.

The [first remote run](https://github.com/rancy777/reu/actions/runs/39010362150), on `1bfe888f589bb6d9b478efaa144d704866118c0f`, passed the eight OS/Python test jobs, SDK fixture jobs, wheel installations and Windows native demo. Its source-integrity job failed because Windows and Linux `Path` ordering placed mixed-case paths differently; the final aggregate correctly failed as well.

Source inventory and ZIP entry ordering were changed to explicit POSIX-string order, with a mixed-case-path regression. The local full suite then passed **77 tests**. The [subsequent remote run](https://github.com/rancy777/reu/actions/runs/39010541785), on **`9e76034f4d6727fef4543c6645dca81637050572`**, completed with **all 15 jobs successful**: Windows/Ubuntu × Python 3.11–3.14, two SDK fixture jobs, two clean wheel installations, source integrity, the Windows public-IR native demo, and `CI passed`.

These runs verify this project's CI and protocol fixtures, not a third-party debugger MCP provider. The native demo rebuilds recorded IR and validates its harness; it does not perform a new protected-program recovery. Later commits must retain their own passing CI result. Pushing this private repository did not create a release tag, publish a GitHub Release, deploy software or change repository visibility.
