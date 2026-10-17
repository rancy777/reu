# Regression Cases

The maintained machine-readable datasets are:

- `corpus/regression/automated.jsonl`: 16 fully executable policy/routing records used by the strict offline gate.
- `corpus/regression/research.jsonl`: 8 research records retaining 5 PARTIAL and 3 MANUAL results.

All 24 original records are retained with unchanged IDs, assertions, inputs, and expected results. No record appears in both datasets. The split declares acceptance scope; it does not increase demonstrated protector coverage.

Run `re-skill regress --strict --file corpus/regression/automated.jsonl` for offline acceptance. Run research records separately; their strict mode intentionally returns exit code 2.

New definitions ingested with `CorpusStore.add_regression` go to the research dataset. Move a definition to the automated dataset only after reviewing fully executable assertions and confirming strict success; never delete manual assertions merely to make CI green.

The runner rejects empty datasets and duplicate IDs.
