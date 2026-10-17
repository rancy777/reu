# Case Library

## Case clustering keys

Primary:
- protector family
- protector version
- architecture
- platform
- runtime

Secondary:
- configuration
- packer layers
- anti-analysis pattern
- loader pattern
- dynamic materialization pattern
- reconstruction failure class

## Similarity rule

"Similar" means similar evidence and scope, not simply the same product name.

A VMProtect x64 case from one version/configuration is not automatically a close match to another version/configuration.

## Case reuse

When a new target resembles an old case:
1. retrieve candidate cases;
2. compare version/architecture/runtime;
3. compare observed indicators;
4. identify transferable techniques;
5. identify non-transferable assumptions;
6. label the new route as analogy-derived;
7. validate against the new target.

## Public case sources

Prioritize:
- crackmes.one
- CTF writeups
- original researcher posts
- official sample repositories
- reproducible community cases

The current crackmes.one rules and FAQ are useful boundary and dataset-quality references. Their labels can be AI-generated and may be inaccurate; therefore labels are discovery signals, not ground truth.
