"""Bounded MCP tool argument validation; never resolve third-party remote schema refs.

The MCP server advertises this schema, but it is untrusted input. Fail closed
for capabilities that require potentially unbounded regexp or reference
resolution. A provider requiring these needs an independently reviewed adapter.
"""
from __future__ import annotations
import json
from typing import Any

from jsonschema import Draft202012Validator

MAX_SCHEMA_BYTES = 512 * 1024
MAX_ARGS_BYTES = 1024 * 1024
MAX_DEPTH = 24
MAX_NODES = 8192
UNSAFE_KEYWORDS = frozenset({'$ref', '$dynamicRef', '$recursiveRef', 'pattern', 'patternProperties'})

class UnsafeToolSchema(ValueError):
    pass


def _bound_structure(value: Any, *, max_nodes: int, max_depth: int) -> None:
    stack = [(value, 0)]
    visited = 0
    while stack:
        item, depth = stack.pop()
        visited += 1
        if visited > max_nodes or depth > max_depth:
            raise UnsafeToolSchema('MCP schema/input exceeds safety complexity limit')
        if isinstance(item, dict):
            stack.extend((k, depth+1) for k in item.keys())
            stack.extend((v, depth+1) for v in item.values())
        elif isinstance(item, (list, tuple)):
            stack.extend((x, depth+1) for x in item)


def validate_mcp_arguments(schema: dict[str, Any], arguments: dict[str, Any]) -> None:
    if not isinstance(schema, dict) or not schema:
        raise UnsafeToolSchema('MCP tool has no valid object inputSchema')
    if not isinstance(arguments, dict):
        raise UnsafeToolSchema('MCP tool arguments must be JSON object')
    if schema.get('type') != 'object':
        raise UnsafeToolSchema('MCP tool inputSchema must declare top-level object type')
    schema_raw = json.dumps(schema, ensure_ascii=False, allow_nan=False)
    args_raw = json.dumps(arguments, ensure_ascii=False, allow_nan=False)
    if len(schema_raw.encode('utf-8')) > MAX_SCHEMA_BYTES:
        raise UnsafeToolSchema('MCP inputSchema is too large for automated validation')
    if len(args_raw.encode('utf-8')) > MAX_ARGS_BYTES:
        raise UnsafeToolSchema('MCP tool arguments exceed 1 MiB safety cap')
    _bound_structure(schema, max_nodes=MAX_NODES, max_depth=MAX_DEPTH)
    _bound_structure(arguments, max_nodes=MAX_NODES, max_depth=MAX_DEPTH)
    stack = [schema]
    while stack:
        item = stack.pop()
        if isinstance(item, dict):
            keys = set(item)
            bad = keys & UNSAFE_KEYWORDS
            if bad:
                raise UnsafeToolSchema(
                    'MCP inputSchema contains reference/regexp keywords requiring manual adapter review: '
                    + ', '.join(sorted(bad))
                )
            stack.extend(item.values())
        elif isinstance(item,list):
            stack.extend(item)
    Draft202012Validator.check_schema(schema)
    # No external refs; they were rejected above. Validation neither executes
    # arbitrary code nor dereferences external schema resources.
    Draft202012Validator(schema).validate(arguments)
