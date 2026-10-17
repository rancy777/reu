"""Evidence-driven workflow routing. A suspicious indicator is not proof of packing."""
from __future__ import annotations
from typing import Any


def route_target(triage: dict[str, Any]) -> dict[str, Any]:
    name = str(triage.get('filename', '')).lower()
    fmt = str(triage.get('format', '')).lower()
    arch = str(triage.get('architecture') or 'Unknown')
    flags = {str(x.get('kind') if isinstance(x, dict) else x).lower()
             for x in triage.get('indicators', [])}
    flags |= {str(x).lower() for x in triage.get('signals', [])}
    candidate = False
    if fmt in ('aab','apks'):
        platform, workflows = 'android', ['android-triage','android-split-aab']
    elif fmt == 'apk':
        platform, workflows = 'android', ['android-triage','android-dex']
    elif fmt in ('dex','cdex','vdex','odex','oat'):
        platform, workflows = 'android', ['android-dex']
        if fmt in ('cdex', 'vdex', 'odex', 'oat'):
            workflows.append('android-art-runtime')
    elif fmt == 'elf' or fmt == 'so':
        is_android = (str(triage.get('container_platform') or '').lower() == 'android' or
                      triage.get('android_context') is True or
                      'android-so' in flags or str(triage.get('platform') or '').lower() == 'android')
        platform = 'android/native' if is_android else 'native'
        workflows = ['android-native'] if platform == 'android/native' else ['native-elf-triage']
    elif fmt in ('pe', 'pe32', 'pe32+'):
        platform, workflows = 'windows', ['windows-triage']
    elif fmt == 'unknown' and name.endswith(('.aab','.apk','.exe','.dll','.so','.dex')):
        platform, workflows = 'unknown', ['file-triage']
    else:
        platform, workflows = 'unknown', ['file-triage']
    if platform == 'windows':
        if triage.get('dotnet') is True or triage.get('clr') is True:
            workflows.append('windows-dotnet')
        else:
            if triage.get('packer') or triage.get('protector') or 'high-entropy-section' in flags:
                candidate = True
                workflows.append('windows-basic-unpacking')
            if triage.get('virtualization'):
                workflows.extend(['windows-custom-packer','windows-virtualization'])
    if platform.startswith('android'):
        if triage.get('dynamic_dex') or triage.get('in_memory_dex') or 'classloader-load-observation' in flags:
            workflows.append('android-dynamic-loading')
        if triage.get('native_protection') or triage.get('anti_hook') or triage.get('anti_frida'):
            workflows.append('android-complex-protection')
    return {'platform': platform, 'architecture': arch,
            'workflows': list(dict.fromkeys(workflows)),
            'protection_status': 'hypothesis' if candidate else 'Unknown',
            'reasons': [f'format={fmt}', f'architecture={arch}'] + sorted(flags),
            'requires_verification': (platform == 'unknown' or arch.lower() == 'unknown'),
            'next_step': 'module/split inventory' if fmt in ('aab','apks') else 'collect discriminating structural/runtime evidence'}
