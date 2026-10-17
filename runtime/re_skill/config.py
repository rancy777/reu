from __future__ import annotations
import json
import os
import re
from pathlib import Path
from typing import Any
import yaml
from .models import ProviderSpec

EXACT_ENV = re.compile(r'^\$\{([A-Za-z_][A-Za-z0-9_]*)\}$')


def load_data(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    raw = p.read_text(encoding='utf-8')
    value = yaml.safe_load(raw) if p.suffix.lower() in ('.yaml','.yml') else json.loads(raw)
    if not isinstance(value, dict): raise ValueError('configuration must be an object')
    return value


def _resolve_secret(value: str) -> str:
    match = EXACT_ENV.fullmatch(value)
    if not match: return value
    name = match.group(1)
    if name not in os.environ:
        raise ValueError(f'configuration needs environment variable {name}')
    return os.environ[name]


def load_provider_specs(path: str | Path) -> list[ProviderSpec]:
    raw = load_data(path).get('providers', [])
    if not isinstance(raw, list): raise ValueError('providers must be a list')
    providers = []
    seen = set()
    for row in raw:
        if not isinstance(row, dict): raise ValueError('each provider must be an object')
        spec = ProviderSpec.from_dict(row)
        if spec.provider_id in seen: raise ValueError(f'duplicate provider id {spec.provider_id}')
        seen.add(spec.provider_id)
        spec.headers = {k: _resolve_secret(v) for k, v in spec.headers.items()}
        spec.env = {k: _resolve_secret(v) for k, v in spec.env.items()}
        providers.append(spec)
    return providers


def load_registry(path: str | Path) -> dict[str, dict[str, Any]]:
    result = {}
    for row in load_data(path).get('providers', []):
        if isinstance(row, dict) and row.get('id'):
            result[str(row['id'])] = row
    return result
