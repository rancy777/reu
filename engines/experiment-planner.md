# Experiment Planner

Choose the next experiment by expected information gain, not by habit.

## Procedure

1. List active hypotheses.
2. List evidence supporting and contradicting each.
3. Identify the uncertainty that blocks the next decision.
4. Generate candidate experiments.
5. Estimate which hypotheses each experiment could distinguish.
6. Prefer:
   - low risk;
   - reversible;
   - deterministic;
   - read-only;
   - high discrimination;
   - low setup cost.
7. Record expected observations before execution.
8. Execute only when authorized.
9. Compare actual vs expected.
10. Update hypotheses and the evidence graph.

## Failure loop

Never:
`failed experiment → same experiment again`

Prefer:
`failed experiment → classify failure → change variable/representation/tool/provider/timing → new experiment`

## Example

Symptom:
"dumped PE does not run"

Candidates:
- IAT incomplete
- wrong section mapping
- TLS/runtime initialization
- wrong capture state
- self-integrity
- generated code still active

High-information next test:
check whether imports resolve and whether the entry path reaches the expected reconstructed image before changing bytes.

The exact experiment must be adapted to the authorized environment and available MCP capabilities.
