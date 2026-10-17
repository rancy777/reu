# Evidence Policy

## Claim taxonomy
Every important sentence should be tagged internally as:
- FACT: directly supported by authoritative documentation or observed artifact
- OBSERVATION: directly observed in the supplied sample/runtime
- INFERENCE: reasoned from observations
- HYPOTHESIS: testable explanation
- UNKNOWN: evidence insufficient
- SUPERSEDED: formerly accepted but replaced

## Evidence card
Required fields:
Technique:
Platform:
Artifact Type:
Protection:
Version:
Architecture:
OS / Android API:
Runtime:
Prerequisites:
Goal:
Observation:
Method:
Expected Observation:
Failure Signs:
Alternative:
Tooling:
Source:
Source Date:
Source Quality:
Confidence:
Applicable Scope:
Known Limitations:
Counter-Evidence:
Reproduction Notes:
Last Verified:

## Ranking
S: official docs/source, original paper, original author
A: recognized security teams/researchers and reproducible research
B: detailed community cases with artifacts
C: ordinary secondary material
D: unverifiable material

## Cross-validation
For claims about a protector or tool:
1. primary documentation/source where available
2. independent technical case
3. sample evidence
4. experiment
5. counterexample search

If only one case exists, keep it case-scoped.

## Confidence rule
Confidence is not source rank. A high-quality source can describe a behavior that does not apply to the current version/sample. Store:
- Evidence confidence
- Applicability confidence
- Temporal confidence

## Citation rule
Cite the smallest claim supported by a source. Do not use a source to imply facts it does not establish.
