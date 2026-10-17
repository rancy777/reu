# MCP Installation Policy

The Skill does not silently download and execute arbitrary third-party MCP repositories.

## Principle

The user installs the native tools and, if desired, the MCP providers. The Skill:
- discovers what is already installed;
- validates the provider;
- suggests the upstream installation path;
- records exact version/commit;
- performs health checks;
- binds capabilities;
- updates the compatibility/corpus records.

## Recommended installation order

1. Native analysis tool
2. Native tool self-test
3. MCP provider from an identified upstream repository
4. MCP provider self-test/doctor command
5. MCP discovery
6. Capability mapping
7. Regression fixture
8. Enable for real analysis

## Do not auto-install by default

Avoid an automatic "curl | shell", arbitrary Git checkout + execute, or mutable `latest` deployment.

For each upstream:
- prefer signed/released artifacts when the project provides them;
- verify checksum when published;
- pin a release/tag/commit for reproducible environments;
- record the source URL;
- keep third-party code outside the Skill package unless licensing and update ownership are explicitly handled.

## Native CLI fallback

A dedicated MCP is not required for every CLI.

For tools such as:
- DIE/diec
- PE-bear
- PEStudio
- FLOSS
- capa
- YARA
- Scylla
- PE-sieve
- pefile/LIEF scripts
- adb
- bundletool
- baksmali/smali

the preferred fallback is a constrained `artifact.exec` capability.

The output must be normalized into the same evidence schema as MCP output.

## Why not bundle every MCP

Bundling creates:
- stale versions;
- conflicting plugin versions;
- license obligations;
- supply-chain risk;
- duplicate tool surfaces;
- harder regression maintenance.

Use upstream-by-reference + lock metadata instead.
