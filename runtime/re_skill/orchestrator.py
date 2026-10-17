from __future__ import annotations

from typing import Any

from .capabilities import map_tool
from .config import load_provider_specs, load_registry
from .discovery import discover_all
from .models import ProviderSpec
from .router import route_target
from .selection import independent_modalities, rank_providers


class RESkillRuntime:
    """Small runtime facade for an Agent host.

    The runtime does not install third-party tools. It discovers configured MCP
    providers, maps their live tool schemas to semantic capabilities, performs
    a non-destructive health probe, and selects providers for the requested
    capability.
    """

    def __init__(self, provider_config: str, registry_path: str):
        self.provider_config = provider_config
        self.registry_path = registry_path
        self.registry = load_registry(registry_path)
        self.specs = load_provider_specs(provider_config)
        self.discovery: list[dict[str, Any]] = []

    async def discover(self, timeout: float = 20.0) -> list[dict[str, Any]]:
        self.discovery = await discover_all(self.specs, self.registry, timeout)
        return self.discovery

    def select(self, capability: str) -> dict[str, Any]:
        ranked = rank_providers(capability, self.registry, self.discovery)
        return {
            "capability": capability,
            "ranked": ranked,
            "independent_modalities": independent_modalities(ranked),
        }

    @staticmethod
    def route(triage: dict[str, Any]) -> dict[str, Any]:
        return route_target(triage)
