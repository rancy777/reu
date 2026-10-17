"""Accept this benchmark only after fresh structure and isolated behavior checks."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from validate_behavior import validate

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
root = Path(__file__).resolve().parents[1]
candidate = root / 'unpacked' / 'reu-challenge.unpacked.exe'
try:
    fingerprint = hashlib.sha256(candidate.read_bytes()).hexdigest()
    subprocess.run([sys.executable, str(Path(__file__).with_name('validate_structure.py'))], check=True)
    structure = json.loads((root / 'evidence' / 'unpacked-structure.json').read_text(encoding='utf-8'))
    previous_directory = Path.cwd()
    with tempfile.TemporaryDirectory(prefix='reu-unpacked-isolated-') as temporary:
        isolated = Path(temporary) / 'independent.exe'
        shutil.copy2(candidate, isolated)
        try:
            os.chdir(temporary)
            behavior = validate(isolated)
        finally:
            os.chdir(previous_directory)
        behavior.update(source_artifact=str(candidate), working_directory=temporary,
                        files_present_before_execution=['independent.exe'],
                        isolation='Only the reconstructed EXE was copied into the temporary working directory')
    (root / 'evidence' / 'unpacked-behavior.json').write_text(json.dumps(behavior, indent=2)+'\n', encoding='utf-8')
    if not behavior['sha256'] == structure['sha256'] == fingerprint:
        raise ValueError('Reports identify different artifacts')
    if hashlib.sha256(candidate.read_bytes()).hexdigest() != fingerprint:
        raise ValueError('Artifact changed during verification')
    if behavior['behavior'] != 'PASS' or structure['structure'] != 'PASS':
        raise ValueError('A required acceptance gate failed')
    acceptance = {'status': 'PASS_THIS_SAMPLE', 'sha256': fingerprint,
                  'behavior_checks': f"{behavior['passed']}/{behavior['total']}",
                  'structure_checks': f"{sum(structure['checks'].values())}/{len(structure['checks'])}",
                  'scope': 'Known-OEP-assisted, manually repaired loader-only benchmark; no devirtualization claim'}
    (root / 'evidence' / 'acceptance.json').write_text(json.dumps(acceptance, indent=2)+'\n', encoding='utf-8')
    print('脱壳验证成功（仅当前自有样本；不代表去虚拟化）')
    print(json.dumps(acceptance, ensure_ascii=False))
except Exception as error:
    print(f'脱壳验证失败：{error}', file=sys.stderr)
    raise SystemExit(1)
