# MCP Provider Setup & Verification (2026-10-16)

**规则**：这个项目没有、也不会未经用户批准地安装第三方执行工具。GitHub 仓库链接只是供应链候选，不是安全担保。安装后必须获取本地 MCP 的 live `tools/list`，记录版本、提交哈希、权限并做小规模授权 fixture 验证。

| Tool | Upstream MCP | Status for Skill | How to connect | Notes |
|---|---|---|---|---|
| IDA | https://github.com/HexRaysSA/ida-mcp | Official; profile/command documented | stdio | 官方说明 IDA 9.4+、idalib、Python 3.11+；需另装插件/基础软件，版本信息以当前官方 README 为准 |
| radare2 | https://github.com/radareorg/radare2-mcp | First-party; verified config syntax | stdio | Upstream documents `r2pm -r r2mcp` |
| Ghidra | https://github.com/LaurieWired/GhidraMCP | Community candidate | GUI plugin + MCP | Adapter 名称基于上游 README；未做 live 验证 |
| JADX | https://github.com/zinja-coder/jadx-ai-mcp | Community candidate | GUI plugin + Python MCP server | `jadx plugins --install ...`；完整具体调用参数以 runtime `tools/list` 为准 |
| Apktool | https://github.com/zinja-coder/apktool-mcp-server | Community candidate/security-sensitive | Python server + apktool CLI | 安装前查阅 release security fixes；`decode_apk` 会向文件系统写出文件，需要 mutation approval |
| Frida | https://github.com/majimboo/rexd-frida-mcp | Experimental | Node stdio + Frida host/device | 示例 `listModules`, `readMemory`, `writeMemory` 等，仅供 adapter 识别；attach/hook 均需授权 |
| Unidbg | https://github.com/zhkl0228/unidbg | First-party built-in experimental | legacy localhost SSE | 在 paused emulator/debugger 会话中启动；必须安装官方 MCP SDK 可选依赖；没有 live handshake 验证 |
| WinDbg | https://github.com/glslang/windbg-mcp | Community candidate | DbgEng/WinDbg | 不支持将此当作 Microsoft 官方工具；版本/体系结构需现场验证 |
| x64dbg | https://github.com/ouonet/x64dbg-mcp | Community candidate | Windows host plugin/bridge | 运行样本必须在隔离 Windows VM；原始样本保持只读 |
| REMnux | https://github.com/REMnux/remnux-mcp-server | First-party project; isolated research alternative | local stdio / Docker / SSH | 该 Provider 能运行工具/转移文件，`analyze_file` 属执行类操作；需明确路径与隔离权限 |

## 建议的主机布局

`Agent host → 本机 MCP gateway → Windows VM / Linux VM / Android emulator`。
所有服务默认只监听 localhost；若跨主机连接，使用认证、TLS/隧道及网络隔离。不要直接公开 debugger/Frida/Shell MCP 端口。

## 执行规范

- 复制 `runtime/config/providers.ready-to-install.json`，把对应条目改成经过本人审核的**本地路径/版本**，再启用。
- 本包的 `doctor` 不启动 MCP Server；`discover` **会启动配置好的本地进程**，不要拿未知来源的配置直接执行。
- `adapter-plan` 对比**真实发现的工具名**与上游文档记载的 exact names，输出真实 MCP input schema，不能根据网上示例编造参数。
- `call` 需要和 `--authorized-target`、`--allow-execute / --allow-mutate / --allow-destructive` 组合使用，只读工具除外。未知风险永远拒绝自动执行。
- `host-inventory` 模式可直接消费 Agent 宿主已连接的 MCP 清单，避免重复启动 GUI 插件。
- 没有被测试的 HTTP/SSE 路线必须在交付给他人前用真实装机验证。

## 上游文档重点

- [MCP Python SDK v2 Client](https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/client/transports.md)
- [MCP tool annotations are untrusted hints](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/)
- [JADX-AI-MCP tool API reference](https://github.com/zinja-coder/jadx-ai-mcp/blob/jadx-ai/docs/api-reference.md)
- [Apktool MCP tool names](https://github.com/zinja-coder/apktool-mcp-server/blob/master/README.md)
- [rexd Frida MCP tool surface](https://github.com/majimboo/rexd-frida-mcp)
- [Unidbg MCP runtime modes](https://github.com/zhkl0228/unidbg/blob/master/README.md)
