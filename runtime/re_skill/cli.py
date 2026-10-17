"""Agent-facing CLI: safe preflight, discovery, invocation, triage and corpus operations."""
from __future__ import annotations

import argparse
import asyncio
import json
import shutil
from pathlib import Path
from typing import Any

from .capabilities import map_tool, side_effect_class
from .adapters import load_adapter_profiles, adapter_plan
from .config import load_provider_specs, load_registry
from .corpus import CorpusStore, validate_record
from .discovery import discover_all
from .filetriage import inspect_file
from .host_inventory import normalize_host_inventory
from .mcp_client import connect, list_all_tools, tool_to_descriptor, call_tool
from .models import ProviderSpec, ToolDescriptor
from .normalize import normalize_result, observation_to_dict
from .orchestrator import RESkillRuntime
from .regression import run_regressions
from .reasoning import diagnose, promote_case_to_research
from .security import SecurityPolicyError, authorize_tool, authorize_read_tool_shape, validate_provider_spec
from .provider_policy import require_approved_provider
from .tool_schema import validate_mcp_arguments
from .system_probe import system_probe
from jsonschema.exceptions import ValidationError


def dump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)


def write_output(value: Any, path: str | None = None) -> None:
    formatted = dump(value)
    if path:
        Path(path).write_text(formatted + '\n', encoding='utf-8')
    print(formatted)


def cmd_system_probe(args: argparse.Namespace) -> int:
    write_output(system_probe(), args.output)
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    configs = load_provider_specs(args.config)
    results = []
    for spec in configs:
        row: dict[str, Any] = {'id': spec.provider_id, 'transport': spec.transport}
        try:
            validate_provider_spec(spec)
            if spec.transport == 'stdio':
                binary = shutil.which(spec.command) or (spec.command if Path(spec.command).is_file() else None)
                row.update(status='configured' if binary else 'missing-executable', command=spec.command,
                           notes='preflight ONLY; no MCP process launched')
            else:
                row.update(status='configured-unverified', url=spec.url,
                           notes='no remote request made')
        except SecurityPolicyError as e:
            row.update(status='blocked', reason=str(e))
        results.append(row)
    write_output({'providers': results, 'actual_handshakes_performed': False})
    return 0 if all(r['status'].startswith('configured') for r in results) else 2


def cmd_discover(args: argparse.Namespace) -> int:
    results = asyncio.run(discover_all(load_provider_specs(args.config),
                                       load_registry(args.registry), timeout=args.timeout,
                                       prefer_wire=args.wire))
    write_output({'providers': results}, args.output)
    return 0 if all(r['health']['status'] == 'healthy' for r in results) else 2


def cmd_route(args: argparse.Namespace) -> int:
    value = json.loads(Path(args.input).read_text(encoding='utf-8'))
    write_output(RESkillRuntime.route(value)); return 0


def cmd_triage(args: argparse.Namespace) -> int:
    info = inspect_file(args.file, max_size=args.max_size)
    if args.route: info['workflow_route'] = RESkillRuntime.route(info)
    write_output(info, args.output)
    return 0


def cmd_select(args: argparse.Namespace) -> int:
    runtime = RESkillRuntime(args.config, args.registry)
    runtime.discovery = json.loads(Path(args.discovery).read_text(encoding='utf-8'))['providers']
    write_output(runtime.select(args.capability)); return 0


def cmd_host(args: argparse.Namespace) -> int:
    value = json.loads(Path(args.input).read_text(encoding='utf-8'))
    write_output(normalize_host_inventory(value)); return 0


def cmd_validate(args: argparse.Namespace) -> int:
    errors, count = [], 0
    for i, line in enumerate(Path(args.jsonl).read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip(): continue
        count += 1
        try:
            problem = validate_record(json.loads(line), args.schema)
        except json.JSONDecodeError as e:
            problem = [str(e)]
        if problem: errors.append({'line': i, 'errors': problem})
    write_output({'records': count, 'valid': not errors, 'errors': errors})
    return 0 if not errors else 2


def cmd_regression(args: argparse.Namespace) -> int:
    result = run_regressions(args.file)
    write_output(result, args.output)
    return 0 if (not result['summary']['FAIL'] and (not args.strict or result['summary']['PARTIAL'] == result['summary']['MANUAL'] == 0)) else 2


def cmd_workspace(args: argparse.Namespace) -> int:
    store = CorpusStore(args.path)
    write_output({'workspace': str(store.root.resolve()), 'status': 'initialized',
                  'samples_copied': False, 'automatic_tools_installed': False})
    return 0


def cmd_case(args: argparse.Namespace) -> int:
    store = CorpusStore(args.workspace)
    write_output({'results': store.query_cases(platform=args.platform, protector=args.protector,
                                                architecture=args.architecture)}); return 0


def cmd_similar(args: argparse.Namespace) -> int:
    store = CorpusStore(args.workspace)
    record = json.loads(Path(args.input).read_text(encoding='utf-8'))
    write_output({'results': store.similar_cases(record, limit=args.limit)}); return 0


def cmd_graph(args: argparse.Namespace) -> int:
    write_output(CorpusStore(args.workspace).graph_neighborhood(args.node, depth=args.depth)); return 0


def cmd_graph_repair(args: argparse.Namespace) -> int:
    write_output(CorpusStore(args.workspace).repair_graph(dry_run=not args.apply))
    return 0


def cmd_ingest(args: argparse.Namespace) -> int:
    store = CorpusStore(args.workspace)
    record = json.loads(Path(args.input).read_text(encoding='utf-8'))
    if args.kind == 'case': key = store.add_case(record)
    elif args.kind == 'compatibility': key = store.add_compatibility(record)
    elif args.kind == 'observation': key = store.add_observation(record)
    elif args.kind == 'node': key = store.add_node(record)
    else: raise ValueError('unsupported ingest kind')
    write_output({'ingested': args.kind, 'id': key, 'schema_validated': True}); return 0


def cmd_adapter_plan(args: argparse.Namespace) -> int:
    profiles=load_adapter_profiles(args.profiles)
    discovered=json.loads(Path(args.discovery).read_text(encoding='utf-8'))
    write_output(adapter_plan(discovered,args.provider,args.intent,profiles.get(args.provider)))
    return 0


def cmd_diagnose(args: argparse.Namespace) -> int:
    write_output(diagnose(args.symptom, args.known)); return 0


def cmd_promote_check(args: argparse.Namespace) -> int:
    store = CorpusStore(args.workspace)
    cases = {x['case_id']: x for x in store.read('protector-cases/index.jsonl')}
    if args.case not in cases: raise ValueError('unknown case id')
    result = promote_case_to_research(cases[args.case], store.read('evidence-graph/nodes.jsonl'))
    write_output(result); return 0


async def _call(args: argparse.Namespace) -> dict[str, Any]:
    specs = {spec.provider_id: spec for spec in load_provider_specs(args.config)}
    if args.provider not in specs: raise ValueError(f'unknown provider id: {args.provider}')
    spec = specs[args.provider]
    require_approved_provider(args.provider, load_registry(args.registry))
    validate_provider_spec(spec)
    arguments = json.loads(Path(args.arguments_file).read_text(encoding='utf-8')) if args.arguments_file else json.loads(args.arguments)
    if not isinstance(arguments, dict): raise ValueError('tool arguments must be a JSON object')
    target = json.loads(Path(args.target_file).read_text(encoding='utf-8')) if args.target_file else json.loads(args.target)
    if not isinstance(target, dict): raise ValueError('target must be a JSON object')
    async with connect(spec, prefer_wire=args.wire) as session:
        tool_list = await asyncio.wait_for(list_all_tools(session), timeout=args.timeout)
        raw_tool = next((x for x in tool_list if getattr(x, 'name', None) == args.tool), None)
        if raw_tool is None: raise ValueError(f'tool not discovered from provider: {args.tool}')
        desc = tool_to_descriptor(raw_tool)
        tool = ToolDescriptor(name=desc['name'], title=desc['title'], description=desc['description'],
                              input_schema=desc['input_schema'], annotations=desc['annotations'])
        effect = side_effect_class(tool)
        authorize_read_tool_shape(tool, effect)
        authorize_tool(effect, authorized_target=args.authorized_target,
                       allow_execute=args.allow_execute, allow_mutate=args.allow_mutate,
                       allow_destructive=args.allow_destructive)
        validate_mcp_arguments(tool.input_schema, arguments)
        result = await asyncio.wait_for(call_tool(session, args.tool, arguments), timeout=args.timeout)
        identity = getattr(session, 'server_info', None)
        mapped = map_tool(tool)
        normalized = normalize_result(
            provider_id=args.provider, tool=tool, result=result, target=target,
            operation=mapped[0].capability_id if mapped else 'unknown', inputs=arguments,
            representation=args.representation, provider_version=getattr(identity, 'version', None),
            native_tool_version=None, workspace=args.workspace,
            store_raw=getattr(args, 'store_raw', False),
        )
        return observation_to_dict(normalized)


def cmd_call(args: argparse.Namespace) -> int:
    value = asyncio.run(_call(args))
    if args.workspace:
        CorpusStore(args.workspace).add_observation(value)
    write_output(value, args.output)
    return 0 if value['status'] == 'success' else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='re-skill', description='Evidence-driven RE Tool Plane')
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('system-probe', help='Offline PATH inventory: DOES NOT start tools'); p.add_argument('--output'); p.set_defaults(func=cmd_system_probe)
    p = sub.add_parser('doctor', help='Offline provider preflight: DOES NOT start tools'); p.add_argument('--config', required=True); p.set_defaults(func=cmd_doctor)
    p = sub.add_parser('discover', help='LIVE MCP handshake/list-tools; launches configured providers');
    p.add_argument('--config', required=True); p.add_argument('--registry', required=True)
    p.add_argument('--output'); p.add_argument('--timeout', type=float, default=20.0)
    p.add_argument('--wire', action='store_true', help='Limited legacy stdio client for offline fixtures only')
    p.set_defaults(func=cmd_discover)
    p = sub.add_parser('triage', help='Read-only file identification (never executes input)'); p.add_argument('--file', required=True)
    p.add_argument('--route', action='store_true'); p.add_argument('--max-size', type=int, default=512*1024**2)
    p.add_argument('--output'); p.set_defaults(func=cmd_triage)
    p = sub.add_parser('route'); p.add_argument('--input', required=True); p.set_defaults(func=cmd_route)
    p = sub.add_parser('select'); p.add_argument('--config', required=True); p.add_argument('--registry', required=True)
    p.add_argument('--discovery', required=True); p.add_argument('--capability', required=True); p.set_defaults(func=cmd_select)
    p = sub.add_parser('host-inventory'); p.add_argument('--input', required=True); p.set_defaults(func=cmd_host)
    p = sub.add_parser('call', help='LIVE MCP tool invocation with separate authorization gates')
    p.add_argument('--config', required=True); p.add_argument('--registry', required=True)
    p.add_argument('--provider', required=True); p.add_argument('--tool', required=True)
    p.add_argument('--arguments', default='{}'); p.add_argument('--arguments-file'); p.add_argument('--target', default='{}'); p.add_argument('--target-file')
    p.add_argument('--representation'); p.add_argument('--workspace'); p.add_argument('--output')
    p.add_argument('--store-raw', action='store_true',
                   help='Opt-in: store unredacted MCP response locally; may contain secrets or proprietary code')
    p.add_argument('--timeout', type=float, default=60.0, help='Maximum live MCP tool call time (seconds)')
    p.add_argument('--wire', action='store_true', help='Use constrained stdio JSON-RPC transport (testing/labs)')
    p.add_argument('--authorized-target', action='store_true'); p.add_argument('--allow-execute', action='store_true')
    p.add_argument('--allow-mutate', action='store_true'); p.add_argument('--allow-destructive', action='store_true')
    p.set_defaults(func=cmd_call)
    p = sub.add_parser('validate-jsonl'); p.add_argument('--jsonl', required=True); p.add_argument('--schema', required=True); p.set_defaults(func=cmd_validate)
    p = sub.add_parser('regress'); p.add_argument('--file', required=True); p.add_argument('--output'); p.add_argument('--strict', action='store_true', help='Exit non-zero for PARTIAL/MANUAL as well as FAIL'); p.set_defaults(func=cmd_regression)
    p = sub.add_parser('workspace-init'); p.add_argument('--path', required=True); p.set_defaults(func=cmd_workspace)
    p = sub.add_parser('case-query'); p.add_argument('--workspace', required=True); p.add_argument('--platform'); p.add_argument('--protector'); p.add_argument('--architecture'); p.set_defaults(func=cmd_case)
    p = sub.add_parser('case-similar'); p.add_argument('--workspace', required=True); p.add_argument('--input', required=True); p.add_argument('--limit', type=int, default=10); p.set_defaults(func=cmd_similar)
    p = sub.add_parser('graph-trace'); p.add_argument('--workspace', required=True); p.add_argument('--node', required=True); p.add_argument('--depth', type=int, default=2); p.set_defaults(func=cmd_graph)
    p = sub.add_parser('graph-repair', help='Inspect and optionally repair missing graph nodes from existing records')
    p.add_argument('--workspace', required=True); p.add_argument('--apply', action='store_true')
    p.set_defaults(func=cmd_graph_repair)
    p = sub.add_parser('ingest'); p.add_argument('--workspace', required=True); p.add_argument('--kind', choices=['case','compatibility','observation','node'], required=True); p.add_argument('--input', required=True); p.set_defaults(func=cmd_ingest)
    p = sub.add_parser('adapter-plan'); p.add_argument('--discovery',required=True); p.add_argument('--profiles',required=True); p.add_argument('--provider',required=True); p.add_argument('--intent',required=True); p.set_defaults(func=cmd_adapter_plan)
    p = sub.add_parser('diagnose'); p.add_argument('--symptom', required=True); p.add_argument('--known', nargs='*', default=[]); p.set_defaults(func=cmd_diagnose)
    p = sub.add_parser('promote-check'); p.add_argument('--workspace', required=True); p.add_argument('--case', required=True); p.set_defaults(func=cmd_promote_check)
    return parser


def main() -> int:
    try:
        args = build_parser().parse_args()
        return args.func(args)
    except ValidationError:
        # jsonschema exceptions can embed literal user arguments and secrets.
        print('ValidationError: MCP arguments do not match the advertised tool schema')
        return 3
    except (SecurityPolicyError, ValueError, KeyError, FileNotFoundError, RuntimeError, TimeoutError) as exc:
        # Do not accidentally print detailed user-supplied arguments in exceptions.
        public_message = str(exc) if isinstance(exc, (RuntimeError, TimeoutError, FileNotFoundError)) else str(exc)[:300]
        print(f'{type(exc).__name__}: {public_message}')
        return 3

if __name__ == '__main__':
    raise SystemExit(main())
