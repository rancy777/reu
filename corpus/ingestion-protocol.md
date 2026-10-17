# Corpus Ingestion Protocol

## After every meaningful analysis

1. Compute/confirm target hash.
2. Create or reuse `case_id`.
3. Record target/platform/architecture/runtime.
4. Record every MCP provider and native tool version used.
5. Capture normalized observations.
6. Create Evidence Cards for material claims.
7. Add graph nodes/edges.
8. Record failures and successful pivots.
9. Add compatibility observations if a version interaction was tested.
10. Create/update a regression fixture if the behavior is valuable for future routing.
11. Decide whether the finding remains case-only or is eligible for research/canonical promotion.

## Deduplication

Cases are duplicates only when:
- target hash matches; or
- an external public case explicitly proves the same artifact identity.

Similar-looking binaries are not duplicates.

## Redaction

Before committing corpus records:
- remove secrets/tokens/passwords;
- remove personal data;
- remove private paths when not necessary;
- replace private sample names with stable IDs;
- never embed commercial license material.

## Promotion

Case → Research:
- reproducible observations;
- clear scope;
- evidence provenance.

Research → Canonical:
- independent corroboration or authoritative source;
- no unresolved contradiction;
- version/architecture/runtime scope;
- regression test when practical.

If these are absent, keep the finding case-only.
