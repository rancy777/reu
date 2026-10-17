# Host Agent Integration

There are two supported deployment modes.

## Mode A — Host-native MCP

The Agent host already connects to MCP servers and exposes their tools directly to the model.

In this mode the Skill should:
1. inspect the host's live MCP inventory;
2. map each tool to the semantic capability taxonomy;
3. use the host tool directly;
4. record provider/server/native-tool versions when available;
5. avoid launching a second MCP connection.

The host may export its inventory using `runtime/config/host-inventory.example.json` as a neutral interchange shape.

## Mode B — Runtime bridge

The Agent has shell access but does not itself expose the MCP server to the model.

Use `re-skill discover` to launch/connect to configured providers through the official MCP Python SDK.

This mode supports:
- stdio subprocess MCP servers;
- Streamable HTTP MCP servers;
- live tool discovery;
- capability mapping;
- health checks;
- normalized observations.

## Why both modes exist

MCP is normally a host integration protocol. A Skill cannot assume that every Agent exposes a generic API for "list all MCP servers". The host-native mode avoids duplicating an existing connection. The bridge mode provides a real client for Agents that need one.

## Provider installation

The user/operator remains responsible for installing the native reverse-engineering tool and the third-party MCP provider. The Skill validates and uses what is installed; it does not silently fetch and execute arbitrary repositories.
