# Research Method

## Source workflow

`search → open original → inspect text/code → trace references → corroborate → evidence card → scope → promotion decision`

## Claim discipline

Every material claim must answer:
- What exactly is being claimed?
- On what target/platform?
- Which version?
- Which architecture?
- Under what runtime/environment?
- What is the direct observation?
- What is inference?
- What evidence contradicts it?
- What would falsify it?
- What source supports it?

## Public community evidence

Forum/blog/CTF material is useful for discovery and case comparison.

It is not automatically canonical.

Record:
`Forum Evidence → case-scoped → corroborate → research/canonical if justified`

## MCP research

When researching an MCP provider:
- verify repository ownership;
- inspect recent activity/release history;
- inspect installation requirements;
- inspect transport/security posture;
- inspect tool surface;
- inspect whether it mutates the underlying analysis database;
- test health on a harmless fixture;
- pin the release/commit for case reproducibility.

## Update cadence

Recheck:
- provider status before major skill releases;
- native tool versions when compatibility matters;
- Android runtime changes when a case depends on ART/API behavior;
- protector information when a version-specific claim is reused.

## Unknown is a valid result

If a source is unavailable or conflicting:
`Unknown` / `Needs verification`

Do not reconstruct missing facts from memory.
