from __future__ import annotations

from typing import Any

from .capabilities import map_tool
from .models import ToolDescriptor


def normalize_host_inventory(inventory: dict[str, Any]) -> dict[str, Any]:
    """Normalize an Agent-provided MCP inventory without opening new connections.

    Expected input is intentionally host-neutral:
    {
      "servers": [
        {
          "id": "...",
          "server_name": "...",
          "server_version": "...",
          "protocol_version": "...",
          "tools": [
             {"name": "...", "description": "...", "input_schema": {}, "annotations": {}}
          ]
        }
      ]
    }
    """
    result = []
    for server in inventory.get("servers", []):
        provider_id = str(server.get("id") or server.get("server_name") or "unknown")
        tools = []
        for raw in server.get("tools", []):
            tool = ToolDescriptor(
                name=str(raw.get("name", "")),
                title=raw.get("title"),
                description=str(raw.get("description", "")),
                input_schema=raw.get("input_schema") or raw.get("inputSchema") or {},
                annotations=raw.get("annotations") or {},
            )
            matches = map_tool(tool, server.get("capabilities", []))
            tools.append({
                "name": tool.name,
                "capabilities": [
                    {
                        "capability_id": m.capability_id,
                        "confidence": m.confidence,
                        "side_effect_class": m.side_effect_class,
                        "reasons": m.reasons,
                    }
                    for m in matches
                ],
            })
        result.append({
            "provider_id": provider_id,
            "server_name": server.get("server_name"),
            "server_version": server.get("server_version"),
            "protocol_version": server.get("protocol_version"),
            "tools": tools,
        })
    return {"servers": result}
