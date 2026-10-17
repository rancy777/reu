# Evidence Graph Contract

## Node types

- `target` — original sample identity/hash
- `artifact` — derived/captured/reconstructed file or memory representation
- `observation` — direct measurement
- `claim` — proposition about the target
- `hypothesis` — competing explanation
- `experiment` — action designed to discriminate hypotheses
- `source` — external publication/document/repository
- `case` — sample-scoped research case
- `tool` — native tool
- `provider` — MCP provider
- `version` — tool/protector/runtime version
- `runtime` — OS/ART/CLR/etc.
- `workflow` — selected procedure
- `failure` — observed failure
- `technique` — technique/concept
- `protector` — protector/packer family

## Edge semantics

`supports` means evidence raises support for a claim.

`contradicts` means evidence conflicts with a claim.

`derived-from` means a node was produced from another representation.

`observed-in` ties an observation to a target/artifact/session.

`tested-by` ties a hypothesis/claim to an experiment.

`requires` expresses a workflow/tool prerequisite.

`same-family-as` expresses family similarity, not identity.

`supersedes` records temporal replacement.

`applicable-to` constrains scope.

`produced-by` records tool/provider provenance.

`validated-by` records successful verification.

`fails-under` records a bounded compatibility failure.

`caused-by` is allowed only when causal evidence is sufficient; otherwise use `associated-with`.

`resolves` links a contradiction to the experiment/observation that resolves it.

## Confidence

Confidence is an explanation aid, not a calibrated probability.

Use:
- High
- Medium
- Low
- Unknown
- Needs verification

Do not calculate numeric posterior probabilities unless a separate calibrated evaluation protocol exists.
