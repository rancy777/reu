import json
import tempfile
import unittest
from pathlib import Path
from re_skill.corpus import CorpusStore, validate_record
from re_skill.reasoning import compatibility_applicability, promote_case_to_research
from re_skill.regression import run_regressions

ROOT = Path(__file__).resolve().parents[2]

class CorpusEngineTests(unittest.TestCase):
    def test_case_schema_dedup_and_similarity(self):
        case=json.loads((ROOT/'corpus/protector-cases/index.jsonl').read_text().splitlines()[0])
        with tempfile.TemporaryDirectory() as td:
            store=CorpusStore(td)
            store.add_case(case)
            self.assertEqual(store.query_cases(protector='.NET Reactor')[0]['case_id'],case['case_id'])
            res=store.similar_cases({'platform':'Windows/.NET','protector':{'family':'.NET Reactor'}})
            self.assertGreater(res[0]['similarity_score'],0)
            with self.assertRaises(ValueError): store.add_case(case)
            check=promote_case_to_research(case,[])
            self.assertFalse(check['research_eligible'])

    def test_graph_edges_validate_and_connect(self):
        with tempfile.TemporaryDirectory() as td:
            store=CorpusStore(td)
            s=store.add_node({'node_id':'S1','node_type':'source','label':'official'})
            c=store.add_node({'node_id':'C1','node_type':'claim','label':'restricted claim'})
            store.add_edge(s,c,'supports','official source supports claim')
            sub=store.graph_neighborhood('C1',1)
            self.assertEqual(len(sub['nodes']),2)
            with self.assertRaises(ValueError): store.add_edge('missing',c,'supports','invalid')

    def test_compatibility_does_not_leak_across_versions(self):
        row={'environment':{'os':'Android 15','android_api':35,'abi':'arm64','runtime':'ART'},
             'result':'compatible','evidence_ids':['E1']}
        self.assertFalse(compatibility_applicability(row,{'os':'Android 16','android_api':36,'abi':'arm64','runtime':'ART'})['applicable'])
        self.assertEqual(compatibility_applicability(row,{'os':'Android 15','android_api':35,'abi':'arm64','runtime':'ART'})['status'],'needs-verification')

    def test_bundled_all_corpus_valid(self):
        schema_paths={'protector-cases/index.jsonl':'protector-case.schema.json','runtime-compatibility/index.jsonl':'runtime-compatibility.schema.json',
                      'evidence-graph/nodes.jsonl':'evidence-node.schema.json','evidence-graph/edges.jsonl':'evidence-edge.schema.json',
                      'regression/automated.jsonl':'regression-case.schema.json',
                      'regression/research.jsonl':'regression-case.schema.json'}
        for relative,schema in schema_paths.items():
            for line in (ROOT/'corpus'/relative).read_text().splitlines():
                if line.strip(): self.assertEqual(validate_record(json.loads(line),ROOT/'corpus/schemas'/schema),[],relative)

    def test_regressions_are_not_falsely_all_passed(self):
        result=run_regressions(ROOT/'corpus/regression/research.jsonl')
        self.assertEqual(result['total'],8)
        self.assertEqual(result['summary']['FAIL'],0)
        self.assertGreater(result['summary']['MANUAL']+result['summary']['PARTIAL'],0)

    def test_promotion_requires_reproduced_experiments_not_prose(self):
        base={'target':{'sha256':'a'*64},'protector':{'version':'1.0'},'validation':'Validated perfectly',
              'evidence_ids':['E1','E2'],'status':'case-only'}
        sources=[{'node_id':'E1','provenance':{'source_ids':['SRC-1']}},
                 {'node_id':'E2','provenance':{'source_ids':['SRC-2']}}]
        first=promote_case_to_research(base,sources)
        self.assertFalse(first['research_eligible'])
        self.assertFalse(first['checks']['reproduced_experiment_ids_recorded'])
        base['verification']={'reproduced':True,'human_reviewed':True,'independent_sources_reviewed':True,'experiment_ids':['LAB-0001']}
        second=promote_case_to_research(base,sources)
        self.assertTrue(second['research_eligible'])
        self.assertFalse(second['canonical_eligible'])
        base['target']['sha256']='z'*64
        self.assertFalse(promote_case_to_research(base,sources)['research_eligible'])
