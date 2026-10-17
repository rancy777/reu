"""Release-curated, explicit provider execution allow-list.

A registry entry is an *administrative* decision to permit launching a
specific process. It is not evidence that its runtime descriptions are true.
"""
from __future__ import annotations
from typing import Any

from .security import SecurityPolicyError

ALLOWED_PROVIDER_STATUSES = frozenset({
    'recommended', 'candidate-recommended', 'candidate', 'experimental',
    'optional', 'optional-recommended', 'host-dependent',
    'recommended-when-emulation-fits', 'recommended-for-android-triage',
})


def require_approved_provider(provider_id: str, registry: dict[str, dict[str, Any]]) -> dict[str, Any]:
    entry = registry.get(provider_id)
    if not isinstance(entry, dict):
        raise SecurityPolicyError(f'Provider {provider_id!r} absent from reviewed registry; do not launch')
    status = entry.get('status')
    if status not in ALLOWED_PROVIDER_STATUSES:
        raise SecurityPolicyError(f'Provider {provider_id!r} is not launch-approved: status={status!r}')
    return entry
