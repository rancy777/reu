"""Conservative, name-first semantic tool classification.

Discovered names, descriptions and annotations are UNTRUSTED. A provider may
claim a tool is read-only; only an explicit known safe verb receives 'observe'.
For stateful actions, risk is classified by name and never downgraded by text.
"""
from __future__ import annotations

import re
from typing import Any
from .models import CapabilityMatch, ToolDescriptor

RULES = [
    (r'\b(decompile|decompiler|pseudocode)\b', 'decompiler', .96),
    (r'\b(xref|cross reference|references)\b', 'static.xrefs', .94),
    (r'\b(callgraph|call graph)\b', 'static.callgraph', .92),
    (r'\b(functions|function|symbols)\b', 'static.functions', .86),
    (r'\b(sections|segments|headers|imports|exports|metadata)\b', 'static.metadata', .87),
    (r'\b(strings|floss)\b', 'strings', .9),
    (r'\b(breakpoint|breakpoints)\b', 'runtime.breakpoints', .9),
    (r'\b(attach|detach)\b', 'runtime.attach', .9),
    (r'\b(spawn|launch|start process)\b', 'runtime.spawn', .87),
    (r'\b(resume|continue)\b', 'runtime.resume', .86),
    (r'\b(step|single step)\b', 'runtime.step', .85),
    (r'\b(register|registers)\b', 'runtime.registers', .86),
    (r'\b(memory|hexdump|read bytes)\b', 'runtime.memory-read', .84),
    (r'\b(scan memory|memory scan|pattern scan)\b', 'runtime.memory-search', .9),
    (r'\b(modules|module|libraries)\b', 'runtime.modules', .86),
    (r'\b(trace|tracing)\b', 'runtime.trace', .85),
    (r'\b(dump|capture memory)\b', 'reconstruct.dump', .86),
    (r'\b(import reconstruction|rebuild imports|iat repair)\b', 'reconstruct.imports', .96),
    (r'\b(relocations|relocation)\b', 'reconstruct.relocations', .92),
    (r'\b(manifest|apk|android package)\b', 'android.package', .91),
    (r'\b(aab|split apk|splits|bundletool)\b', 'android.splits', .9),
    (r'\b(dex|odex|vdex|oat)\b', 'android.dex', .9),
    (r'\b(class|classes|smali|methods)\b', 'android.class-search', .84),
    (r'\b(logcat)\b', 'android.logcat', .96),
    (r'\b(adb|android device|emulator)\b', 'android.device', .9),
    (r'\b(frida|hook|instrumentation)\b', 'android.instrumentation', .88),
    (r'\b(jni|native method|register natives)\b', 'android.native-jni', .91),
    (r'\b(elf|shared object|native library)\b', 'native.elf', .85),
    (r'\b(emulate|emulation|symbolic execution)\b', 'emulation', .92),
    (r'\b(yara|capa|apkid|rules)\b', 'rule-scanning', .9),
    (r'\b(hash|sha256|digest)\b', 'evidence.hash', .9),
    (r'\b(identify|file type|file format)\b', 'target.identify', .86),
]

WRITE_RE = re.compile(r'\b(write|set|modify|patch|rename|retype|save|create|insert|edit|change|hook|inject|compile|build|dump|fix|rebuild|install|upload|download|export|connect)\b')
EXEC_RE = re.compile(r'\b(attach|spawn|launch|run|execute|resume|continue|step|debug|trace|emulate|restart|start|load|unpack|invoke)\b')
DELETE_RE = re.compile(r'\b(delete|remove|terminate|kill|uninstall|overwrite|wipe|format disk)\b')
READ_RE = re.compile(r'^(get|read|list|find|search|scan|query|inspect|analyze|analyse|decompile|disassemble|xref|hash|describe|enumerate|show|parse|detect|identify|lookup|info|ping|health|status)\b')


def _tokens(s: str) -> str:
    s = re.sub(r'(?<=[a-z0-9])(?=[A-Z])', ' ', s)
    return re.sub(r'[_\-./]+', ' ', s.lower()).strip()


def side_effect_class(tool: ToolDescriptor) -> str:
    name = _tokens(tool.name)
    ann = tool.annotations or {}
    if not isinstance(ann, dict):
        ann = ann.model_dump(exclude_none=True) if hasattr(ann, 'model_dump') else {}
    if name in {'analyze file', 'run tool', 'decode apk'}:
        return 'execute' if name != 'decode apk' else 'mutate'
    if DELETE_RE.search(name) or ann.get('destructiveHint') is True or ann.get('destructive_hint') is True:
        return 'destructive'
    if WRITE_RE.search(name):
        return 'mutate'
    if EXEC_RE.search(name):
        return 'execute'
    # A textual description or self-reported readOnlyHint does not grant read permissions.
    if READ_RE.search(name):
        return 'observe'
    return 'unknown'


def map_tool(tool: ToolDescriptor, provider_capabilities: list[str] | None = None) -> list[CapabilityMatch]:
    # Descriptions help map semantic intent, not authorization.
    name = _tokens(tool.name)
    supplementary = _tokens(f'{tool.title or ""} {tool.description or ""}')
    matches: dict[str, CapabilityMatch] = {}
    side = side_effect_class(tool)
    for pattern, capability, conf in RULES:
        if re.search(pattern, name):
            matches[capability] = CapabilityMatch(capability, conf, [f'live tool name pattern: {pattern}'], side)
        elif re.search(pattern, supplementary):
            # Untrusted description is only a research hint (< automatic selection threshold).
            matches[capability] = CapabilityMatch(capability, .40, [f'unverified description pattern: {pattern}'], side)
    # Expand only a proved operation into umbrella classifications.
    aliases = {
        'static.metadata': ['pe.static'], 'static.functions': ['pe.static'],
        'static.xrefs': ['pe.static'], 'decompiler': ['pe.static'],
        'android.package': ['android.package'], 'android.dex': ['android.dex'],
        'runtime.memory-read': ['pe.memory'], 'runtime.breakpoints': ['pe.runtime'],
    }
    for matched in list(matches):
        for umbrella in aliases.get(matched, []):
            if umbrella not in matches:
                inherited = min(.65, matches[matched].confidence)
                matches[umbrella] = CapabilityMatch(umbrella, inherited, [f'derived from observed {matched} tool operation'], side)
    # Registry capability declarations are ONLY used to filter the matches, never mint one.
    return sorted(matches.values(), key=lambda m: (-m.confidence, m.capability_id))
