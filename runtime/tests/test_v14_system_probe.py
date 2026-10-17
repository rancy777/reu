import unittest
from re_skill.system_probe import system_probe


class SystemProbeTests(unittest.TestCase):
    def test_inventory_is_read_only_and_unverified(self):
        row=system_probe()
        self.assertFalse(row['actual_provider_handshakes_performed'])
        self.assertIn('None:',row['side_effects'])
        self.assertIn('adb',row['tools'])
        for tool in row['tools'].values():
            self.assertEqual(tool['version'],'Not checked')
            self.assertEqual(tool['health'],'Not checked')
