"""Deterministic evidence, compatibility and failure-routing helpers.

No numerical 'probabilities' are fabricated: confidence remains categorical
until there are ground-truth experiments and calibrated data.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

FAILURES = {
    'dumped-pe-does-not-start': [
        ('imports', 'inspect import resolution and thunk targets'),
        ('section-mapping', 'compare on-disk raw and in-memory VA layouts'),
        ('relocations', 'check relocated image base and fixups'),
        ('TLS', 'inspect TLS callback presence/order'),
        ('exception', 'inspect exception/unwind metadata'),
        ('load-config', 'check loader/security directory dependencies'),
        ('capture-timing', 'compare dump state with runtime code availability'),
        ('runtime-state', 'check missing generated code or external loader state'),
    ],
    'frida-attach-crashes': [
        ('tool-version', 'record host/server Frida versions'),
        ('ABI', 'compare process and server architecture'),
        ('ART-compatibility', 'record device API/build and runtime'),
        ('instrumentation-timing', 'compare no-script vs instrumented sessions'),
        ('native-crash', 'capture logcat crash and tombstone evidence'),
        ('anti-instrumentation', 'hypothesis only; seek discriminating evidence'),
    ],
    'dex-not-found-on-disk': [
        ('split-package', 'inventory base/split/feature modules'),
        ('dynamic-loading', 'observe classloader and runtime representation'),
        ('in-memory-loading', 'assess memory-backed DEX evidence'),
        ('no-dex-needed', 'consider native-only or resource-only module'),
    ],
    'protector-signature-disagrees': [
        ('stale-signature', 'check scanner rule version'),
        ('modified-signature', 'inspect header/section manipulation'),
        ('multiple-layers', 'consider nested transformations'),
        ('custom-protector', 'do not assign brand without positive corroboration'),
    ],
}


def diagnose(symptom: str, known: list[str] | None = None) -> dict[str, Any]:
    patterns = FAILURES.get(symptom, [])
    return {
        'symptom': symptom,
        'known_observations': known or [],
        'diagnoses': [{'hypothesis': name, 'next_observation': action,
                      'status': 'untested', 'confidence': 'Unknown'} for name, action in patterns],
        'requires_changed_variable': True,
        'next_step': 'collect evidence discriminating between the listed hypotheses',
        'result': 'Unknown' if patterns else 'Needs verification',
    }


def compatibility_applicability(record: dict[str, Any], environment: dict[str, Any]) -> dict[str, Any]:
    """Compare runtime + native tool + provider identity and versions.

    `environment` accepts flat OS/ABI fields and optional `subject` / `target`
    objects. Unknown compatibility and mismatched tool versions must NEVER
    be promoted to a compatible result by coincidence of OS/architecture.
    """
    observed = record.get('environment') or {}
    if not isinstance(observed, dict): observed = {}
    if not isinstance(environment, dict): environment = {}
    mismatches: list[str] = []
    missing: list[str] = []

    def known(x: Any) -> bool:
        return x not in (None, '', 'Unknown', 'unknown', 'Any', '*')

    def compare(field: str, expected: Any, actual: Any) -> None:
        if not known(expected) or not known(actual):
            missing.append(field)
        elif str(expected).casefold() != str(actual).casefold():
            mismatches.append(field)

    for field in ('os','arch'):
        compare('environment.'+field, observed.get(field), environment.get(field))
    if any(known((observed.get(k) or environment.get(k))) for k in
           ('android_api','abi','runtime','device_or_emulator')):
        for field in ('android_api','abi','runtime','device_or_emulator'):
            if known(observed.get(field)) or known(environment.get(field)):
                compare('environment.'+field, observed.get(field), environment.get(field))

    subject = record.get('subject') or {}
    actual_subject = environment.get('subject') or {}
    if not isinstance(subject,dict): subject = {}
    if not isinstance(actual_subject,dict): actual_subject = {}
    for field in ('capability','provider_id','provider_version','tool','tool_version'):
        # All five dimensions are necessary for a version-bound MCP result.
        compare('subject.'+field, subject.get(field), actual_subject.get(field))

    expected_target = record.get('target') or {}
    actual_target = environment.get('target') or {}
    if isinstance(expected_target,dict) and isinstance(actual_target,dict):
        for field in ('platform','architecture','protector','protector_version'):
            if known(expected_target.get(field)):
                compare('target.'+field, expected_target.get(field), actual_target.get(field))

    if mismatches:
        return {'applicable': False, 'status': 'not-applicable',
                'mismatches': mismatches, 'unknown_fields': missing}
    if missing or not record.get('evidence_ids'):
        return {'applicable': False, 'status': 'needs-verification',
                'mismatches': [], 'unknown_fields': missing}
    if record.get('result') not in ('compatible','partially-compatible','incompatible'):
        return {'applicable': False, 'status': 'needs-verification',
                'mismatches': [], 'unknown_fields': []}
    return {'applicable': True, 'status': record['result'],
            'mismatches': [], 'unknown_fields': [],
            'observed_at': record.get('observed_at', 'Unknown'),
            'note': 'Applies only to these exact observed versions and conditions; not a universal guarantee.'}


def promote_case_to_research(case: dict[str, Any], evidence_nodes: list[dict[str, Any]]) -> dict[str, Any]:
    """Strict research eligibility gate. A prose success claim is NOT validation.

    Real validation requires explicit reproducer and experiment IDs; independent
    sources must be recorded in the evidence graph. Canonical promotion is NEVER
    automated, including when all research eligibility checks pass.
    """
    import re

    refs = set(case.get('evidence_ids') or [])
    sources: set[str] = set()
    for node in evidence_nodes:
        if node.get('node_id') in refs:
            sources.update(str(s) for s in ((node.get('provenance') or {}).get('source_ids') or [])
                           if s not in ('Unknown', '', None))
    validation = case.get('verification') or {}
    if not isinstance(validation, dict):
        validation = {}
    sha = str((case.get('target') or {}).get('sha256') or '')
    constraints = {
        'sample_hash_known': bool(re.fullmatch(r'[0-9a-fA-F]{64}', sha)),
        'protector_version_known': (case.get('protector') or {}).get('version') not in ('Unknown', None, ''),
        'at_least_two_independent_sources': len(sources) >= 2 and
                                          validation.get('independent_sources_reviewed') is True,
        'reproduced_experiment_ids_recorded': bool(validation.get('reproduced') is True and
                                                     validation.get('experiment_ids') and
                                                     all(isinstance(e, str) and e.strip() for e in validation['experiment_ids'])),
        'human_reviewed': validation.get('human_reviewed') is True,
    }
    eligible = all(constraints.values())
    return {
        'research_eligible': eligible,
        'canonical_eligible': False,
        'checks': constraints,
        'decision': 'research-review' if eligible else 'case-only',
        'note': 'Manual/editorial review is required; neither a forum writeup nor tool agreement proves reproduction.',
    }
