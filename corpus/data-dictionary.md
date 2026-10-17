# Corpus Data Dictionary

## Identity

`target_sha256` — SHA-256 of the exact artifact. Required whenever a concrete artifact is available.

`case_id` — stable identifier for one analysis case.

`evidence_id` — stable identifier for one evidence item.

`source_id` — stable identifier for one external source.

## Scope

Scope should include as many as known:
- platform
- file type
- architecture
- OS
- runtime
- API level
- ABI
- protector family
- protector version
- configuration
- sample type

## Observation vs claim

Observation:
"What the tool/test directly returned."

Claim:
"An interpretation derived from one or more observations."

Do not store an interpretation only as an observation.

## Confidence

Confidence labels:
- High
- Medium
- Low
- Unknown
- Needs verification

They are not calibrated probabilities.

## Completeness

Always distinguish:
- complete
- partial
- truncated
- paginated
- sampled
- unknown
