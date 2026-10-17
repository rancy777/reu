"""Provider-specific intent -> *live-discovered* tool binding; no invented input args."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from .capabilities import side_effect_class
from .models import ToolDescriptor


def load_adapter_profiles(path: str | Path) -> dict[str, dict[str, Any]]:
    data=json.loads(Path(path).read_text(encoding='utf-8'))
    return {p['provider_id']:p for p in data['profiles']}


def adapter_plan(discovered: dict[str, Any], provider: str, intent: str,
                 profile: dict[str, Any] | None = None) -> dict[str, Any]:
    target = next((r for r in discovered.get('providers', []) if r.get('provider', {}).get('id') == provider), None)
    if not target or target.get('health',{}).get('status') != 'healthy':
        return {'status': 'no-healthy-provider', 'provider':provider, 'intent':intent, 'candidates':[]}
    names = set((profile or {}).get('mapping', {}).get(intent, []))
    matches = []
    for t in target.get('tools', []):
        if t.get('name') not in names: continue
        effect = side_effect_class(ToolDescriptor(name=t['name'], title=t.get('title'),
                                                    description=t.get('description',''),
                                                    input_schema=t.get('input_schema') or {}, annotations=t.get('annotations') or {}))
        matches.append({'tool': t['name'], 'input_schema': t.get('input_schema'),
                        'risk': effect, 'arguments': 'fill from live input_schema, never infer',
                        'source': (profile or {}).get('repository')})
    return {'status': 'ready-to-plan' if matches else 'unmapped-or-schema-changed',
            'provider':provider, 'intent':intent, 'candidates':matches,
            'note': 'Requires explicit permission and a separate LIVE call. No tool was invoked.'}
