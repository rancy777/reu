"""Install a portable Skill into a fresh directory and preserve existing data."""
import json
import runpy
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml

from re_skill.cli import main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
NAME = 'reverse-engineering-unpacking'


class InstallationTests(unittest.TestCase):
    def run_installer(self, target):
        return subprocess.run([sys.executable, str(ROOT/'scripts/install_skill.py'),
                               '--destination', str(target)], capture_output=True,
                              text=True, encoding='utf-8', timeout=30)

    def test_install_contains_discoverable_skill_and_its_dependencies(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)/NAME
            result = self.run_installer(target)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(json.loads(result.stdout)['providers_started'])
            text = (target/'SKILL.md').read_text(encoding='utf-8')
            self.assertTrue(text.startswith('---\n'))
            meta = yaml.safe_load(text.split('---', 2)[1])
            self.assertEqual(meta['name'], target.name)
            self.assertTrue(meta['description'].strip())
            for relative in ('references/evidence-policy.md', 'workflows/windows-triage.md',
                             'integrations/mcp-provider-registry.yaml', 'pyproject.toml',
                             'runtime/re_skill/cli.py'):
                self.assertTrue((target/relative).is_file(), relative)
            env = subprocess.run([sys.executable, '-c',
                'import sys; sys.path.insert(0, "runtime"); '
                'from re_skill.router import route_target; '
                'assert route_target({"format":"apk"})["platform"] == "android"'],
                cwd=target, capture_output=True, text=True, timeout=10)
            self.assertEqual(env.returncode, 0, env.stderr)
            self.assertFalse((target/'.git').exists())
            self.assertFalse((target/'build').exists())

    def test_existing_install_is_unchanged_and_source_recursion_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)/NAME
            target.mkdir()
            marker = target/'keep.txt'
            marker.write_text('user data', encoding='utf-8')
            result = self.run_installer(target)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(marker.read_text(encoding='utf-8'), 'user data')
            self.assertEqual(list(target.iterdir()), [marker])
        result = self.run_installer(ROOT/'build'/NAME)
        self.assertEqual(result.returncode, 2)

    def test_package_inventory_excludes_local_configuration_and_runtime_output(self):
        inventory = runpy.run_path(str(ROOT/'scripts/release.py'))['tracked_files']
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'SKILL.md').write_text('public instructions', encoding='utf-8')
            (root/'providers.json').write_text('{"secret":"private"}', encoding='utf-8')
            (root/'discovery.json').write_text('{}', encoding='utf-8')
            (root/'runtime-artifacts').mkdir()
            (root/'runtime-artifacts'/'private.bin').write_bytes(b'private')
            (root/'.agents').mkdir()
            (root/'.agents'/'local.md').write_text('local instructions', encoding='utf-8')
            self.assertEqual(inventory(root), [Path('SKILL.md')])


class RegressionGateTests(unittest.TestCase):
    def test_empty_and_duplicate_corpora_cannot_pass_the_cli_gate(self):
        from contextlib import redirect_stdout
        import io
        row = (ROOT/'corpus/regression/automated.jsonl').read_text(encoding='utf-8').splitlines()[0]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'invalid.jsonl'
            for content in ('', row+'\n'+row+'\n'):
                path.write_text(content, encoding='utf-8')
                with self.subTest(content=bool(content)), redirect_stdout(io.StringIO()):
                    with patch.object(sys, 'argv', ['re-skill','regress','--strict','--file',str(path)]):
                        self.assertEqual(main(), 3)

    def test_automated_corpus_passes_strict_gate(self):
        from re_skill.cli import cmd_regression
        from argparse import Namespace
        with patch('re_skill.cli.write_output'):
            result = cmd_regression(Namespace(file=str(ROOT/'corpus/regression/automated.jsonl'),
                                             strict=True, output=None))
        self.assertEqual(result, 0)
