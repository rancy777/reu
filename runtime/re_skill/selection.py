"""Provider selection requires real discovered tool capability, not a registry boast."""
from __future__ import annotations
from collections import defaultdict
from typing import Any

TRUST = {'official': 100, 'official-runtime-feature': 92, 'first-party-project': 90,
         'community/AI-native distribution': 72, 'community': 65, 'community-aggregator': 50}
from .provider_policy import ALLOWED_PROVIDER_STATUSES
ALLOWED = ALLOWED_PROVIDER_STATUSES
BLOCKED = {'quarantined-by-default', 'blocked', 'unreviewed', 'disabled'}


def rank_providers(capability: str, registry: dict[str, dict[str, Any]],
                   discovered: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ranked = []
    for x in discovered:
        pid = x.get('provider', {}).get('id')
        reg = registry.get(pid, {})
        health = x.get('health', {})
        if health.get('status') != 'healthy' or reg.get('status') not in ALLOWED:
            continue
        real_matches = [
            {'tool': t.get('tool'), **m} for t in x.get('tool_capabilities', [])
            for m in t.get('capabilities', [])
            if m.get('capability_id') == capability and float(m.get('confidence', 0)) >= .65
        ]
        if not real_matches:
            continue
        score = TRUST.get(reg.get('class', ''), 40)
        score += 15 if reg.get('status') == 'recommended' else 5
        score += int(max(m['confidence'] for m in real_matches) * 15)
        if all(m.get('side_effect_class') in ('observe', 'read') for m in real_matches):
            score += 5
        ranked.append({
            'provider_id': pid, 'score': score, 'status': 'healthy',
            'class': reg.get('class'), 'native_tool': reg.get('native_tool'),
            'candidate_tools': real_matches,
            'reason': ['live tool/schema discovered', 'healthy', 'not quarantined'],
        })
    return sorted(ranked, key=lambda row: (-row['score'], row['provider_id']))


def _native_family(value: str) -> str:
    v = value.casefold().strip()
    if 'ida' in v and 'radare' not in v: return 'ida'
    if 'ghidra' in v: return 'ghidra'
    if 'radare2' in v or v == 'r2': return 'radare2'
    if 'binary ninja' in v or 'binaryninja' in v: return 'binaryninja'
    if 'frida' in v: return 'frida'
    if 'x64dbg' in v or 'x32dbg' in v: return 'x64dbg'
    return v

def independent_modalities(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in candidates:
        groups[_native_family(str(row.get('native_tool') or row['provider_id']))].append(row)
    return [{'native_tool_key': key, 'selected_provider': vals[0]['provider_id'],
             'providers': [x['provider_id'] for x in vals], 'count_as_independent_modalities': 1}
            for key, vals in groups.items()]
