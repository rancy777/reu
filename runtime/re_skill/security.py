from __future__ import annotations

import ipaddress
from urllib.parse import urlparse
from .models import ProviderSpec, ToolDescriptor

class SecurityPolicyError(RuntimeError):
    pass


def _loopback(host: str | None) -> bool:
    if not host: return False
    if host.lower() in {'localhost', 'localhost.localdomain'}: return True
    try: return ipaddress.ip_address(host.strip('[]')).is_loopback
    except ValueError: return False


def validate_provider_spec(spec: ProviderSpec) -> None:
    if not spec.enabled:
        raise SecurityPolicyError(f'{spec.provider_id}: provider disabled')
    if spec.transport == 'stdio':
        if not spec.command or spec.command.startswith('REPLACE_'):
            raise SecurityPolicyError(f'{spec.provider_id}: configure a real executable; placeholders cannot launch')
        if not isinstance(spec.args, list) or any(not isinstance(x, str) for x in spec.args):
            raise SecurityPolicyError('stdio args must be argv string list')
        # An argv command like `sh -c ...` is still a shell, even with shell=False.
        import os
        executable = os.path.basename(spec.command).casefold()
        if executable in {'sh', 'bash', 'zsh', 'fish', 'cmd', 'cmd.exe',
                          'powershell', 'powershell.exe', 'pwsh', 'pwsh.exe'}:
            raise SecurityPolicyError('shell interpreter MCP launcher blocked: use a reviewed direct executable')
        if executable in {'uvx', 'npx', 'npx.cmd', 'npm', 'npm.cmd', 'r2pm',
                          'pipx', 'pipx.exe', 'bunx', 'bunx.exe'}:
            meta = spec.metadata or {}
            if not (meta.get('allow_package_manager_launch') is True and
                    isinstance(meta.get('supply_chain_review_id'), str) and
                    len(meta['supply_chain_review_id']) >= 5):
                raise SecurityPolicyError(
                    'launcher may fetch/execute packages; install a pinned upstream release '
                    'or explicitly record a supply-chain review in provider metadata'
                )
        return
    if spec.transport == 'sse':
        parsed = urlparse(spec.url or '')
        if parsed.username or parsed.password or parsed.fragment or parsed.query:
            raise SecurityPolicyError('SSE endpoint cannot embed credentials, query or fragment')
        if parsed.scheme not in ('http','https') or not _loopback(parsed.hostname) or spec.headers:
            raise SecurityPolicyError('legacy SSE allowed only for unauthenticated loopback; use official SDK')
        return
    if spec.transport == 'http':
        parsed = urlparse(spec.url or '')
        if parsed.scheme not in ('http', 'https') or not parsed.hostname:
            raise SecurityPolicyError('MCP endpoint must be http(s) URL')
        if parsed.username or parsed.password or parsed.fragment:
            raise SecurityPolicyError('inline URL credentials or fragments forbidden')
        if parsed.query:
            raise SecurityPolicyError('query parameters in MCP URL forbidden; use explicit headers')
        if _loopback(parsed.hostname):
            return
        if not spec.allow_remote or parsed.scheme != 'https':
            raise SecurityPolicyError('remote MCP requires allow_remote=true and TLS HTTPS')
        if not spec.headers:
            raise SecurityPolicyError('remote MCP must declare explicit auth headers')
        return
    raise SecurityPolicyError(f'unsupported MCP transport: {spec.transport}')


def authorize_tool(effect: str, *, authorized_target: bool, allow_execute: bool,
                   allow_mutate: bool, allow_destructive: bool) -> None:
    if effect in {'read', 'observe'}:
        return
    if not authorized_target:
        raise SecurityPolicyError(f'{effect} tool requires --authorized-target')
    if effect == 'execute' and not allow_execute:
        raise SecurityPolicyError('execution requires --allow-execute')
    if effect == 'mutate' and not allow_mutate:
        raise SecurityPolicyError('mutation requires --allow-mutate')
    if effect == 'destructive' and not allow_destructive:
        raise SecurityPolicyError('destructive operation requires --allow-destructive')
    if effect == 'unknown':
        raise SecurityPolicyError('unknown tool risk: explicit tool review/adapter required')


# Heuristic read-only names cannot be trusted to execute freeform scripts or
# arbitrary shell commands. Such operations need a manually reviewed adapter.
COMMAND_BEARING_KEYS = frozenset({
    'command', 'cmd', 'shell', 'shell_command', 'script', 'script_code',
    'javascript', 'expression', 'eval', 'eval_code', 'python_code',
    'powershell', 'execute_command', 'device_shell', 'hook_script',
})

def authorize_read_tool_shape(tool: ToolDescriptor, effect: str) -> None:
    """Reject read-looking tools whose untrusted parameter surface can execute code."""
    if effect not in ('read', 'observe'):
        return
    stack = [tool.input_schema]
    inspected = 0
    while stack:
        item = stack.pop()
        inspected += 1
        if inspected > 8192:
            raise SecurityPolicyError('too many tool schema nodes for authorization review')
        if not isinstance(item, dict):
            if isinstance(item, list):
                stack.extend(item)
            continue
        props = item.get('properties', {})
        if isinstance(props, dict):
            found = {str(k).casefold() for k in props} & COMMAND_BEARING_KEYS
            if found:
                raise SecurityPolicyError('read-like MCP tool accepts code/command parameter; reviewed adapter required')
        stack.extend(item.values())
