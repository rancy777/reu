import io
import json
import os
import struct
import tempfile
import unittest
import zipfile
from pathlib import Path

from re_skill.filetriage import inspect_file
from re_skill.router import route_target


def write_pe(path, managed=False):
    raw = bytearray(0x400)
    raw[0:2] = b'MZ'
    struct.pack_into('<I', raw, 0x3c, 0x80)
    off = 0x80
    raw[off:off+4] = b'PE\x00\x00'
    struct.pack_into('<HHIIIHH', raw, off+4, 0x8664, 1, 0, 0, 0, 0xf0, 0x22)
    opt = off+24
    struct.pack_into('<H', raw, opt, 0x20b)
    struct.pack_into('<I', raw, opt+16, 0x1000)
    struct.pack_into('<I', raw, opt+108, 16)
    if managed: struct.pack_into('<II', raw, opt+112+14*8, 0x2000, 0x50)
    sec = opt+0xf0
    raw[sec:sec+8] = b'.text\x00\x00\x00'
    struct.pack_into('<IIII', raw, sec+8, 0x100, 0x1000, 0x200, 0x200)
    struct.pack_into('<I', raw, sec+36, 0x60000020)
    path.write_bytes(raw)

class TriageTests(unittest.TestCase):
    def test_pe32plus(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'maliciously_named.apk'; write_pe(p)
            val=inspect_file(p)
            self.assertEqual(val['format'], 'pe')
            self.assertEqual(val['pe_kind'], 'PE32+')
            self.assertEqual(val['architecture'], 'x64')
            self.assertIn('windows-triage', route_target(val)['workflows'])
            self.assertFalse(val['executable_was_run'])

    def test_pe_clr_dir(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'fixture.exe'; write_pe(p, True)
            val=inspect_file(p)
            self.assertTrue(val['dotnet'])
            self.assertIn('windows-dotnet', route_target(val)['workflows'])

    def test_apk_versus_aab(self):
        with tempfile.TemporaryDirectory() as td:
            for filename, entries, expected in [
                ('a.apk', {'AndroidManifest.xml':b'fake','classes.dex':b'fake'}, 'apk'),
                ('b.aab', {'base/manifest/AndroidManifest.xml':b'fake','base/dex/classes.dex':b'fake'},'aab'),
            ]:
                p=Path(td)/filename
                with zipfile.ZipFile(p,'w') as z:
                    for name,content in entries.items(): z.writestr(name,content)
                info=inspect_file(p)
                self.assertEqual(info['format'], expected)
                self.assertEqual(info['platform'],'android')

    def test_dex_and_elf(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'classes.dex'; p.write_bytes(b'dex\n039\x00' + b'\x00'*128)
            self.assertEqual(inspect_file(p)['dex_version'],'039')
            e=Path(td)/'libfoo.so'
            data=bytearray(64); data[:6]=b'\x7fELF\x02\x01'; struct.pack_into('<H',data,18,183)
            e.write_bytes(data)
            self.assertEqual(inspect_file(e)['architecture'],'ARM64')
            self.assertIn('native-elf-triage',route_target(inspect_file(e))['workflows'])
            self.assertIn('android-native',route_target({**inspect_file(e), 'android_context': True})['workflows'])

    def test_symlink_and_size_cap(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'a'; p.write_bytes(b'MZ'*20)
            link=Path(td)/'b'; link.symlink_to(p)
            with self.assertRaises(ValueError): inspect_file(link)
            with self.assertRaises(ValueError): inspect_file(p,max_size=10)
