import json
import tempfile
import unittest
from pathlib import Path

from re_skill.capabilities import map_tool, side_effect_class
from re_skill.models import ToolDescriptor
from re_skill.router import route_target
from re_skill.security import SecurityPolicyError, validate_provider_spec
from re_skill.models import ProviderSpec
from re_skill.corpus import CorpusStore
from re_skill.selection import rank_providers, independent_modalities


class RuntimeTests(unittest.TestCase):
    def test_capability_mapping(self):
        tool = ToolDescriptor(
            name="decompile_function",
            title=None,
            description="Decompile a function and return pseudocode",
            input_schema={"type": "object"},
        )
        matches = map_tool(tool)
        self.assertEqual(matches[0].capability_id, "decompiler")
        self.assertEqual(side_effect_class(tool), "observe")

    def test_mutation_is_gated(self):
        tool = ToolDescriptor(
            name="write_memory",
            title=None,
            description="Write bytes into process memory",
            input_schema={"type": "object"},
        )
        self.assertEqual(side_effect_class(tool), "mutate")

    def test_route_android_dynamic_dex(self):
        result = route_target({
            "filename": "sample.apk",
            "format": "apk",
            "architecture": "arm64",
            "dynamic_dex": True,
        })
        self.assertEqual(result["platform"], "android")
        self.assertIn("android-dynamic-loading", result["workflows"])

    def test_remote_http_blocked_by_default(self):
        spec = ProviderSpec(
            provider_id="test",
            transport="http",
            url="http://192.0.2.10:8080/mcp",
            allow_remote=False,
        )
        with self.assertRaises(SecurityPolicyError):
            validate_provider_spec(spec)

    def test_corpus_writes_jsonl(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = CorpusStore(tmp)
            obs_id = store.add_observation({
                "provider_id": "test",
                "operation": "static.metadata",
                "native_tool": "fixture",
                "status": "success",
            })
            self.assertTrue(obs_id.startswith("OBS-"))
            path = Path(tmp) / "observations/index.jsonl"
            self.assertTrue(path.exists())
            record = json.loads(path.read_text().splitlines()[0])
            self.assertEqual(record["observation_id"], obs_id)

    def test_provider_selection_does_not_count_wrappers_twice(self):
        registry = {
            "ida": {"class": "official", "status": "recommended", "native_tool": "IDA", "capabilities": ["pe.static"]},
            "ida-wrapper": {"class": "community", "status": "candidate", "native_tool": "IDA", "capabilities": ["pe.static"]},
        }
        discovery = [
            {"provider": {"id": "ida"}, "health": {"status": "healthy", "capabilities": ["pe.static"]},
             "tool_capabilities": [{"tool": "get_functions", "capabilities": [{"capability_id": "pe.static", "confidence": .8, "side_effect_class": "observe"}]}]},
            {"provider": {"id": "ida-wrapper"}, "health": {"status": "healthy", "capabilities": ["pe.static"]},
             "tool_capabilities": [{"tool": "get_functions", "capabilities": [{"capability_id": "pe.static", "confidence": .8, "side_effect_class": "observe"}]}]},
        ]
        ranked = rank_providers("pe.static", registry, discovery)
        self.assertEqual(ranked[0]["provider_id"], "ida")
        mods = independent_modalities(ranked)
        self.assertEqual(mods[0]["count_as_independent_modalities"], 1)


if __name__ == "__main__":
    unittest.main()
