"""Behavior oracle for the self-owned benchmark; never claims devirtualization."""
import argparse
import hashlib
import json
from pathlib import Path
import random
import subprocess


def expected(value):
    for index in range(7):
        value ^= (0x9E3779B9 + index * 0x01020304) & 0xFFFFFFFF
        value = ((value << 5) | (value >> 27)) & 0xFFFFFFFF
        value = (value * 0x85EBCA6B + 0xC2B2AE35) & 0xFFFFFFFF
    return value


def validate(executable):
    executable = executable.resolve(strict=True)
    def run(*args):
        result = subprocess.run([str(executable), *args], capture_output=True, timeout=10)
        return result.returncode, result.stdout.decode('utf-8', errors='replace').replace('\r\n', '\n')
    assertions = []
    code, output = run('--self-test')
    assertions.append(('self-test', code == 0 and 'PASS (8/8)' in output))
    code, output = run('--negative-test')
    assertions.append(('negative-path', code == 1 and 'FAIL' in output))
    rng = random.Random(384)
    values = [0, 1, 2, 42, 123456789, 0x80000000, 0xFFFFFFFE, 0xFFFFFFFF]
    values += [rng.randrange(2**32) for _ in range(32)]
    for value in values:
        code, output = run('--value', str(value))
        assertions.append((f'value:{value}', code == 0 and output == f'{expected(value)}\n'))
    for value in ('4294967296', '-1', 'abc'):
        code, _ = run('--value', value)
        assertions.append((f'invalid:{value}', code == 2))
    return {
        'file': str(executable), 'sha256': hashlib.sha256(executable.read_bytes()).hexdigest(),
        'behavior': 'PASS' if all(ok for _, ok in assertions) else 'FAIL',
        'passed': sum(ok for _, ok in assertions), 'total': len(assertions),
        'failed': [name for name, ok in assertions if not ok],
        'scope': 'Functional equivalence only. Unpacking and devirtualization require separate evidence.'
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('executable', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    report = validate(args.executable)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))
    raise SystemExit(report['behavior'] != 'PASS')
