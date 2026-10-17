"""Install a complete local Skill copy without overwriting an existing install."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil

from release import tracked_files

SKILL_NAME = 'reverse-engineering-unpacking'
SOURCE = Path(__file__).resolve().parents[1]


def install_skill(destination: Path) -> dict:
    destination = destination.expanduser()
    if destination.is_symlink():
        raise ValueError('destination must not be a symlink')
    destination = destination.resolve()
    if destination.name != SKILL_NAME:
        raise ValueError(f'destination folder must be named {SKILL_NAME}')
    if destination == SOURCE or SOURCE in destination.parents:
        raise ValueError('install outside the source tree')
    if destination.exists():
        raise FileExistsError(f'existing installation left unchanged: {destination}')
    files = tracked_files(SOURCE)
    destination.mkdir(parents=True, exist_ok=False)
    for relative in files:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE / relative, target)
    return {'skill': SKILL_NAME, 'path': str(destination), 'files': len(files),
            'runtime_installed': False, 'providers_started': False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path,
                        default=Path.home() / '.agents' / 'skills' / SKILL_NAME,
                        help='full Skill folder path; defaults to the Codex user Skill directory')
    args = parser.parse_args()
    try:
        print(json.dumps(install_skill(args.destination), indent=2))
    except (OSError, ValueError) as exc:
        parser.exit(2, f'Installation failed: {exc}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
