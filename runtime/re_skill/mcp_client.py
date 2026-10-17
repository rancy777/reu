"""MCP transport selector: official SDK v2 when installed; constrained stdio fallback."""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

from .models import ProviderSpec
from .security import validate_provider_spec


def build_client(spec: ProviderSpec, *, prefer_wire: bool = False) -> Any:
    validate_provider_spec(spec)
    if prefer_wire and spec.transport == 'stdio':
        from .mcp_wire import StdioWireClient
        return StdioWireClient(spec)
    try:
        from mcp import Client, StdioServerParameters
    except ImportError as exc:
        raise RuntimeError(
            'Official MCP SDK v2 is not installed; install the runtime with [mcp]. '
            'The limited legacy stdio client is opt-in via --wire for isolated fixtures only.'
        ) from exc
    if spec.transport == 'sse':
        return _legacy_sse_client(spec.url)
    if spec.transport == 'stdio':
        return Client(StdioServerParameters(command=spec.command, args=spec.args,
                                           env=spec.env or None, cwd=spec.cwd))
    if spec.headers:
        try:
            import httpx2
            from mcp.client.streamable_http import streamable_http_client
        except ImportError as exc:
            raise RuntimeError('Authenticated HTTP requires MCP SDK v2 HTTP dependencies') from exc
        http_client = httpx2.AsyncClient(
            headers=spec.headers,
            timeout=httpx2.Timeout(timeout=30.0, read=300.0),
        )
        return _HttpClientContext(
            Client(streamable_http_client(spec.url, http_client=http_client)), http_client,
        )
    return Client(spec.url)


@asynccontextmanager
async def _legacy_sse_client(url: str) -> AsyncIterator[Any]:
    """Bridge old local SSE streams to the SDK v2 ClientSession.

    The v2 high-level Client does not accept ``sse_client(url)`` directly:
    that helper yields (read, write) streams, not an SDK Transport.
    """
    from mcp import ClientSession
    from mcp.client.sse import sse_client

    async with sse_client(url) as (read, write):
        async with ClientSession(read, write) as session:
            initialized = await session.initialize()
            yield _LegacySessionFacade(session, initialized)


class _LegacySessionFacade:
    """Normalizes the v2 ClientSession cursor interface to Client API."""

    def __init__(self, session: Any, initialized: Any):
        self._session = session
        self.server_info = getattr(initialized, 'server_info', None)
        self.protocol_version = getattr(initialized, 'protocol_version', None)

    async def list_tools(self, cursor: str | None = None) -> Any:
        from mcp.types import PaginatedRequestParams
        if cursor is None:
            return await self._session.list_tools()
        return await self._session.list_tools(params=PaginatedRequestParams(cursor=cursor))

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        return await self._session.call_tool(name, arguments)


class _HttpClientContext:
    def __init__(self, client: Any, http_client: Any):
        self.client = client
        self.http_client = http_client

    async def __aenter__(self) -> Any:
        await self.http_client.__aenter__()
        try:
            return await self.client.__aenter__()
        except BaseException:
            await self.http_client.__aexit__(None, None, None)
            raise

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> Any:
        try:
            return await self.client.__aexit__(exc_type, exc, tb)
        finally:
            await self.http_client.__aexit__(exc_type, exc, tb)


@asynccontextmanager
async def connect(spec: ProviderSpec, *, prefer_wire: bool = False) -> AsyncIterator[Any]:
    async with build_client(spec, prefer_wire=prefer_wire) as session:
        yield session


async def list_all_tools(session: Any) -> list[Any]:
    all_tools: list[Any] = []
    seen: set[str] = set()
    cursor: str | None = None
    tool_names: set[str] = set()
    for _ in range(128):
        page = await session.list_tools(cursor=cursor)
        for tool in page.tools:
            name = getattr(tool, 'name', None)
            if not isinstance(name, str) or not name:
                raise RuntimeError('MCP tool without valid name')
            if name in tool_names:
                raise RuntimeError(f'MCP duplicate tool name across pages: {name}')
            tool_names.add(name)
            all_tools.append(tool)
            if len(all_tools) > 4096:
                raise RuntimeError('MCP server exposes too many tools (limit 4096)')
        cursor = getattr(page, 'next_cursor', None)
        if not cursor:
            return all_tools
        if cursor in seen:
            raise RuntimeError('MCP tool pagination cursor loop detected')
        seen.add(cursor)
    raise RuntimeError('MCP tool listing exceeds 128 pages')


def tool_to_descriptor(tool: Any) -> dict[str, Any]:
    def model_dump(value: Any) -> Any:
        if hasattr(value, 'model_dump'):
            return value.model_dump(mode='json', exclude_none=True)
        return value
    schema = model_dump(getattr(tool, 'input_schema', None))
    if not isinstance(schema, dict) or not schema:
        raise RuntimeError('Discovered MCP tool has no valid inputSchema')
    return {
        'name': str(getattr(tool, 'name', '')),
        'title': getattr(tool, 'title', None),
        'description': str(getattr(tool, 'description', '') or ''),
        'input_schema': schema,
        'annotations': model_dump(getattr(tool, 'annotations', {}) or {}),
    }


def server_identity(session: Any) -> dict[str, Any]:
    info = getattr(session, 'server_info', None)
    return {'name': getattr(info, 'name', None), 'version': getattr(info, 'version', None)}


async def call_tool(session: Any, name: str, arguments: dict[str, Any] | None = None) -> Any:
    return await session.call_tool(name, arguments or {})
