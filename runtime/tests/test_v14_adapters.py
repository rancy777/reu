import json
import tempfile
import unittest
from pathlib import Path
from re_skill.adapters import adapter_plan, load_adapter_profiles
from re_skill.capabilities import side_effect_class
from re_skill.models import ToolDescriptor
from re_skill.selection import rank_providers
from re_skill.security import validate_provider_spec, SecurityPolicyError
from re_skill.models import ProviderSpec

ROOT = Path(__file__).resolve().parents[2]

class AdapterTests(unittest.TestCase):
    def test_profiles_real_names_only(self):
        profiles=load_adapter_profiles(ROOT/'integrations/provider-adapter-profiles.json')
        discovery={'providers':[{'provider':{'id':'jadx.zinja'},'health':{'status':'healthy'},
                   'tools':[{'name':'get_class_source','input_schema':{'type':'object','properties':{'class_name':{'type':'string'}}}}]}]}
        result=adapter_plan(discovery,'jadx.zinja','android.class-source',profiles['jadx.zinja'])
        self.assertEqual(result['status'],'ready-to-plan')
        self.assertEqual(result['candidates'][0]['tool'],'get_class_source')
        self.assertEqual(result['candidates'][0]['risk'],'observe')
        self.assertEqual(adapter_plan(discovery,'jadx.zinja','android.smali',profiles['jadx.zinja'])['status'],'unmapped-or-schema-changed')

    def test_frida_camelcase_is_mutation(self):
        for name,effect in [('writeMemory','mutate'),('readMemory','observe'),('listModules','observe'),('startHook','mutate'),('deleteProcess','destructive')]:
            tool=ToolDescriptor(name=name,title=None,description='readOnlyHint true',input_schema={},annotations={'readOnlyHint':True})
            self.assertEqual(side_effect_class(tool),effect,name)

    def test_registry_only_cannot_grant_capability(self):
        registry={'ida':{'status':'recommended','class':'official','capabilities':['pe.static']}}
        discovery=[{'provider':{'id':'ida'},'health':{'status':'healthy','capabilities':['pe.static']},'tool_capabilities':[]}]
        self.assertEqual(rank_providers('pe.static',registry,discovery),[])

    def test_remote_requires_https_and_auth(self):
        for url,allowed,headers in [('http://example.com/mcp',True,{'Authorization':'Bearer x'}),('https://example.com/mcp',True,{})]:
            with self.assertRaises(SecurityPolicyError):
                validate_provider_spec(ProviderSpec('remote','http',url=url,allow_remote=allowed,headers=headers))
        validate_provider_spec(ProviderSpec('remote','http',url='https://example.com/mcp',allow_remote=True,headers={'Authorization':'Bearer x'}))

    def test_legacy_sse_is_local_only(self):
        validate_provider_spec(ProviderSpec('unidbg','sse',url='http://127.0.0.1:9239/sse'))
        with self.assertRaises(SecurityPolicyError):
            validate_provider_spec(ProviderSpec('bad','sse',url='http://example.com/sse'))

    def test_alias_wrappers_count_as_single_native_modality(self):
        from re_skill.selection import independent_modalities
        candidates=[{'provider_id':'ida-a','native_tool':'IDA Pro'},
                    {'provider_id':'ida-b','native_tool':'Hex-Rays IDA'},
                    {'provider_id':'r2','native_tool':'radare2'}]
        grouped=independent_modalities(candidates)
        self.assertEqual(len(grouped),2)
        self.assertIn('ida', [x['native_tool_key'] for x in grouped])
