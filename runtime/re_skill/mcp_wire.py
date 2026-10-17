"""Constrained MCP JSON-RPC stdio client for offline lab/testing.

Production hosts should prefer the official MCP Python SDK. This fallback only
implements initialize, tools/list, tools/call, and ping. No resources, sampling,
elicitation, progress streams or HTTP. It does NOT execute arbitrary shell text:
provider commands are pre-approved argv and spawn with shell=False.
"""
from __future__ import annotations

import asyncio
import json
import os
from types import SimpleNamespace
from typing import Any

from .models import ProviderSpec

MAX_LINE = 16 * 1024 * 1024


class WireProtocolError(RuntimeError):
    pass


def _ns(value: dict[str, Any]) -> SimpleNamespace:
    return SimpleNamespace(**value)


class StdioWireClient:
    def __init__(self, spec: ProviderSpec, timeout: float = 15.0):
        self.spec = spec
        self.timeout = timeout
        self.process: asyncio.subprocess.Process | None = None
        self.server_info: Any = None
        self.protocol_version: str | None = None
        self._next_id = 0
        self._stderr_task: asyncio.Task | None = None
        self._stderr = bytearray()

    async def __aenter__(self) -> 'StdioWireClient':
        env_keys = ('PATH', 'HOME', 'USER', 'LOGNAME', 'TMP', 'TEMP', 'SYSTEMROOT', 'COMSPEC')
        env = {k: os.environ[k] for k in env_keys if k in os.environ}
        env.update(self.spec.env)
        self.process = await asyncio.create_subprocess_exec(
            self.spec.command, *self.spec.args, stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
            cwd=self.spec.cwd, env=env, limit=MAX_LINE,
        )
        self._stderr_task = asyncio.create_task(self._drain_stderr())
        try:
            init = await self._request('initialize', {
                'protocolVersion': '2025-06-18', 'capabilities': {},
                'clientInfo': {'name': 'reverse-engineering-unpacking', 'version': '1.5.0'},
            })
            self.server_info = _ns(init.get('serverInfo', {}))
            self.protocol_version = init.get('protocolVersion')
            await self._send({'jsonrpc': '2.0', 'method': 'notifications/initialized'})
            return self
        except BaseException:
            await self.__aexit__(None, None, None)
            raise

    async def _drain_stderr(self) -> None:
        assert self.process and self.process.stderr
        while data := await self.process.stderr.read(8192):
            if len(self._stderr) < 64 * 1024:
                self._stderr.extend(data[:64*1024 - len(self._stderr)])

    async def _send(self, payload: dict[str, Any]) -> None:
        if not self.process or not self.process.stdin:
            raise WireProtocolError('server not running')
        raw = (json.dumps(payload, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8')
        if len(raw) > MAX_LINE:
            raise WireProtocolError('MCP request exceeds size limit')
        self.process.stdin.write(raw)
        await self.process.stdin.drain()

    async def _request(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        assert self.process and self.process.stdout
        self._next_id += 1
        identifier = self._next_id
        await self._send({'jsonrpc': '2.0', 'id': identifier, 'method': method, 'params': params})
        deadline = asyncio.get_running_loop().time() + self.timeout
        while True:
            try:
                remaining = deadline - asyncio.get_running_loop().time()
                if remaining <= 0:
                    raise asyncio.TimeoutError(f'MCP {method} exceeded total timeout')
                raw = await asyncio.wait_for(self.process.stdout.readline(), timeout=remaining)
            except asyncio.LimitOverrunError as exc:
                raise WireProtocolError('MCP response too large') from exc
            if not raw:
                raise WireProtocolError(f'MCP server exited during {method}: returncode={self.process.returncode}')
            if len(raw) > MAX_LINE:
                raise WireProtocolError('MCP response exceeds size limit')
            try:
                msg = json.loads(raw)
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise WireProtocolError('MCP stdout contained invalid JSON-RPC') from exc
            if msg.get('id') != identifier:
                # MCP server notifications and ping requests are legal during calls.
                if msg.get('method') == 'ping' and 'id' in msg:
                    await self._send({'jsonrpc': '2.0', 'id': msg['id'], 'result': {}})
                elif msg.get('method') and 'id' in msg:
                    await self._send({'jsonrpc': '2.0', 'id': msg['id'], 'error': {'code': -32601, 'message': 'Unsupported client method'}})
                elif 'id' in msg and 'result' in msg:
                    raise WireProtocolError('unexpected response id')
                continue
            if msg.get('jsonrpc') != '2.0':
                raise WireProtocolError('unsupported JSON-RPC envelope')
            if 'error' in msg:
                raise WireProtocolError(f'MCP {method} error: {msg["error"]}')
            result = msg.get('result', {})
            if not isinstance(result, dict):
                raise WireProtocolError('MCP result must be an object')
            return result

    async def list_tools(self, *, cursor: str | None = None) -> Any:
        response = await self._request('tools/list', {'cursor': cursor} if cursor is not None else {})
        tools = []
        for row in response.get('tools', []):
            tools.append(_ns({
                'name': row.get('name', ''), 'title': row.get('title'),
                'description': row.get('description', ''), 'input_schema': row.get('inputSchema', {}),
                'annotations': row.get('annotations', {}),
            }))
        return _ns({'tools': tools, 'next_cursor': response.get('nextCursor')})

    async def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> Any:
        result = await self._request('tools/call', {'name': name, 'arguments': arguments or {}})
        return _ns({
            'structured_content': result.get('structuredContent'),
            'content': result.get('content', []),
            'is_error': result.get('isError', False),
        })

    async def __aexit__(self, *_exc: Any) -> None:
        proc = self.process
        if not proc:
            return
        if proc.stdin and not proc.stdin.is_closing():
            proc.stdin.close()
        try:
            await asyncio.wait_for(proc.wait(), timeout=1)
        except asyncio.TimeoutError:
            proc.terminate()
            try:
                await asyncio.wait_for(proc.wait(), timeout=2)
            except asyncio.TimeoutError:
                proc.kill()
                await proc.wait()
        if self._stderr_task:
            try:
                await asyncio.wait_for(self._stderr_task, timeout=2)
            except asyncio.TimeoutError:
                self._stderr_task.cancel()
        self.process = None
