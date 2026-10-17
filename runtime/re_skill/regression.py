"""Executable regression assertions for supported deterministic scenarios.

Unsupported natural-language claims remain MANUAL, not silently marked PASS.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from .router import route_target
from .reasoning import diagnose, compatibility_applicability
from .capabilities import map_tool, side_effect_class
from .models import ToolDescriptor


def _get_path(obj: Any, path: str) -> Any:
    """Data-only assertion path; deliberately no eval or arbitrary Python."""
    for key in path.split('.'):
        if not isinstance(obj, dict) or key not in obj:
            raise KeyError(path)
        obj = obj[key]
    return obj


def _declarative_fixture(data: dict[str, Any]) -> Any:
    kind = data.get('executor')
    params = data.get('data', {})
    if not isinstance(params, dict):
        raise ValueError('declarative regression requires input.data object')
    if kind == 'route':
        return route_target(params)
    if kind == 'diagnose':
        return diagnose(params['symptom'], params.get('known'))
    if kind == 'compatibility':
        return compatibility_applicability(params['record'], params['environment'])
    if kind == 'tool-effect':
        td=ToolDescriptor(name=params['name'],title=None,description=params.get('description',''),
                          input_schema={'type':'object'}, annotations=params.get('annotations') or {})
        return {'side_effect_class': side_effect_class(td),
                'capabilities': [m.capability_id for m in map_tool(td) if m.confidence >= .65]}
    raise ValueError(f'unsupported declarative regression executor: {kind!r}')


def _check_fixture(result: Any, check: dict[str, Any]) -> bool:
    actual = _get_path(result, check['path'])
    expected = check.get('value')
    op = check.get('op')
    if op == 'eq': return actual == expected
    if op == 'ne': return actual != expected
    if op == 'contains': return expected in actual
    if op == 'not-contains': return expected not in actual
    if op == 'subset': return set(expected).issubset(set(actual))
    if op == 'exists': return actual is not None
    raise ValueError(f'unsupported declarative regression assertion: {op!r}')


def run_case(case: dict[str, Any]) -> dict[str, Any]:
    cid, data, exp = case['regression_id'], case['input'], case.get('expected', {})
    passed, failed, manual = [], [], []
    def check(name: str, ok: bool) -> None:
        (passed if ok else failed).append(name)
    if data.get('executor') is not None and 'checks' in exp:
        actual = _declarative_fixture(data)
        for entry in exp['checks']:
            try: check(entry['path']+' '+entry['op'], _check_fixture(actual,entry))
            except (KeyError, TypeError, ValueError): check(entry.get('path','invalid')+' invalid',False)
        manual = case.get('assertions', [])
    elif cid == 'RG-001':
        result = route_target({'filename':'fixture.exe','format':'pe32+', 'architecture':'x64',
                               'indicators':['high-entropy-section']})
        check('PE route', all(x in result['workflows'] for x in exp['route_contains']))
        check('packer only hypothesis', result['protection_status'] == exp['protector_status'])
        manual = case.get('assertions', [])
    elif cid == 'RG-002':
        result = diagnose('dumped-pe-does-not-start', data.get('known', []))
        names = {x['hypothesis'] for x in result['diagnoses']}
        check('failure branches', set(exp['diagnosis_contains']) <= names)
        check('changed-variable gate', result['requires_changed_variable'])
        manual = case.get('assertions', [])
    elif cid == 'RG-003':
        result = route_target({'filename':'fixture.aab','format':'aab'})
        check('AAB route', all(x in result['workflows'] for x in exp['route_contains']))
        check('split inventory', result['next_step'] == exp['next_step'])
        manual = case.get('assertions', [])
    elif cid == 'RG-004':
        result = route_target({'filename':'fixture.apk','format':'apk', 'signals':data['signals']})
        check('dynamic DEX route', all(x in result['workflows'] for x in exp['route_contains']))
        manual = case.get('assertions', [])
    elif cid == 'RG-009':
        from .capabilities import side_effect_class
        from .models import ToolDescriptor
        got=side_effect_class(ToolDescriptor(name=data['tool'],title=None,description='',input_schema={},annotations=data['annotations']))
        check('untrusted readOnlyHint cannot downgrade memory write',got==exp['side_effect_class'])
    elif cid == 'RG-010':
        from .selection import rank_providers
        got=rank_providers('pe.static', {'ida':{'status':'recommended','class':'official','capabilities':['pe.static']}},
                           [{'provider':{'id':'ida'},'health':{'status':'healthy'},'tool_capabilities':[]}])
        check('registry-only capability not authorized',bool(got)==exp['selected'])
    elif cid == 'RG-011':
        from .reasoning import compatibility_applicability
        got=compatibility_applicability({'environment':{'android_api':35},'result':'compatible','evidence_ids':['E1']},
                                        {'android_api':36})
        check('Android API mismatch is not applicable',got['applicable']==exp['applicable'])
    elif cid == 'RG-012':
        import tempfile
        from .corpus import CorpusStore
        with tempfile.TemporaryDirectory() as td:
            store=CorpusStore(td)
            store.add_node({'node_id':'C1','node_type':'claim','label':'claim'})
            try: store.add_edge('nonexistent','C1','supports','invalid')
            except ValueError: check('edge rejects dangling endpoint',True)
            else: check('edge rejects dangling endpoint',False)
    elif cid == 'RG-013':
        got=route_target({'format':'pe','indicators':['high-entropy-section']})
        check('high entropy is hypothesis',got['protection_status']==exp['protection_status'])
    elif cid == 'RG-014':
        from .capabilities import side_effect_class
        from .models import ToolDescriptor
        got=side_effect_class(ToolDescriptor(name='startHook',title=None,description='safe',input_schema={},annotations=data['annotations']))
        check('Frida hook is mutation',got==exp['side_effect_class'])
    elif cid == 'RG-015':
        from .security import validate_provider_spec, SecurityPolicyError
        from .models import ProviderSpec
        try: validate_provider_spec(ProviderSpec('bad','http',url=data['endpoint'],allow_remote=True,headers={'Authorization':'secret'}))
        except SecurityPolicyError: check('remote HTTP rejected',exp['blocked'])
        else: check('remote HTTP rejected',not exp['blocked'])
    elif cid == 'RG-016':
        import tempfile, struct
        from pathlib import Path
        from .filetriage import inspect_file
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'misleading.apk'
            buf=bytearray(256); buf[:2]=b'MZ'; struct.pack_into('<I',buf,0x3c,0x80)
            buf[0x80:0x84]=b'PE\x00\x00'; struct.pack_into('<HHIIIHH',buf,0x84,0x8664,0,0,0,0,0x70,0)
            buf[0x98:0x9a]=b'\x0b\x02'; p.write_bytes(buf)
            got=inspect_file(p)
        check('magic outranks misleading filename',got['format']==exp['format'])
    elif cid == 'RG-017':
        from .reasoning import promote_case_to_research
        got=promote_case_to_research({'target':{'sha256':'Unknown'},'protector':{'version':'Unknown'},
                                        'validation':data['case_validation']},[])
        check('unverified case not promoted',got['research_eligible']==exp['research_eligible'])
    elif cid == 'RG-018':
        from .reasoning import compatibility_applicability
        got=compatibility_applicability({'environment':{},'evidence_ids':[], 'result':'compatible'}, {})
        check('unknown environments need verification',got['status']==exp['result'])
    elif cid == 'RG-007':
        from .reasoning import compatibility_applicability
        result = compatibility_applicability({'result':'needs-verification','environment':{},'evidence_ids':[]}, {})
        check('unknown compatibility remains unknown', result['status'] == exp['result'])
        manual = case.get('assertions', [])
    else:
        manual = case.get('assertions', [])
    if not passed and not failed:
        status = 'MANUAL'
    elif failed:
        status = 'FAIL'
    elif manual:
        status = 'PARTIAL' # executable assertions pass; language assertions unverified
    else:
        status = 'PASS'
    return {'regression_id': cid, 'status': status,
            'passed': passed, 'failed': failed, 'manual_assertions': manual}


def run_regressions(path: str | Path) -> dict[str, Any]:
    rows, seen = [], set()
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        case = json.loads(line)
        cid = case['regression_id']
        if cid in seen:
            raise ValueError(f'duplicate regression ID: {cid}')
        seen.add(cid)
        rows.append(run_case(case))
    if not rows:
        raise ValueError('regression corpus must contain at least one case')
    statuses = {key: sum(x['status'] == key for x in rows) for key in ('PASS','PARTIAL','MANUAL','FAIL')}
    return {'summary': statuses, 'total': len(rows), 'results': rows,
            'warning': 'MANUAL and PARTIAL rows are NOT fully validated.'}
