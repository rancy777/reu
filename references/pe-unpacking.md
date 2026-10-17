# PE Unpacking

## Decision stages
L0 acquisition/hash
L1 PE structure
L2 packer/protector hypotheses
L3 baseline runtime
L4 locate transformed/generated code
L5 identify meaningful execution boundary
L6 capture
L7 imports
L8 metadata/sections/relocations/TLS/load-config/exception structures
L9 static re-analysis
L10 runtime validation
L11 custom loader analysis
L12 virtualization research

## Success criteria
Do not define success as "OEP found". Success means the recovered representation is sufficient for the stated research goal and, when executable reconstruction is claimed, survives validation.

## Capture principle
Capture when the evidence indicates the desired code/data exists in a stable runtime representation. Record:
address space, module, thread, trigger, memory permissions, transformations, and exact capture state.

## Import reconstruction
Treat IAT recovery as evidence reconstruction. Verify:
- target pointers belong to expected modules
- forwarded APIs
- delay imports if relevant
- API-set behavior
- ordinal/name ambiguity
- architecture
- loader state

Use Scylla or equivalent as a candidate generator, then verify.

## Modern/complex cases
Escalate when:
- code is generated/decrypted repeatedly
- execution boundary moves
- code is virtualized
- imports are resolved dynamically
- self-integrity detects modifications
- dump executes only in the original process state
- TLS/exception/load-config structures matter

In these cases, "dump harder" is not a strategy; identify the representation needed by the analysis goal.
