# Evidence Graph Store

`nodes.jsonl` and `edges.jsonl` are append-only logical stores.

Use stable IDs and preserve old records.

For a database implementation, an operator may import the JSONL into SQLite, DuckDB, PostgreSQL or a graph database. The skill does not require a particular database engine.

Recommended indexes:
- node_id
- node_type
- target_sha256
- case_id
- protector_family
- protector_version
- provider_id
- native_tool
- runtime
- source_id
- timestamp

Recommended graph queries:
- all evidence supporting a protector claim;
- all contradictions for a claim;
- all cases for a protector/version/arch tuple;
- all failures associated with a provider version;
- all compatibility failures for a runtime/API;
- all workflows validated by a case cluster.
