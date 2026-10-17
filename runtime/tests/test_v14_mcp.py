import asyncio
import json
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from re_skill.mcp_client import connect, list_all_tools, tool_to_descriptor
from re_skill.models import ProviderSpec, ToolDescriptor
from re_skill.capabilities import side_effect_class
from re_skill.security import authorize_tool, SecurityPolicyError
from re_skill.discovery import discover_one
from re_skill.cli import _call
from re_skill.corpus import CorpusStore

FIXTURE = Path(__file__).with_name('fixtures') / 'mock_mcp_stdio.py'

class MCPWireTests(unittest.IsolatedAsyncioTestCase):
    def setup_spec(self):
        return ProviderSpec(provider_id='fixture', transport='stdio', command=sys.executable, args=[str(FIXTURE)])

    async def test_real_stdio_handshake_pages_call(self):
        async with connect(self.setup_spec(), prefer_wire=True) as session:
            tools = await list_all_tools(session)
            self.assertEqual([t.name for t in tools], ['get_functions','decompile_function','write_memory'])
            self.assertEqual(session.server_info.name, 'offline-mcp-fixture')
            out = await session.call_tool('get_functions', {})
            self.assertEqual(out.structured_content['functions'], ['main'])

    async def test_mock_discovery(self):
        r=await discover_one(self.setup_spec(), {'capabilities':['pe.static'], 'status':'candidate'}, prefer_wire=True)
        self.assertEqual(r['health']['status'], 'healthy')
        self.assertIn('pe.static',r['health']['capabilities'])
        self.assertEqual(r['health']['tool_count'], 3)

    async def test_readonly_hint_cannot_override_write(self):
        tool=ToolDescriptor(name='write_memory',title=None,description='Reads state',input_schema={},annotations={'readOnlyHint':True})
        self.assertEqual(side_effect_class(tool),'mutate')
        with self.assertRaises(SecurityPolicyError):
            authorize_tool('mutate',authorized_target=True,allow_execute=False,allow_mutate=False,allow_destructive=False)

    async def test_real_cli_call_and_corpus(self):
        with tempfile.TemporaryDirectory() as td:
            conf=Path(td)/'providers.json'
            conf.write_text(json.dumps({'providers':[{'provider_id':'fixture','transport':'stdio','command':sys.executable,'args':[str(FIXTURE)]}]}))
            reg=Path(td)/'registry.yaml'; reg.write_text('providers:\n  - id: fixture\n    status: candidate\n')
            args=Namespace(config=str(conf),registry=str(reg),provider='fixture',tool='decompile_function',
                           arguments='{"address":"0x1000"}',arguments_file=None,target='{"sha256":"'+('a'*64)+'"}',target_file=None,
                           representation='mapped-pe',workspace=td,wire=True,store_raw=True,
                           authorized_target=False,allow_execute=False,allow_mutate=False,allow_destructive=False,timeout=20.0)
            result=await _call(args)
            self.assertEqual(result['status'],'success')
            self.assertEqual(result['completeness'],'complete')
            self.assertTrue(result['raw_output_ref'])
            store=CorpusStore(td)
            store.add_observation(result)
            obs=store.read('observations/index.jsonl')
            self.assertEqual(obs[0]['observation_id'], result['observation_id'])
            self.assertEqual(len(store.read('evidence-graph/edges.jsonl')),1)

    async def test_json_schema_inputs_are_enforced(self):
        with tempfile.TemporaryDirectory() as td:
            conf=Path(td)/'providers.json'; conf.write_text(json.dumps({'providers':[{'provider_id':'fixture','transport':'stdio','command':sys.executable,'args':[str(FIXTURE)]}]}))
            reg=Path(td)/'registry.yaml'; reg.write_text('providers:\n  - id: fixture\n    status: candidate\n')
            args=Namespace(config=str(conf),registry=str(reg),provider='fixture',tool='decompile_function',
                           arguments='{}',arguments_file=None,target='{}',target_file=None,
                           representation=None,workspace=None,wire=True,store_raw=False,
                           authorized_target=False,allow_execute=False,allow_mutate=False,allow_destructive=False,timeout=20.0)
            with self.assertRaises(Exception):
                await _call(args)

    async def test_refuse_mutation_even_with_false_readonly_hint(self):
        with tempfile.TemporaryDirectory() as td:
            conf=Path(td)/'providers.json'
            conf.write_text(json.dumps({'providers':[{'provider_id':'fixture','transport':'stdio','command':sys.executable,'args':[str(FIXTURE)]}]}))
            reg=Path(td)/'registry.yaml'; reg.write_text('providers:\n  - id: fixture\n    status: candidate\n')
            args=Namespace(config=str(conf),registry=str(reg), provider='fixture',tool='write_memory',
                           arguments='{"address":"0x1000","bytes":"AA"}',arguments_file=None,
                           target='{}',target_file=None, representation=None,workspace=None,
                           wire=True, authorized_target=False,allow_execute=False,allow_mutate=False,allow_destructive=False,timeout=20.0)
            with self.assertRaises(SecurityPolicyError):
                await _call(args)
