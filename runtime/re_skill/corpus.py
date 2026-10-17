"""Schema-validated, append-only JSONL case/compatibility/evidence store.

Writes metadata and derived observations, never executable samples. Graph edges
require resolvable nodes; single-case evidence is never silently canonicalized.
"""
from __future__ import annotations

import json
import os
import time
from contextlib import contextmanager
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

SCHEMA_FILES = {
    'observations/index.jsonl': 'mcp-observation.schema.json',
    'protector-cases/index.jsonl': 'protector-case.schema.json',
    'runtime-compatibility/index.jsonl': 'runtime-compatibility.schema.json',
    'evidence-graph/nodes.jsonl': 'evidence-node.schema.json',
    'evidence-graph/edges.jsonl': 'evidence-edge.schema.json',
    'regression/automated.jsonl': 'regression-case.schema.json',
    'regression/research.jsonl': 'regression-case.schema.json',
}


@contextmanager
def _file_lock(path: Path, *, timeout: float = 15.0):
    """Process-safe sidecar advisory lock (POSIX flock / Windows msvcrt).

    Every writer must use this function. This guards duplicate IDs + appends;
    it is not a distributed transaction protocol (single workstation only).
    """
    lock_path = path.with_name(path.name + '.lock')
    if lock_path.is_symlink():
        raise ValueError('corpus lock path cannot be a symlink')
    fd = os.open(lock_path, os.O_CREAT | os.O_RDWR | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    try:
        if os.name == 'nt':
            import msvcrt
            if os.fstat(fd).st_size == 0:
                os.write(fd, b'\0')
            lock = lambda: msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
            unlock = lambda: msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
            retry_errors = (OSError,)
        else:
            import fcntl
            lock = lambda: fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            unlock = lambda: fcntl.flock(fd, fcntl.LOCK_UN)
            retry_errors = (BlockingIOError,)
        deadline = time.monotonic() + timeout
        while True:
            try:
                os.lseek(fd, 0, os.SEEK_SET)
                lock()
                break
            except retry_errors:
                if time.monotonic() >= deadline:
                    raise TimeoutError('timed out waiting for corpus append lock')
                time.sleep(0.03)
        try:
            yield
        finally:
            os.lseek(fd, 0, os.SEEK_SET)
            unlock()
    finally:
        os.close(fd)


def _parse_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    result: list[dict[str, Any]] = []
    with path.open(encoding='utf-8') as stream:
        for n, line in enumerate(stream, 1):
            if not line.strip():
                continue
            if len(line) > 16 * 1024 * 1024:
                raise ValueError(f'oversized corpus JSONL record at {path.name}:{n}')
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f'invalid corpus JSONL at {path.name}:{n}') from exc
            if not isinstance(record, dict):
                raise ValueError(f'non-object corpus JSONL at {path.name}:{n}')
            result.append(record)
    return result


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_record(record: dict[str, Any], schema_path: str | Path) -> list[str]:
    schema = json.loads(Path(schema_path).read_text(encoding='utf-8'))
    errors = sorted(Draft202012Validator(schema).iter_errors(record), key=lambda e: str(list(e.path)))
    return [f'{list(e.path)}: {e.message}' for e in errors]


class CorpusStore:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.schema_root = Path(__file__).with_name('schemas')
        if not self.schema_root.exists():
            self.schema_root = Path(__file__).resolve().parents[2] / 'corpus' / 'schemas'
        for folder in ('observations', 'evidence-graph', 'protector-cases', 'runtime-compatibility', 'regression'):
            (self.root / folder).mkdir(parents=True, exist_ok=True)

    def _checked_path(self, relative: str) -> Path:
        """Prevent traversal and symlink redirection outside a local corpus."""
        rel = Path(relative)
        if not str(relative).strip() or rel.is_absolute() or '..' in rel.parts:
            raise ValueError('corpus file must be a relative path without traversal')
        current = self.root.resolve()
        for part in rel.parts:
            current = current / part
            if current.is_symlink():
                raise ValueError('corpus paths must not contain symlinks')
        if not current.resolve().is_relative_to(self.root.resolve()):
            raise ValueError('corpus path escapes workspace')
        return current

    def read(self, relative: str) -> list[dict[str, Any]]:
        path = self._checked_path(relative)
        if not path.is_file():
            return []
        # Readers may see the previous complete generation; no partial JSONL lines.
        with _file_lock(path):
            return _parse_jsonl(path)

    def append(self, relative: str, record: dict[str, Any], *, id_field: str | None = None) -> Path:
        path = self._checked_path(relative)
        if relative in SCHEMA_FILES:
            errors = validate_record(record, self.schema_root / SCHEMA_FILES[relative])
            if errors:
                raise ValueError(f'{relative}: schema violation: {errors}')
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = (json.dumps(record, ensure_ascii=False, sort_keys=True) + '\n').encode('utf-8')
        if len(payload) > 16 * 1024 * 1024:
            raise ValueError('corpus record exceeds 16 MiB JSONL cap')
        with _file_lock(path):
            if id_field:
                current = {row.get(id_field) for row in _parse_jsonl(path)}
                if record.get(id_field) in current:
                    raise ValueError(f'duplicate {id_field}={record[id_field]}')
            fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, 'O_NOFOLLOW', 0), 0o600)
            try:
                offset = 0
                while offset < len(payload):
                    n = os.write(fd, payload[offset:])
                    if n <= 0:
                        raise OSError('corpus append failed: short write')
                    offset += n
                os.fsync(fd)
            finally:
                os.close(fd)
        return path

    def repair_graph(self, *, dry_run: bool = True) -> dict[str, Any]:
        """Reconcile graph nodes after an interrupted multi-file append.

        Graph storage is *eventually consistent*, not one atomic multi-file
        transaction. This explicitly reports and repairs missing nodes only;
        it never silently invents case evidence or research conclusions.
        """
        nodes = {n['node_id'] for n in self.read('evidence-graph/nodes.jsonl')}
        pending = []
        for relative, kind, id_key in (
            ('observations/index.jsonl', 'observation', 'observation_id'),
            ('protector-cases/index.jsonl', 'case', 'case_id'),
            ('runtime-compatibility/index.jsonl', 'runtime', 'compat_id'),
        ):
            for record in self.read(relative):
                nid = record.get(id_key)
                if isinstance(nid, str) and nid not in nodes:
                    pending.append({'node_id': nid, 'node_type': kind,
                                    'label': record.get('operation') or nid})
                    nodes.add(nid)
        actual_nodes = {n['node_id'] for n in self.read('evidence-graph/nodes.jsonl')}
        dangling = [e['edge_id'] for e in self.read('evidence-graph/edges.jsonl')
                    if e['from'] not in actual_nodes or e['to'] not in actual_nodes]
        repaired = []
        if not dry_run:
            for node in pending:
                self.add_node(node)
                repaired.append(node['node_id'])
        return {'dry_run': dry_run, 'missing_nodes': [n['node_id'] for n in pending],
                'repaired_nodes': repaired, 'dangling_edges': dangling,
                'limitation': 'Edges cannot be reconstructed without source provenance; review dangling edges manually.'}

    def add_node(self, node: dict[str, Any]) -> str:
        obj = dict(node)
        nid = obj.pop('id', None) or obj.get('node_id') or f'NODE-{uuid.uuid4().hex[:16]}'
        obj['node_id'] = nid
        obj['node_type'] = obj.get('node_type') or obj.pop('type', 'observation')
        obj.setdefault('label', nid)
        obj.setdefault('provenance', {'created_at': utc_now(), 'source_ids': [], 'evidence_ids': []})
        self.append('evidence-graph/nodes.jsonl', obj, id_field='node_id')
        return nid

    def add_edge(self, source: str, target: str, relation: str, reason: str,
                 evidence_ids: list[str] | None = None) -> str:
        existing = {r['node_id'] for r in self.read('evidence-graph/nodes.jsonl')}
        if source not in existing or target not in existing:
            raise ValueError('graph edges may only connect existing nodes')
        eid = f'EDGE-{uuid.uuid4().hex[:16]}'
        edge = {'edge_id': eid, 'from': source, 'to': target,
                'relation': relation, 'reason': reason,
                'provenance': {'created_at': utc_now(), 'source_ids': [],
                               'evidence_ids': evidence_ids or []}}
        self.append('evidence-graph/edges.jsonl', edge, id_field='edge_id')
        return eid

    def add_observation(self, observation: dict[str, Any]) -> str:
        obs = dict(observation)
        obs_id = obs.setdefault('observation_id', f'OBS-{uuid.uuid4().hex[:16]}')
        obs.setdefault('timestamp', utc_now())
        obs.setdefault('status', 'unknown')
        obs.setdefault('operation', 'unknown')
        obs.setdefault('provider_id', 'unknown')
        if obs.get('side_effect_class') and not obs.get('side_effects'):
            effect = obs['side_effect_class']
            obs['side_effects'] = effect if effect in ('read','observe','execute','mutate','destructive') else 'execute'
        obs.setdefault('side_effects', 'observe')
        obs.setdefault('completeness', 'unknown')
        obs.setdefault('evidence_ids', [])
        obs.setdefault('derived_claims', [])
        obs.setdefault('host', {})
        self.append('observations/index.jsonl', obs, id_field='observation_id')
        self.add_node({'node_id': obs_id, 'node_type': 'observation',
                       'label': obs['operation'], 'status': obs['status']})
        target_hash = obs.get('target_sha256') or obs.get('target', {}).get('sha256')
        if isinstance(target_hash, str) and len(target_hash) == 64 and all(c in '0123456789abcdefABCDEF' for c in target_hash):
            tid = f'TARGET-{target_hash}'
            if tid not in {n['node_id'] for n in self.read('evidence-graph/nodes.jsonl')}:
                self.add_node({'node_id': tid, 'node_type': 'target', 'label': target_hash[:16], 'value': target_hash})
            self.add_edge(obs_id, tid, 'observed-in', 'Observation derived from the hashed target', [obs_id])
        return obs_id

    def add_case(self, case: dict[str, Any]) -> str:
        case = dict(case)
        case_id = case.setdefault('case_id', f'CASE-{uuid.uuid4().hex[:16]}')
        case.setdefault('status', 'case-only')
        case.setdefault('created_at', utc_now())
        self.append('protector-cases/index.jsonl', case, id_field='case_id')
        self.add_node({'node_id': case_id, 'node_type': 'case', 'label': case_id,
                       'status': case['status'], 'scope': case.get('scope')})
        for evid in case.get('evidence_ids', []):
            existing = {n['node_id'] for n in self.read('evidence-graph/nodes.jsonl')}
            if evid in existing:
                self.add_edge(evid, case_id, 'observed-in', 'Case references evidence card', [evid])
        return case_id

    def add_compatibility(self, record: dict[str, Any]) -> str:
        obj = dict(record)
        compat_id = obj.setdefault('compat_id', f'COMP-{uuid.uuid4().hex[:16]}')
        self.append('runtime-compatibility/index.jsonl', obj, id_field='compat_id')
        self.add_node({'node_id': compat_id, 'node_type': 'runtime', 'label': compat_id})
        return compat_id

    def add_regression(self, record: dict[str, Any]) -> str:
        obj = dict(record)
        reg_id = obj.setdefault('regression_id', f'RG-{uuid.uuid4().hex[:16]}')
        if 'category' in obj:
            # New cases require review before inclusion in the automated gate.
            self.append('regression/research.jsonl', obj, id_field='regression_id')
        else:
            self.append('regression/runtime-results.jsonl', obj, id_field='regression_id')
        return reg_id

    def query_cases(self, *, platform: str | None = None, protector: str | None = None,
                    architecture: str | None = None) -> list[dict[str, Any]]:
        result = self.read('protector-cases/index.jsonl')
        if platform:
            result = [c for c in result if platform.lower() in str(c.get('platform', '')).lower()]
        if protector:
            result = [c for c in result if protector.lower() in str(c.get('protector', {}).get('family', '')).lower()]
        if architecture:
            result = [c for c in result if architecture.lower() == str(c.get('architecture', '')).lower()]
        return result

    def similar_cases(self, query: dict[str, Any], limit: int = 10) -> list[dict[str, Any]]:
        """Case retrieval only; a similarity score never proves protector identity."""
        out = []
        for case in self.read('protector-cases/index.jsonl'):
            score, reasons = 0, []
            for key, weight in [('platform', 25), ('file_type', 15), ('architecture', 10), ('runtime', 10)]:
                q, c = str(query.get(key, '')).lower(), str(case.get(key, '')).lower()
                if q and q not in ('unknown', 'none') and q == c:
                    score += weight; reasons.append(key)
            candidate = query.get('protector') or {}
            protector = case.get('protector') or {}
            if isinstance(candidate, str): candidate = {'family': candidate}
            if str(candidate.get('family') or '').lower() == str(protector.get('family') or '').lower() and candidate.get('family'):
                score += 25; reasons.append('protector.family')
                if candidate.get('version') not in (None, '', 'Unknown', 'unknown') and candidate['version'] == protector.get('version'):
                    score += 10; reasons.append('protector.version')
            q_ind = {str(x).lower() for x in query.get('initial_indicators', [])}
            c_ind = {str(x).lower() for x in case.get('initial_indicators', [])}
            shared = q_ind & c_ind
            score += min(15, 5 * len(shared))
            if shared: reasons.append('shared-indicators:' + ','.join(sorted(shared)))
            if score > 0:
                out.append({'case_id': case['case_id'], 'similarity_score': score, 'matched_on': reasons,
                            'status': case.get('status'), 'note': 'retrieval relevance only, not independent validation'})
        return sorted(out, key=lambda x: (-x['similarity_score'], x['case_id']))[:limit]

    def graph_neighborhood(self, node_id: str, depth: int = 2) -> dict[str, Any]:
        if not 0 <= depth <= 5:
            raise ValueError('depth must be 0-5')
        nodes = {n['node_id']: n for n in self.read('evidence-graph/nodes.jsonl')}
        if node_id not in nodes:
            raise KeyError(f'unknown graph node {node_id}')
        edges = self.read('evidence-graph/edges.jsonl')
        reached = {node_id}
        active = {node_id}
        included = []
        for _ in range(depth):
            nxt = set()
            for e in edges:
                if e['from'] in active or e['to'] in active:
                    included.append(e)
                    nxt |= {e['from'], e['to']}
            active = nxt - reached
            reached |= nxt
        return {'nodes': [nodes[i] for i in sorted(reached) if i in nodes],
                'edges': list({e['edge_id']: e for e in included}.values())}
