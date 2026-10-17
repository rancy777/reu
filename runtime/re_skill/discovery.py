from __future__ import annotations

import asyncio
from typing import Any

from .capabilities import map_tool
from .mcp_client import connect, list_all_tools, server_identity, tool_to_descriptor
from .models import ProviderHealth, ProviderSpec, ToolDescriptor
from .provider_policy import require_approved_provider


async def discover_one(
    spec: ProviderSpec,
    registry_entry: dict[str, Any] | None = None,
    timeout: float = 20.0,
    *, prefer_wire: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    registry_caps = list((registry_entry or {}).get("capabilities", []))
    try:
        # Do this check BEFORE starting an MCP subprocess or opening an HTTP session.
        require_approved_provider(spec.provider_id, {spec.provider_id: registry_entry} if registry_entry else {})
        async def work() -> dict[str, Any]:
            async with connect(spec, prefer_wire=prefer_wire) as session:
                checks.append({"name": "initialize", "status": "pass", "observation": "MCP session established"})
                ident = server_identity(session)
                checks.append({"name": "server_identity", "status": "pass", "observation": ident})

                tools_raw = await list_all_tools(session)
                descriptors = [tool_to_descriptor(t) for t in tools_raw]
                checks.append({
                    "name": "list_tools",
                    "status": "pass",
                    "observation": f"{len(descriptors)} tools discovered",
                })

                capabilities: list[dict[str, Any]] = []
                for td in descriptors:
                    tool = ToolDescriptor(
                        name=td["name"],
                        title=td["title"],
                        description=td["description"],
                        input_schema=td["input_schema"],
                        annotations=td["annotations"],
                    )
                    matches = map_tool(tool, registry_caps)
                    capabilities.append({
                        "tool": td["name"],
                        "title": td["title"],
                        "capabilities": [
                            {
                                "capability_id": m.capability_id,
                                "confidence": m.confidence,
                                "reasons": m.reasons,
                                "side_effect_class": m.side_effect_class,
                            }
                            for m in matches
                        ],
                    })

                health = ProviderHealth(
                    provider_id=spec.provider_id,
                    status="healthy" if descriptors else "degraded",
                    protocol_version=getattr(session, "protocol_version", None),
                    server_name=ident["name"],
                    server_version=ident["version"],
                    capabilities=sorted({
                        m["capability_id"]
                        for t in capabilities
                        for m in t["capabilities"]
                    }),
                    tool_count=len(descriptors),
                    checks=checks,
                )
                return {
                    "provider": {
                        "id": spec.provider_id,
                        "transport": spec.transport,
                    },
                    "health": {
                        "provider_id": health.provider_id,
                        "status": health.status,
                        "protocol_version": health.protocol_version,
                        "server_name": health.server_name,
                        "server_version": health.server_version,
                        "capabilities": health.capabilities,
                        "tool_count": health.tool_count,
                        "checks": health.checks,
                        "error": health.error,
                    },
                    "tools": descriptors,
                    "tool_capabilities": capabilities,
                }

        return await asyncio.wait_for(work(), timeout=timeout)
    except Exception as exc:
        checks.append({"name": "provider", "status": "fail", "observation": f"{type(exc).__name__}: {exc}"})
        return {
            "provider": {"id": spec.provider_id, "transport": spec.transport},
            "health": {
                "provider_id": spec.provider_id,
                "status": "unavailable",
                "protocol_version": None,
                "server_name": None,
                "server_version": None,
                "capabilities": [],
                "tool_count": 0,
                "checks": checks,
                "error": f"{type(exc).__name__}: {exc}",
            },
            "tools": [],
            "tool_capabilities": [],
        }


async def discover_all(
    specs: list[ProviderSpec],
    registry: dict[str, dict[str, Any]] | None = None,
    timeout: float = 20.0,
    *, prefer_wire: bool = False,
) -> list[dict[str, Any]]:
    # Sequential execution is intentional: it avoids launching multiple debugger
    # sessions at once and keeps provider logs/corpus writes deterministic.
    results = []
    for spec in specs:
        results.append(await discover_one(spec, (registry or {}).get(spec.provider_id), timeout, prefer_wire=prefer_wire))
    return results
