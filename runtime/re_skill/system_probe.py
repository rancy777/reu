"""Safe OS/PATH capability inventory: never launches a provider or target."""
from __future__ import annotations

import importlib.util
import platform
import shutil
import sys
from typing import Any

BINARIES = {
    'ida': ('ida64', 'ida'), 'ghidra-headless': ('analyzeHeadless', 'analyzeHeadless.bat'),
    'radare2': ('r2',), 'x64dbg': ('x64dbg', 'x64dbg.exe', 'x32dbg.exe'),
    'windbg': ('windbg', 'windbg.exe', 'cdb.exe'), 'frida': ('frida',),
    'adb': ('adb',), 'jadx': ('jadx', 'jadx.bat'),
    'apktool': ('apktool', 'apktool.bat'), 'bundletool': ('bundletool',),
    'yara': ('yara', 'yara64'), 'capa': ('capa',), 'floss': ('floss',),
    'diec': ('diec',), 'pefile-python': ('python', 'python3'),
    'docker': ('docker',),
}


def system_probe() -> dict[str, Any]:
    tools = {}
    for name, candidates in BINARIES.items():
        resolved = next(((candidate, shutil.which(candidate)) for candidate in candidates if shutil.which(candidate)), None)
        tools[name] = {'found_on_path': bool(resolved),
                       'executable_name': resolved[0] if resolved else None,
                       'path': resolved[1] if resolved else None,
                       'version': 'Not checked', 'health': 'Not checked'}
    sdk = importlib.util.find_spec('mcp') is not None
    return {'host_os': platform.system(), 'architecture': platform.machine(),
            'python_version': sys.version.split()[0], 'tools': tools,
            'official_mcp_sdk_importable': sdk,
            'actual_provider_handshakes_performed': False,
            'side_effects': 'None: PATH and Python module metadata only',
            'notes': 'A detected PATH entry does not prove a valid version, MCP integration or executable safety.'}
