<div align="center">

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/assets/readme-hero-dark-mobile.svg">
  <source media="(max-width: 600px)" srcset="docs/assets/readme-hero-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/readme-hero-dark.svg">
  <img src="docs/assets/readme-hero.svg" alt="REU — Um método de engenharia reversa para seu agente de IA: da análise inicial à reconstrução verificada." width="100%">
</picture>

# Reverse Engineering & Unpacking

**Um método de engenharia reversa para seu agente de IA: da análise inicial à reconstrução verificada.**

Windows / .NET · Android / DEX · Native / ELF

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&labelColor=253044)](pyproject.toml)
[![Version 1.5.0](https://img.shields.io/badge/Version-1.5.0-5C6F91?style=flat-square&labelColor=253044)](CHANGELOG.md)
[![MIT License](https://img.shields.io/badge/License-MIT-4F8565?style=flat-square&labelColor=253044)](LICENSE)

[**Casos medidos**](#measured-cases) · [**Início rápido**](#quick-start) · [CI e downloads](https://github.com/rancy777/reu/actions/workflows/ci.yml?query=branch%3Amain) · [Documentação](#documentation)

[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · **Português (Brasil)** · [Русский](README.ru.md)

</div>

O REU combina **Agent Skill + CLI em Python** para examinar arquivos, planejar experimentos, conectar ferramentas de análise existentes e preservar resultados verificáveis. Você fornece a amostra e o ambiente; o REU fornece o processo de investigação, o roteamento e os registros.

<a id="measured-cases"></a>

## Casos medidos

**VMProtect 3.8.4 · Windows x64 · 2026-10-17**

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/assets/readme-cases-dark-mobile.svg">
  <source media="(max-width: 600px)" srcset="docs/assets/readme-cases-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/readme-cases-dark.svg">
  <img src="docs/assets/readme-cases.svg" alt="Casos medidos — VMProtect 3.8.4 x64" width="100%">
</picture>

- **[Empacotamento → reconstrução de EXE independente](docs/cases/vmprotect-3.8.4-x64.md)** — Um dump em execução e o reparo das importações produziram um EXE executável de forma independente. **45/45 verificações de comportamento e 14/14 de estrutura aprovadas**. [Código e validação](examples/vmprotect-3.8.4-x64).
- **[Virtualização de função → semântica nativa](docs/cases/vmprotect-3.8.4-virtualized-x64.md)** — Rastreamento real do depurador → expressão recuperada → função nativa compilada. **53 instruções, 100 008 verificações de entrada e 128 comparações diferenciais com o programa protegido**. [Código e validação](examples/vmprotect-3.8.4-virtualized-x64).

São duas amostras próprias com configurações de proteção diferentes. O caso de empacotamento usou um OEP conhecido e reparos manuais das importações. A recuperação abrange **uma única função pura**, com um harness de testes CLI compilado separadamente; a equivalência SMT para todo o domínio continua sem comprovação. Não é uma restauração byte a byte da função original nem do EXE inteiro.

[![Janela real do DIE exibindo o início da função nativa recuperada](docs/assets/vmp-3.8.4-virtualized-x64/07-recovered-native-function.jpg)](docs/assets/vmp-3.8.4-virtualized-x64/07-recovered-native-function.jpg)

Capturas reais de desassemblagem estática. Clique para ver em tamanho original. Configurações, tentativas malsucedidas, hashes e limites estão nos relatórios.

<details>
<summary>Comparação interna: antes da proteção → protegido → reconstruído</summary>

**Antes da proteção: ponto de entrada original**

![Antes da proteção: ponto de entrada original](docs/assets/vmp-3.8.4-x64/18-original-entrypoint.jpg)

**Protegido: ponto de entrada do protetor**

![Protegido: ponto de entrada do protetor](docs/assets/vmp-3.8.4-x64/19-protected-entrypoint.jpg)

**Reconstruído: ponto de entrada original e importações reparadas**

![Reconstruído: ponto de entrada original e importações reparadas](docs/assets/vmp-3.8.4-x64/20-unpacked-entrypoint.jpg)

</details>

<details>
<summary>Comparação da função: cálculo original → entrada da VM → instruções nativas recuperadas</summary>

**Antes da virtualização: cálculo marcado pelo SDK**

![Antes da virtualização: cálculo marcado pelo SDK](docs/assets/vmp-3.8.4-virtualized-x64/06-original-function.jpg)

**Virtualizado: entrada na máquina virtual do VMP**

![Virtualizado: entrada na máquina virtual do VMP](docs/assets/vmp-3.8.4-virtualized-x64/05-virtualized-function.jpg)

**Recuperado: instruções nativas compiladas a partir da semântica recuperada**

![Recuperado: instruções nativas compiladas a partir da semântica recuperada](docs/assets/vmp-3.8.4-virtualized-x64/07-recovered-native-function.jpg)

</details>

<a id="quick-start"></a>

## Início rápido

É necessário **Python 3.11+** e acesso a este repositório privado. Execute os comandos na raiz do projeto.

```bash
git clone https://github.com/rancy777/reu.git
cd reu
python -m pip install -e .
re-skill route --input runtime/examples/triage.sample.json
```

Não é necessário servidor MCP nem executar o arquivo-alvo. Os metadados sintéticos incluídos declaram carregamento dinâmico de DEX, selecionando os fluxos correspondentes. `Unknown` permanece explicitamente desconhecido.

<details>
<summary>Trecho da saída real</summary>

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

</details>

Para a análise inicial de um arquivo que você tem autorização para examinar:

```bash
re-skill triage --file ./sample.exe --route
```

Registra SHA-256, examina as estruturas compatíveis e recomenda um fluxo **sem executar o alvo**.

### Usar com seu agente

Instale o Skill local completo. O instalador para se o destino já existir.

```bash
python scripts/install_skill.py
```

```text
$reverse-engineering-unpacking
Analise ./sample.exe, que tenho autorização para examinar.
Comece com análise somente de leitura: SHA-256, arquitetura e indícios de proteção.
Proponha o próximo experimento, explique o que ele verifica e preserve as evidências. Separe fatos, hipóteses e informações desconhecidas.
```

O destino padrão é `~/.agents/skills/reverse-engineering-unpacking`. Instale a CLI separadamente e informe ao agente o caminho absoluto do executável ao trabalhar em outro diretório.

### Recompilar a demonstração nativa

Requer **Windows x64, Python 3.11 x64, ferramentas de compilação C++ x64 do Visual Studio e Windows SDK**. Na raiz do projeto:

```powershell
powershell -NoProfile -File .\examples\vmprotect-3.8.4-virtualized-x64\source\rebuild_demo.ps1
```

Baixa uma versão fixa do llvmlite em um ambiente novo, compila o IR recuperado publicado e vincula a DLL e o harness CLI. Executa **45 verificações de comportamento** em um EXE renomeado e colocado sozinho. Não requer VMProtect nem SDK proprietário. A saída vai para `runtime-artifacts/vmp-native-demo`; diretórios existentes são recusados. Isso recompila um resultado registrado: não desempacota um novo alvo nem repete comparações com o programa protegido. [Código e validação](examples/vmprotect-3.8.4-virtualized-x64/README.md).

## Por que REU

- **Saber o que investigar em seguida.** Fluxos por plataforma com hipóteses, observações esperadas e diagnóstico de falhas.
- **Conectar as ferramentas existentes.** Descobrir capacidades MCP reais e planejar chamadas conforme os esquemas de entrada disponíveis.
- **Tornar os resultados verificáveis.** Preservar hashes, rastreamentos, verificações e experimentos que falharam.

## Escopo da pesquisa

| Alvo | Análise inicial e roteamento integrados | Continuar com |
| :--- | :--- | :--- |
| **Windows PE / .NET** | Cabeçalhos, arquitetura, indícios de CLR, seções e entropia | [Windows](workflows/windows-triage.md) · [.NET](workflows/windows-dotnet.md) |
| **Android APK / AAB** | Estrutura do pacote, inventário DEX/nativo e pacotes divididos | [Android](workflows/android-triage.md) · [Splits / AAB](workflows/android-split-aab.md) |
| **DEX / ART** | Identificação de DEX, CDEX e VDEX; artefatos de execução | [DEX](workflows/android-dex.md) · [ART](workflows/android-art-runtime.md) |
| **Native ELF / SO** | Identidade e arquitetura ELF; roteamento Android com o contexto fornecido | [ELF](workflows/native-elf-triage.md) · [Android native](workflows/android-native.md) |

Os guias cobrem desempacotamento, carregamento dinâmico e proteções complexas. A reconstrução exige ferramentas externas, experimentos específicos e validação.

## Conectar ferramentas

Se o ambiente já expõe ferramentas MCP, use o [modo nativo do host](runtime/host-integration.md). Para uma ponte independente:

```bash
python -m pip install -e '.[mcp]'
```

Crie `providers.json` a partir do [modelo desativado](runtime/config/providers.ready-to-install.json) e configure o servidor instalado com [Provider Setup](integrations/PROVIDER-SETUP.md).

```bash
re-skill doctor --config ./providers.json
re-skill discover --config ./providers.json --registry ./integrations/mcp-provider-registry.yaml --output discovery.json
```

`doctor` verifica offline. `discover` inicia provedores ativados e aprovados pelo registro. A ponte aceita stdio e Streamable HTTP, com autorizações separadas para execução e alteração. IDA, Ghidra, x64dbg, WinDbg, JADX e Frida são candidatos no [catálogo](integrations/mcp-upstream-catalog.yaml); a presença na lista não certifica compatibilidade.

## Estado do projeto

**v1.5.0 · versão candidata para avaliação técnica.** Há dois experimentos registrados com ferramentas nativas do Windows; ampliar a cobertura de amostras continua pendente. Provedores MCP de terceiros seguem suas instruções originais; repetir sua validação não é requisito de publicação. A CI Windows/Ubuntu verifica Python 3.11–3.14, instalação, integridade do código e demonstração nativa. Execuções bem-sucedidas disponibilizam ZIPs de código verificado, wheels e evidências em **Artifacts**.

```bash
python -m pip install -e '.[test]'
python -m pytest -q runtime/tests
re-skill regress --strict --file corpus/regression/automated.jsonl
```

A verificação automática contém 16 registros executáveis. O conjunto separado de pesquisa mantém 5 PARTIAL / 3 MANUAL; seu modo estrito retorna intencionalmente o código 2. Os 24 registros originais e suas asserções são preservados.

## Perguntas frequentes

**Um comando desempacota qualquer programa VMP?** Não. A CLI faz análise inicial, roteamento e operações de evidência. Os dois casos medidos não constituem um desempacotador universal.

**O que a demonstração reproduz?** A compilação de LLVM IR já recuperado e 45 testes funcionais do harness. A reprodução de rastreamentos, as 100 008 entradas e as 128 comparações com o programa protegido têm evidências separadas.

**Ferramentas e executáveis protegidos estão incluídos?** Inclui scripts, IR recuperado, evidências em texto e capturas reais. Exclui ferramentas nativas, SDKs proprietários, binários-alvo e dumps de memória. Uma nova amostra protegida exige sua instalação do VMProtect e seu SDK.

<a id="documentation"></a>

## Documentação

[Primeiros passos](docs/getting-started.md) · [Arquitetura](docs/architecture.md) · [Agent Skill](SKILL.md) · [Política de evidências](references/evidence-policy.md) · [Verificação](docs/verification.md) · [Escopo e trabalho restante](docs/project-status.md)

Esta página é uma visão geral localizada. Relatórios e guias detalhados mantêm seu idioma atual. Política de manutenção das traduções: [Translations](docs/translations.md).

## Contribuir

Contribua com casos reproduzíveis, experimentos de provedores com versões identificadas, fixtures de regressão ou falhas documentadas. Inclua ambiente, observação esperada, resultado real e evidências. [Contributing](CONTRIBUTING.md).

## Uso responsável e licença

Para software próprio, avaliações autorizadas, análise isolada de malware, CTFs, interoperabilidade, educação e pesquisa defensiva. Execute amostras não confiáveis em ambiente isolado. O runtime não é uma sandbox. Ferramentas e provedores externos mantêm suas próprias licenças. [Security](SECURITY.md).

[MIT](LICENSE) · [English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · **Português (Brasil)** · [Русский](README.ru.md)
