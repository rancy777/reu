<div align="center">

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/assets/readme-hero-dark-mobile.svg">
  <source media="(max-width: 600px)" srcset="docs/assets/readme-hero-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/readme-hero-dark.svg">
  <img src="docs/assets/readme-hero.svg" alt="REU：逆向研究，结论有据。" width="100%">
</picture>

# Reverse Engineering & Unpacking

**给 AI Agent 一套从样本初筛到脱壳验证的逆向研究方法。**

Windows / .NET · Android / DEX · Native / ELF

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&labelColor=253044)](pyproject.toml)
[![Version 1.5.0](https://img.shields.io/badge/Version-1.5.0-5C6F91?style=flat-square&labelColor=253044)](CHANGELOG.md)
[![MIT License](https://img.shields.io/badge/License-MIT-4F8565?style=flat-square&labelColor=253044)](LICENSE)

[**看实测**](#实测案例) · [**快速上手**](#快速上手) · [CI 与下载](https://github.com/rancy777/reu/actions/workflows/ci.yml?query=branch%3Amain) · [文档](#文档导航)

[English](README.md) · **简体中文** · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md) · [Русский](README.ru.md)

</div>

REU 是 **Agent Skill + Python CLI**：识别文件、选择实验、连接现有分析工具，并把结果整理成可复核的证据。你提供样本与分析环境，REU 提供研究流程、路由与记录。

## 实测案例

**VMProtect 3.8.4 · Windows x64 · 2026-10-17**

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/assets/readme-cases-dark-mobile.svg">
  <source media="(max-width: 600px)" srcset="docs/assets/readme-cases-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/readme-cases-dark.svg">
  <img src="docs/assets/readme-cases.svg" alt="Two VMProtect 3.8.4 x64 experiments: packing reconstruction passed 45 behavior and 14 structural checks; one virtualized pure function recovered as 53 native instructions passed 100,008 input checks and 128 protected-program comparisons. Separate samples and configurations." width="100%">
</picture>

- **[加壳 → 脱壳重建](docs/cases/vmprotect-3.8.4-x64.md)**：运行时导出与导入修复，得到可独立运行的 EXE。[源码与验收](examples/vmprotect-3.8.4-x64)。
- **[函数虚拟化 → 原生语义重建](docs/cases/vmprotect-3.8.4-virtualized-x64.md)**：真实调试轨迹 → 恢复表达式 → 编译原生函数。[源码、恢复 IR 与验收](examples/vmprotect-3.8.4-virtualized-x64)。

两组自有样本、不同保护配置。前者使用已知 OEP 与人工导入修复；后者只验证一个纯函数，CLI 测试外壳另行编译，全域 SMT 证明未完成。报告保留了参数、失败记录和适用范围。

[![DIE 实际窗口中恢复的原生函数开头](docs/assets/vmp-3.8.4-virtualized-x64/07-recovered-native-function.jpg)](docs/assets/vmp-3.8.4-virtualized-x64/07-recovered-native-function.jpg)

<p align="center"><sub>真实 DIE 截图：恢复后 DLL 的原生函数开头。点击可查看原图；完整 53 条指令与产物哈希见<a href="docs/cases/vmprotect-3.8.4-virtualized-x64.md">案例报告</a>。</sub></p>

<details>
<summary>查看加壳案例内部对照：加壳前 → 加壳后 → 脱壳重建后</summary>

**加壳前：原始入口点**

![加壳前的入口点反汇编](docs/assets/vmp-3.8.4-x64/18-original-entrypoint.jpg)

**加壳后：保护器入口点**

![加壳后的静态入口点反汇编](docs/assets/vmp-3.8.4-x64/19-protected-entrypoint.jpg)

**脱壳重建后：原入口点与重建的导入调用**

![脱壳重建后的入口点反汇编](docs/assets/vmp-3.8.4-x64/20-unpacked-entrypoint.jpg)

[查看 PE 文件头、节区、导入表、哈希和重建限制](docs/cases/vmprotect-3.8.4-x64.md)。

</details>

<details>
<summary>查看函数虚拟化内部对照：原始计算 → VM 入口 → 恢复的原生指令</summary>

**虚拟化前：SDK 标记的原始计算函数**

![SDK 标记的原始函数反汇编](docs/assets/vmp-3.8.4-virtualized-x64/06-original-function.jpg)

**虚拟化后：函数进入 VMP 虚拟机**

![虚拟化后的函数入口反汇编](docs/assets/vmp-3.8.4-virtualized-x64/05-virtualized-function.jpg)

**语义重建后：由恢复表达式编译出的原生指令**

![恢复的原生函数反汇编](docs/assets/vmp-3.8.4-virtualized-x64/07-recovered-native-function.jpg)

以上均为实际静态反汇编截图。恢复函数保持了已验证的行为，不是原函数或整个 EXE 的逐字节还原。[查看轨迹、验收与限制](docs/cases/vmprotect-3.8.4-virtualized-x64.md)。

</details>

## 快速上手

准备 **Python 3.11+**，使用有此私有仓库访问权限的 GitHub 账号克隆并运行：

```bash
git clone https://github.com/rancy777/reu.git
cd reu
python -m pip install -e .
re-skill route --input runtime/examples/triage.sample.json
```

无需 MCP、无需执行目标。内置合成元数据声明了动态 DEX 加载，运行时因此选择对应工作流；`Unknown` 保留为未知。

<details>
<summary>查看实际输出与路由示例图</summary>

JSON 输出中的部分字段：

```json
{
  "platform": "android",
  "architecture": "arm64",
  "workflows": [
    "android-triage",
    "android-dex",
    "android-dynamic-loading"
  ],
  "protection_status": "Unknown"
}
```

<picture>
  <source media="(max-width: 600px)" srcset="docs/assets/readme-demo-mobile.svg">
  <img src="docs/assets/readme-demo.svg" alt="将声明了动态 DEX 加载的 arm64 APK 示例元数据，路由到 android-triage、android-dex 和 android-dynamic-loading；保护状态保留为 Unknown。图中是实际 CLI 输出的部分字段。" width="100%">
</picture>

</details>

接着分析一个你有权检查的文件：

```bash
re-skill triage --file ./sample.exe --route
```

初筛会记录 SHA-256、检查支持的文件结构并推荐工作流，**不会执行目标文件**。APK、AAB、DEX 和 ELF / SO 文件会进入各自的分析路径。

### 交给 Agent

安装完整本地 Skill；已有安装会被保留，并提示停止：

```bash
python scripts/install_skill.py
```

然后在支持 Skill 的 Agent 中使用：

```text
$reverse-engineering-unpacking
分析 ./sample.exe，我有权检查这个文件。
先做只读初筛：SHA-256、架构、保护迹象。
给出下一步实验，说明要验证什么，并保留证据。
区分观测事实、假设和未知项。
```

默认复制到 `~/.agents/skills/reverse-engineering-unpacking`。CLI 需单独安装；在其他目录使用时，向 Agent 提供 CLI 可执行文件的绝对路径。[宿主发现与隔离安装](docs/getting-started.md)。

### 复建原生演示程序

准备 **Windows x64、Python 3.11 x64、Visual Studio C++ x64 构建工具和 Windows SDK**，在项目根目录运行：

```powershell
powershell -NoProfile -File .\examples\vmprotect-3.8.4-virtualized-x64\source\rebuild_demo.ps1
```

脚本在新环境中下载固定版本的 llvmlite，编译公开的恢复 IR、链接 DLL 和 CLI 测试外壳，再对单独复制并改名的 EXE 执行 **45 项功能检查**。不需要 VMProtect 或专有 SDK。产物位于 `runtime-artifacts/vmp-native-demo`；已有目录会被拒绝覆盖。[详细说明与完整实验前提](examples/vmprotect-3.8.4-virtualized-x64/README.md)。

这条命令复建已有恢复结果，不会为新目标脱壳，也不会重新执行与受保护程序的差分检查。

## 为什么用 REU

- **知道下一步查什么。** 按平台进入工作流，写清每次实验的假设、预期观测与失败诊断。
- **使用你已有的工具。** 发现 MCP 实际暴露的能力，按真实输入 Schema 规划调用。
- **让“成功”有依据。** 保存哈希、轨迹、功能与结构检查；失败实验也能成为下次研究的证据。

```text
样本 → 初筛 → 假设 → 实验 → 验证 → 可复用案例
                      ↑       │
                      └─ 修正 ─┘
```

## 研究范围

| 目标 | 内置初筛与路由 | 继续阅读 |
| :--- | :--- | :--- |
| **Windows PE / .NET** | 文件头、架构、CLR 特征、节属性与熵信号 | [Windows](workflows/windows-triage.md) · [.NET](workflows/windows-dotnet.md) |
| **Android APK / AAB** | 包结构、DEX / 原生库清单、拆分包路由 | [Android](workflows/android-triage.md) · [拆分包与 AAB](workflows/android-split-aab.md) |
| **DEX / ART 产物** | DEX、CDEX、VDEX 识别与运行时产物路由 | [DEX](workflows/android-dex.md) · [ART](workflows/android-art-runtime.md) |
| **Native ELF / SO** | ELF 标识与架构；提供 Android 上下文后选择对应路由 | [ELF](workflows/native-elf-triage.md) · [Android 原生层](workflows/android-native.md) |

研究指南覆盖脱壳、动态加载和复杂保护分析。成功重建目标仍需外部工具、针对具体样本的实验和验证。

## 连接分析工具

宿主已提供 MCP 工具时，使用[宿主原生模式](runtime/host-integration.md)。需要独立客户端桥接时：

```bash
python -m pip install -e '.[mcp]'
```

从[默认禁用的配置模板](runtime/config/providers.ready-to-install.json)创建 `providers.json`，按 [Provider Setup](integrations/PROVIDER-SETUP.md) 配置实际安装的服务。

<details>
<summary>配置检查、发现命令与工具候选</summary>

```bash
re-skill doctor --config ./providers.json
re-skill discover --config ./providers.json --registry ./integrations/mcp-provider-registry.yaml --output discovery.json
```

`doctor` 离线检查；`discover` 启动已启用且获注册表批准的 Provider。桥接支持 stdio 和 Streamable HTTP，执行与修改操作有独立授权门控。

[工具目录](integrations/mcp-upstream-catalog.yaml)收录 IDA、Ghidra、x64dbg、WinDbg、JADX、Frida 等候选；收录不代表实际兼容性已验证。工具和服务需另行安装。[适配规划](integrations/provider-adapter-profiles.json) · [安全审查](integrations/SECURITY-REVIEW.md)。

</details>

## 当前状态

**v1.5.0 · 工程候选阶段。** 两组 Windows 原生工具实验已有记录，更广泛的样本覆盖仍待补充。第三方 MCP Provider 按上游说明安装使用，重复验证不作为发布前置条件。[Windows/Ubuntu CI](https://github.com/rancy777/reu/actions/workflows/ci.yml?query=branch%3Amain)检查 Python 3.11–3.14、安装、源码完整性和原生演示。成功运行的 **Artifacts** 中提供验收后的源码包、wheel 与演示证据。[验证记录](docs/verification.md) · [待办与边界](docs/project-status.md)。

<details>
<summary>运行本地检查，了解语料统计</summary>

```bash
python -m pip install -e '.[test]'
python -m pytest -q runtime/tests
re-skill regress --strict --file corpus/regression/automated.jsonl
```

自动回归门禁有 16 条可执行记录；独立研究数据集保留 5 PARTIAL / 3 MANUAL，严格模式预期退出 2。24 条原始记录及断言均保留。

[种子语料](corpus/STATUS.md)的 1 条公开元数据、14 张机制分类卡片、0 条实测兼容性观测，是资料清单，不等于实测案例数量。[源码归档与发布检查](docs/releasing.md)。

</details>

## 常见问题

**能一条命令脱掉任意 VMP 吗？** 不能。CLI 提供初筛、路由和证据操作；重建需要外部工具与具体研究，两组实测案例不等于通用脱壳器。

**原生演示程序复现了什么？** 从已经恢复的 LLVM IR 编译出原生实现，并执行 45 项 CLI 功能检查。原实验的轨迹重放、100,008 项原生输入检查、128 项与受保护程序的差分检查有独立证据记录。

**仓库包含工具、SDK 和受保护 EXE 吗？** 源码包提供脚本、恢复 IR、文本证据和真实截图；不包含原生分析工具、专有 SDK、目标二进制或内存转储。生成新的受保护样本需要自备 VMProtect 与 SDK。

**必须先配置 MCP 吗？** 离线 CLI 示例可以直接运行。宿主已有分析工具时可使用其原生工具清单；独立 Provider 的配置见[连接分析工具](#连接分析工具)。

## 文档导航

| 从这里开始 | 深入了解 |
| :--- | :--- |
| [快速上手指南](docs/getting-started.md) | [架构](docs/architecture.md) · [运行时](runtime/README.md) |
| [Agent Skill](SKILL.md) | [宿主集成](runtime/host-integration.md) · [Provider 配置](integrations/PROVIDER-SETUP.md) |
| [证据规范](references/evidence-policy.md) | [证据卡模板](templates/evidence-card.md) · [案例报告模板](templates/case-report.md) |
| [研究来源](references/source-registry.md) | [MCP 来源](references/mcp-source-registry.md) · [语料状态](corpus/STATUS.md) |
| [README 多语言](docs/translations.md) | 可用语言、翻译范围与维护约定 |

## 参与贡献

帮助下一次研究做得更好：提交一个**可复现案例**、一次**带版本信息的 Provider 实验**、一个**回归测试样例**，或一份**失败记录**。请附上环境、预期观测、实际结果和证据。

从[贡献指南](CONTRIBUTING.md)开始。当前优先事项是 Windows / Android 实测样例、独立环境复现，以及更丰富的版本化案例语料。

## 使用范围与许可

适用于自有软件、授权评估、隔离环境中的恶意软件分析、CTF、互操作研究、教学和防御性逆向。不可信样本应在隔离环境中运行；运行时本身不提供沙箱，执行与存储模型见[安全策略](SECURITY.md)。

[MIT](LICENSE) · 上游工具与 Provider 保留各自的许可。
