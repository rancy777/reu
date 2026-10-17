from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ProviderSpec:
    provider_id: str
    transport: str
    command: str | None = None
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    cwd: str | None = None
    url: str | None = None
    headers: dict[str, str] = field(default_factory=dict)
    enabled: bool = True
    allow_remote: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProviderSpec":
        transport = str(data.get("transport", "stdio")).lower()
        if transport in {"streamable_http", "streamable-http"}:
            transport = "http"
        return cls(
            provider_id=str(data["provider_id"] if "provider_id" in data else data["id"]),
            transport=transport,
            command=data.get("command"),
            args=[str(x) for x in data.get("args", [])],
            env={str(k): str(v) for k, v in data.get("env", {}).items()},
            cwd=data.get("cwd"),
            url=data.get("url"),
            headers={str(k): str(v) for k, v in data.get("headers", {}).items()},
            enabled=bool(data.get("enabled", True)),
            allow_remote=bool(data.get("allow_remote", False)),
            metadata=dict(data.get("metadata", {})),
        )


@dataclass(slots=True)
class ToolDescriptor:
    name: str
    title: str | None
    description: str
    input_schema: dict[str, Any]
    annotations: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class CapabilityMatch:
    capability_id: str
    confidence: float
    reasons: list[str]
    side_effect_class: str


@dataclass(slots=True)
class ProviderHealth:
    provider_id: str
    status: str
    protocol_version: str | None
    server_name: str | None
    server_version: str | None
    capabilities: list[str]
    tool_count: int
    checks: list[dict[str, Any]]
    error: str | None = None


@dataclass(slots=True)
class NormalizedObservation:
    observation_id: str
    provider_id: str
    operation: str
    native_tool: str
    target: dict[str, Any]
    representation: str | None
    status: str
    side_effect_class: str
    completeness: str
    inputs: dict[str, Any]
    output: Any
    output_sha256: str | None
    raw_output_ref: str | None
    provider_version: str | None
    native_tool_version: str | None
    derived_observations: list[str] = field(default_factory=list)
    evidence_ids: list[str] = field(default_factory=list)
