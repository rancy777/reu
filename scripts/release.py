#!/usr/bin/env python3
"""Deterministic source ZIP/manifest builder; never runs target binaries.

Run from a reviewed source checkout:
  python scripts/release.py --root . --zip /path/to/reverse-engineering-unpacking-v1.5.0.zip
  python scripts/release.py --verify --root . --zip /path/to/...
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import tomllib
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ARCHIVE_ROOT = "reverse-engineering-unpacking"
EXCLUDE_DIRS = {
    "__pycache__", ".pytest_cache", "build", "dist", ".git", ".venv",
    "venv", "node_modules", "Protector", ".mypy_cache", ".ruff_cache", ".agents", "runtime-artifacts",
}
EXCLUDE_SUFFIXES = {".pyc", ".pyo", ".whl", ".zip"}
ALLOWED_TEXT_SUFFIXES = {
    ".md", ".py", ".toml", ".yaml", ".yml", ".json", ".jsonl", ".txt",
    ".ini", ".cfg", ".xml", ".rst", ".cpp", ".ps1", ".ll", ".smt2", ".asm",
}
ALLOWED_BINARY_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
ALLOWED_BARE_FILENAMES = {
    "LICENSE", "LICENSE.txt", "NOTICE", "Dockerfile", "Makefile",
}


def project_version(root: Path) -> str:
    data = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    version = data.get("project", {}).get("version")
    if not isinstance(version, str) or not version:
        raise ValueError("pyproject.toml does not contain project.version")
    return version


def tracked_files(root: Path) -> list[Path]:
    """Return reviewable source/config/docs/assets; reject unexpected binaries."""
    output: list[Path] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        parts = relative.parts
        if any(part in EXCLUDE_DIRS or part.endswith(".egg-info") for part in parts):
            continue
        if path.is_symlink():
            raise ValueError(f"Unsupported symlink in source tree: {relative}")
        if not path.is_file() or path.name in {"MANIFEST.json", "providers.json", "discovery.json"} or path.suffix in EXCLUDE_SUFFIXES:
            continue

        suffix = path.suffix.lower()
        allowed = (
            suffix in ALLOWED_TEXT_SUFFIXES
            or suffix in ALLOWED_BINARY_SUFFIXES
            or path.name in ALLOWED_BARE_FILENAMES
            or relative.parts[0] == ".github"
            or path.name in {".gitignore", ".gitattributes", ".editorconfig"}
        )
        if not allowed:
            raise ValueError(f"Review unexpected binary/resource before packaging: {relative}")
        output.append(relative)
    # Path ordering follows the host filesystem's case rules. Use portable
    # POSIX strings so Windows and Linux emit identical manifest/ZIP order.
    return sorted(output, key=lambda path: path.as_posix())


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_timestamp() -> tuple[int, str]:
    raw = os.environ.get("SOURCE_DATE_EPOCH")
    if raw:
        epoch = int(raw)
        dt = datetime.fromtimestamp(epoch, timezone.utc)
    else:
        dt = datetime(2026, 10, 16, tzinfo=timezone.utc)
    # ZIP timestamps have a two-second granularity and must be >= 1980.
    if dt.year < 1980:
        dt = datetime(1980, 1, 1, tzinfo=timezone.utc)
    second = dt.second - (dt.second % 2)
    dt = dt.replace(second=second, microsecond=0)
    return int(dt.timestamp()), dt.date().isoformat()


def produce_manifest(root: Path) -> dict:
    version = project_version(root)
    _, created = build_timestamp()
    files: dict[str, dict[str, int | str]] = {}
    for relative in tracked_files(root):
        data = (root / relative).read_bytes()
        files[relative.as_posix()] = {"sha256": sha256(data), "bytes": len(data)}
    return {
        "name": ARCHIVE_ROOT,
        "version": version,
        "created": created,
        "description": "Reverse engineering skill + executable MCP bridge (not native tool binaries)",
        "excluded": [
            "MANIFEST.json", "build artifacts", "caches", "virtual environments",
            "symlinks", "Python wheels and source ZIPs",
        ],
        "file_count_excluding_manifest": len(files),
        "files": files,
    }


def verify(root: Path, archive: Path | None = None) -> dict:
    manifest_path = root / "MANIFEST.json"
    if not manifest_path.is_file():
        raise ValueError("MANIFEST.json is missing; run release.py without --verify first")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = manifest["files"]
    actual = {p.as_posix() for p in tracked_files(root)}
    if set(expected) != actual:
        raise ValueError(
            f"Manifest inventory mismatch. Missing={sorted(set(expected)-actual)} "
            f"Extra={sorted(actual-set(expected))}"
        )
    for rel, row in expected.items():
        data = (root / rel).read_bytes()
        if sha256(data) != row["sha256"] or len(data) != row["bytes"]:
            raise ValueError(f"Manifest digest mismatch: {rel}")

    out = {"manifest": "PASS", "files": len(expected) + 1, "archive": None}
    if archive:
        with zipfile.ZipFile(archive) as z:
            bad = z.testzip()
            if bad:
                raise ValueError(f"ZIP CRC error: {bad}")
            paths = set(z.namelist())
            wanted = {f"{ARCHIVE_ROOT}/{rel}" for rel in expected} | {f"{ARCHIVE_ROOT}/MANIFEST.json"}
            if paths != wanted:
                raise ValueError(f"ZIP inventory mismatch: {paths ^ wanted}")
            for item in z.infolist():
                if item.filename.startswith("/") or ".." in Path(item.filename).parts:
                    raise ValueError("Unsafe archive member path")
                if stat.S_ISLNK(item.external_attr >> 16):
                    raise ValueError("Unexpected ZIP symlink")
                if "/" not in item.filename:
                    raise ValueError("Archive member must be rooted under project directory")
                rel = item.filename.split("/", 1)[1]
                disk = (root / rel).read_bytes()
                if z.read(item) != disk:
                    raise ValueError(f"ZIP member differs from disk: {rel}")
        out.update(
            archive="PASS",
            zip_sha256=sha256(archive.read_bytes()),
            zip_size=archive.stat().st_size,
        )
    return out


def build(root: Path, archive: Path) -> dict:
    manifest = produce_manifest(root)
    (root / "MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    files = tracked_files(root) + [Path("MANIFEST.json")]
    archive.parent.mkdir(parents=True, exist_ok=True)
    _, _ = build_timestamp()
    with zipfile.ZipFile(
        archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as z:
        for rel in sorted(files, key=lambda path: path.as_posix()):
            payload = (root / rel).read_bytes()
            entry = zipfile.ZipInfo(f"{ARCHIVE_ROOT}/{rel.as_posix()}")
            entry.date_time = datetime.fromtimestamp(
                build_timestamp()[0], timezone.utc
            ).timetuple()[:6]
            entry.external_attr = 0o100644 << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(entry, payload, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    results = verify(root, archive)
    archive.with_suffix(archive.suffix + ".sha256").write_text(
        f'{results["zip_sha256"]}  {archive.name}\n', encoding="utf-8", newline="\n"
    )
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--zip", type=Path)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.verify:
        result = verify(root, args.zip)
    else:
        if args.zip is None:
            parser.error("--zip is required unless --verify is used")
        result = build(root, args.zip.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
