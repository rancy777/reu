# Source Registry

## Tier S — primary/official

### Binary / Windows
- Microsoft Learn — PE/COFF format
- Microsoft/Windows debugging documentation
- x64dbg official project/documentation
- Ghidra official repository/documentation
- Hex-Rays official IDA documentation
- Hex-Rays official IDA MCP repository
- Binary Ninja official documentation
- radareorg/radare2 and radare2-mcp
- Mandiant FLARE FLOSS
- Mandiant FLARE capa
- PE-sieve project
- APKiD project
- Unidbg project

### Android
- Android Developers — App Bundle / bundletool
- Android Open Source Project — ART/runtime
- Frida official documentation/releases
- OWASP MASTG

### MCP infrastructure
- Model Context Protocol specification
- Official MCP reference filesystem server/repository

## Tier A/B research/community

- Malware Unicorn
- FLARE Learning Hub
- Reverse Engineering Stack Exchange
- Tuts 4 You
- crackmes.one
- 看雪 / kanxue
- 52pojie / 吾爱破解
- FreeBuf
- 先知社区
- original researcher blogs
- conference presentations
- academic papers
- reproducible CTF writeups
- maintained community MCP providers

## Registry fields

Source ID
Title
URL
Author/organization
Publication date
Last checked
Language
Tier
Topic
Versions covered
Primary/secondary
Accessible?
Claims extracted
Independent corroboration
Contradictions
Notes

## MCP provider fields

Provider ID
Repository
Provider class
Native tool
Provider version
Native tool version
Transport
Capabilities
Health status
Security posture
Last checked
Compatibility evidence
Known limitations

## Current MCP research anchors

- Hex-Rays official IDA MCP: official provider; README currently states IDA 9.4+ with idalib and Python 3.11+, and documents stdio/HTTP operation.
- radareorg/radare2-mcp: first-party project MCP; current release observed during research: 1.8.8.
- x64dbg-mcp: multiple active community implementations; version/commit must be pinned per installation.
- WinDbg: public Microsoft material shows MCP support/features in current WinDbg builds, while third-party DbgEng MCP servers provide explicit documented tool surfaces.
- Frida: current releases are moving quickly; record both Frida and provider versions for every Android runtime case.
- Unidbg: project documentation includes MCP debugger integration.
- JADX/APKTool: multiple community MCP implementations exist; tool signatures are not assumed stable.
- Filesystem: official MCP reference server exists and provides constrained filesystem access.
