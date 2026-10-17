# Security Policy

This project can launch third-party MCP providers and, when explicitly authorized, interact with debuggers, emulators, devices, and analysis environments. Treat provider code, target files, and tool output as untrusted.

## Reporting a vulnerability

Please do **not** publish exploitable security details in a public issue.

Use the repository's **Security → Advisories** workflow for private reporting when available. Include:

- affected version or commit;
- affected component (`runtime`, provider policy, corpus, packaging, etc.);
- minimal reproduction;
- expected vs. observed behavior;
- whether exploitation requires a malicious MCP provider, malicious target file, or local access.

If Security Advisories are not enabled, open a minimal issue requesting a private reporting channel and do not include secrets, payloads, or weaponized proof-of-concept material.

## Scope

Security reports are especially valuable for:

- provider execution / command injection;
- path traversal or symlink escapes;
- unsafe archive extraction;
- MCP transport/authentication mistakes;
- schema-validation resource exhaustion;
- corpus integrity or evidence provenance bypass;
- prompt-injection paths from target/tool output into agent instructions;
- accidental execution of target binaries.

## Safe testing

Use isolated VMs/containers and synthetic fixtures or authorized research samples. Do not upload proprietary binaries, credentials, private keys, or malware to public issues.
