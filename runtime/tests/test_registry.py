import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


class RegistryTests(unittest.TestCase):
    def test_registry_is_valid_yaml(self):
        path = ROOT / "integrations" / "mcp-provider-registry.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        self.assertIsInstance(data.get("providers"), list)
        ids = [x.get("id") for x in data["providers"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(ids))

    def test_selection_references_known_providers(self):
        registry = yaml.safe_load(
            (ROOT / "integrations" / "mcp-provider-registry.yaml").read_text(encoding="utf-8")
        )
        selection = yaml.safe_load(
            (ROOT / "integrations" / "provider-selection.yaml").read_text(encoding="utf-8")
        )
        known = {x["id"] for x in registry["providers"]}
        refs = []
        for binding in selection["bindings"].values():
            refs.extend(binding.get("preferred", []))
            refs.extend(binding.get("fallbacks", []))
        self.assertTrue(set(refs) <= known | {"artifact.exec", "shell.host", "filesystem.official"})


if __name__ == "__main__":
    unittest.main()
