"""Release artifacts retain evidence bytes and reject stale source manifests."""
import hashlib
from pathlib import Path
import runpy
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[2]
RELEASE = runpy.run_path(str(ROOT / 'scripts' / 'release.py'))


class SourceReleaseTests(unittest.TestCase):
    def create_source(self, directory):
        source = Path(directory) / 'source'
        source.mkdir()
        (source / 'pyproject.toml').write_bytes(b'[project]\nversion = "1.0.0"\n')
        evidence = source / 'examples' / 'case' / 'trace.txt'
        evidence.parent.mkdir(parents=True)
        evidence.write_bytes(b'recorded|bytes\r\nsecond|row\r\n')
        return source, evidence

    def test_archives_are_reproducible_and_preserve_exact_evidence_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            source, evidence = self.create_source(directory)
            original = evidence.read_bytes()
            first = Path(directory) / 'first.zip'
            second = Path(directory) / 'second.zip'
            RELEASE['build'](source, first)
            RELEASE['build'](source, second)

            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertNotIn(b'\r\n', (source / 'MANIFEST.json').read_bytes())
            expected = hashlib.sha256(first.read_bytes()).hexdigest()
            self.assertEqual(first.with_suffix('.zip.sha256').read_bytes(),
                             f'{expected}  first.zip\n'.encode('ascii'))
            with zipfile.ZipFile(first) as archive:
                self.assertEqual(archive.read('reverse-engineering-unpacking/examples/case/trace.txt'), original)
                self.assertEqual({entry.create_system for entry in archive.infolist()}, {3})
            self.assertEqual(evidence.read_bytes(), original)

    def test_verification_rejects_source_changes_until_manifest_is_refreshed(self):
        with tempfile.TemporaryDirectory() as directory:
            source, evidence = self.create_source(directory)
            RELEASE['build'](source, Path(directory) / 'source.zip')
            evidence.write_bytes(b'changed evidence\n')
            with self.assertRaisesRegex(ValueError, 'digest mismatch'):
                RELEASE['verify'](source)

    def test_mixed_case_paths_have_the_same_archive_order_on_every_platform(self):
        with tempfile.TemporaryDirectory() as directory:
            source, _ = self.create_source(directory)
            (source / 'README.md').write_bytes(b'Project\n')
            (source / 'docs').mkdir()
            (source / 'docs' / 'README.md').write_bytes(b'Documentation\n')
            (source / 'docs' / 'alpha.md').write_bytes(b'Example\n')
            archive_path = Path(directory) / 'source.zip'
            RELEASE['build'](source, archive_path)
            with zipfile.ZipFile(archive_path) as archive:
                names = archive.namelist()
            self.assertEqual(names, sorted(names))
