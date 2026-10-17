# MCP Configuration Examples

These examples are installation/reference material, not hard-coded requirements. Exact commands should be rechecked against the provider's current README before installation.

## IDA — official Hex-Rays

Requirements currently documented by Hex-Rays:
- IDA 9.4+
- idalib
- Python 3.11+
- `uv`

Recommended setup:

```text
uvx ida-hcli mcp install
```

Generic stdio configuration:

```json
{
  "mcpServers": {
    "ida": {
      "command": "uvx",
      "args": [
        "--exclude-newer=1s",
        "ida-mcp",
        "stdio",
        "--agent=my-agent"
      ]
    }
  }
}
```

Source:
https://github.com/HexRaysSA/ida-mcp

## x64dbg

The `ouonet/x64dbg-mcp` project documents:

```json
{
  "mcpServers": {
    "x64dbg-mcp": {
      "command": "x64dbg-mcp"
    }
  }
}
```

It is Windows-only and requires the x64dbg bridge/plugin.

Source:
https://github.com/ouonet/x64dbg-mcp

## radare2

The radareorg project documents:

```json
{
  "mcpServers": {
    "radare2": {
      "command": "r2pm",
      "args": ["-r", "r2mcp"]
    }
  }
}
```

Prefer readonly/restricted mode for initial triage.

Source:
https://github.com/radareorg/radare2-mcp

## WinDbg

A standalone DbgEng MCP can be configured as a local executable:

```json
{
  "mcpServers": {
    "windbg": {
      "command": "C:\\path\\to\\windbg-mcp.exe"
    }
  }
}
```

Use the provider's current install documentation to obtain the binary and exact runtime requirements.

Source:
https://github.com/glslang/windbg-mcp

## Frida / rexd

The project documents a local stdio server launched from the repository:

```text
node <ABSOLUTE_PATH_TO_REPO>\src\mcp-server.mjs
```

Source:
https://github.com/majimboo/rexd-frida-mcp

## Unidbg

When the Unidbg debugger is active, its documented MCP endpoint can be exposed locally. The exact port is session-dependent.

Source:
https://github.com/zhkl0228/unidbg

## JADX

The JADX MCP project documents installation through `uv` and a stdio server. Prefer the current project README over copying old command lines.

Source:
https://github.com/zinja-coder/jadx-mcp-server

## Apktool

The Apktool MCP project documents a Python/uv-based local stdio server.

Source:
https://github.com/zinja-coder/apktool-mcp-server

## Filesystem

The official MCP filesystem server can be run with a constrained set of allowed directories:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/analysis/workspace"
      ]
    }
  }
}
```

On Windows, use the client/provider's documented `cmd /c` wrapper when required.

Source:
https://github.com/modelcontextprotocol/servers

## Ghidra / Binary Ninja

Multiple community providers exist. Because tool surfaces and supported native-tool versions vary, the skill does not hard-code one global configuration.

After installation:
1. discover MCP tools;
2. map to semantic capabilities;
3. run health checks;
4. pin the provider release/commit;
5. record the binding in the case.

## Installation rule

Do not blindly execute installation snippets copied from search results.

Verify:
- repository owner;
- release/commit;
- license;
- install script;
- network endpoints;
- filesystem permissions;
- required privileges;
- native-tool version;
- MCP client compatibility.
