"""Smoke-test a built wheel in a clean environment outside the source checkout."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile
import venv
import zipfile


def check_install(wheel_dir: Path) -> dict:
    wheels = list(wheel_dir.resolve().glob('*.whl'))
    if len(wheels) != 1:
        raise ValueError('wheel directory must contain exactly one wheel')
    with zipfile.ZipFile(wheels[0]) as archive:
        if any(name.startswith('tests/') for name in archive.namelist()):
            raise ValueError('wheel must not install the development tests package')
    source = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix='reu-wheel-') as tmp:
        root = Path(tmp)
        venv.EnvBuilder(with_pip=True).create(root/'venv')
        python = root/'venv'/('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
        subprocess.run([str(python), '-m', 'pip', 'install', str(wheels[0]),
                        '--disable-pip-version-check'], cwd=root, check=True)
        probe = subprocess.run([str(python), '-I', '-c',
            'import json; from importlib.resources import files; import re_skill; '
            'print(json.dumps({"version":re_skill.__version__, '
            '"schemas":len(list(files("re_skill").joinpath("schemas").iterdir()))}))'],
            cwd=root, check=True, capture_output=True, text=True)
        metadata = json.loads(probe.stdout)
        import tomllib
        version = tomllib.loads((source/'pyproject.toml').read_text(encoding='utf-8'))['project']['version']
        if metadata != {'version': version, 'schemas': 7}:
            raise ValueError(f'wheel package data mismatch: {metadata}')
        cli = root/'venv'/('Scripts/re-skill.exe' if os.name == 'nt' else 'bin/re-skill')
        route = subprocess.run([str(cli), 'route',
            '--input', str(source/'runtime/examples/triage.sample.json')],
            cwd=root, check=True, capture_output=True, text=True)
        result = json.loads(route.stdout)
        if result['workflows'] != ['android-triage','android-dex','android-dynamic-loading']:
            raise ValueError(f'installed CLI route mismatch: {result}')
        if result['protection_status'] != 'Unknown':
            raise ValueError('synthetic metadata must not verify protection')
    return {'wheel': str(wheels[0]), 'package': metadata, 'isolated_cli': 'PASS',
            'providers_started': False, 'target_executed': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wheel-dir', required=True, type=Path)
    print(json.dumps(check_install(parser.parse_args().wheel_dir), indent=2))
