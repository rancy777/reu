<div align="center">

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/assets/readme-hero-dark-mobile.svg">
  <source media="(max-width: 600px)" srcset="docs/assets/readme-hero-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/readme-hero-dark.svg">
  <img src="docs/assets/readme-hero.svg" alt="REU — 초기 조사부터 검증된 재구성까지, AI 에이전트에 리버스 엔지니어링 절차를 제공합니다." width="100%">
</picture>

# Reverse Engineering & Unpacking

**초기 조사부터 검증된 재구성까지, AI 에이전트에 리버스 엔지니어링 절차를 제공합니다.**

Windows / .NET · Android / DEX · Native / ELF

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&labelColor=253044)](pyproject.toml)
[![Version 1.5.0](https://img.shields.io/badge/Version-1.5.0-5C6F91?style=flat-square&labelColor=253044)](CHANGELOG.md)
[![MIT License](https://img.shields.io/badge/License-MIT-4F8565?style=flat-square&labelColor=253044)](LICENSE)

[**실측 사례**](#measured-cases) · [**빠른 시작**](#quick-start) · [CI 및 다운로드](https://github.com/rancy777/reu/actions/workflows/ci.yml?query=branch%3Amain) · [문서](#documentation)

[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · **한국어** · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md) · [Русский](README.ru.md)

</div>

REU는 **Agent Skill + Python CLI**입니다. 파일을 조사하고 실험을 계획하며 기존 분석 도구를 연결하고 검증 가능한 기록을 남깁니다. 사용자가 샘플과 분석 환경을 준비하면 REU가 조사 절차, 라우팅, 증거 정리를 지원합니다.

<a id="measured-cases"></a>

## 실측 사례

**VMProtect 3.8.4 · Windows x64 · 2026-10-17**

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/assets/readme-cases-dark-mobile.svg">
  <source media="(max-width: 600px)" srcset="docs/assets/readme-cases-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/readme-cases-dark.svg">
  <img src="docs/assets/readme-cases.svg" alt="실측 사례 — VMProtect 3.8.4 x64" width="100%">
</picture>

- **[패킹 → 독립 실행 EXE 재구성](docs/cases/vmprotect-3.8.4-x64.md)** — 실행 중 덤프와 임포트 복구로 독립 실행 가능한 EXE를 만들었습니다. **동작 검사 45/45개, 구조 검사 14/14개 통과**. [소스 및 검증 기록](examples/vmprotect-3.8.4-x64).
- **[함수 가상화 → 네이티브 의미 재구성](docs/cases/vmprotect-3.8.4-virtualized-x64.md)** — 실제 디버거 트레이스 → 복원한 식 → 컴파일한 네이티브 함수. **명령어 53개, 입력 검사 100,008회, 보호된 프로그램과 차등 비교 128회**. [소스 및 검증 기록](examples/vmprotect-3.8.4-virtualized-x64).

직접 제작한 두 샘플을 서로 다른 보호 설정으로 검증했습니다. 패킹 사례는 알려진 OEP와 수동 임포트 복구를 사용했습니다. 가상화 사례는 **순수 함수 하나**의 의미 재구성이며 CLI 테스트 하네스는 별도로 빌드했습니다. 전체 입력 영역에 대한 SMT 동등성 증명은 완료하지 못했습니다. 원래 함수나 EXE 전체를 바이트 단위로 복원한 결과가 아닙니다.

[![복원한 네이티브 함수를 표시하는 실제 DIE 창](docs/assets/vmp-3.8.4-virtualized-x64/07-recovered-native-function.jpg)](docs/assets/vmp-3.8.4-virtualized-x64/07-recovered-native-function.jpg)

실제 정적 디스어셈블리 화면입니다. 이미지를 누르면 원본 크기로 볼 수 있습니다. 설정, 실패한 시도, 해시, 적용 범위는 사례 보고서에 기록되어 있습니다.

<details>
<summary>내부 비교: 보호 전 → 보호 후 → 재구성 후</summary>

**보호 전: 원래 진입점**

![보호 전: 원래 진입점](docs/assets/vmp-3.8.4-x64/18-original-entrypoint.jpg)

**보호 후: 보호기 진입점**

![보호 후: 보호기 진입점](docs/assets/vmp-3.8.4-x64/19-protected-entrypoint.jpg)

**재구성 후: 원래 진입점과 복구한 임포트**

![재구성 후: 원래 진입점과 복구한 임포트](docs/assets/vmp-3.8.4-x64/20-unpacked-entrypoint.jpg)

</details>

<details>
<summary>함수 내부 비교: 원래 연산 → VM 진입 → 복원한 네이티브 명령어</summary>

**가상화 전: SDK로 표시한 연산 함수**

![가상화 전: SDK로 표시한 연산 함수](docs/assets/vmp-3.8.4-virtualized-x64/06-original-function.jpg)

**가상화 후: VMP 가상 머신 진입점**

![가상화 후: VMP 가상 머신 진입점](docs/assets/vmp-3.8.4-virtualized-x64/05-virtualized-function.jpg)

**재구성 후: 복원한 의미에서 컴파일한 네이티브 명령어**

![재구성 후: 복원한 의미에서 컴파일한 네이티브 명령어](docs/assets/vmp-3.8.4-virtualized-x64/07-recovered-native-function.jpg)

</details>

<a id="quick-start"></a>

## 빠른 시작

**Python 3.11+**와 이 비공개 저장소에 대한 접근 권한이 필요합니다. 프로젝트 루트에서 실행하세요.

```bash
git clone https://github.com/rancy777/reu.git
cd reu
python -m pip install -e .
re-skill route --input runtime/examples/triage.sample.json
```

MCP 서버나 대상 실행이 필요하지 않습니다. 포함된 합성 메타데이터가 동적 DEX 로딩을 선언하므로 해당 워크플로로 라우팅됩니다. `Unknown`은 명시적으로 미확인 상태를 유지합니다.

<details>
<summary>실제 출력 일부</summary>

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

분석 권한이 있는 파일을 초기 조사하려면:

```bash
re-skill triage --file ./sample.exe --route
```

SHA-256, 지원되는 파일 구조, 권장 워크플로를 기록하며 **대상을 실행하지 않습니다**.

### 에이전트에서 사용

전체 Skill을 로컬에 설치합니다. 설치 대상이 이미 있으면 중단합니다.

```bash
python scripts/install_skill.py
```

```text
$reverse-engineering-unpacking
분석 권한이 있는 ./sample.exe를 조사하세요.
먼저 읽기 전용으로 SHA-256, 아키텍처, 보호 징후를 확인하세요.
다음 실험과 검증할 내용을 제안하고 증거를 남기세요. 사실, 가설, 미확인 사항을 구분하세요.
```

기본 설치 경로는 `~/.agents/skills/reverse-engineering-unpacking`입니다. CLI는 별도로 설치해야 합니다. 다른 디렉터리에서 작업할 때는 에이전트에 실행 파일의 절대 경로를 알려주세요.

### 네이티브 데모 다시 빌드

**Windows x64, Python 3.11 x64, Visual Studio C++ x64 빌드 도구 및 Windows SDK**가 필요합니다. 프로젝트 루트에서:

```powershell
powershell -NoProfile -File .\examples\vmprotect-3.8.4-virtualized-x64\source\rebuild_demo.ps1
```

새 환경에 고정 버전 llvmlite를 다운로드하고 공개된 복원 IR을 컴파일해 DLL과 CLI 하네스를 빌드합니다. 이름을 바꿔 단독 배치한 EXE에 **동작 검사 45개**를 실행합니다. VMProtect나 독점 SDK는 필요하지 않습니다. 출력은 `runtime-artifacts/vmp-native-demo`에 저장하며 기존 디렉터리를 덮어쓰지 않습니다. 기록된 복원 결과를 다시 빌드하는 절차로, 새로운 대상을 언패킹하거나 보호된 프로그램과 비교를 다시 실행하지 않습니다. [소스 및 검증 기록](examples/vmprotect-3.8.4-virtualized-x64/README.md).

## REU를 사용하는 이유

- **다음 조사 단계를 명확하게.** 가설, 예상 관측, 실패 진단을 포함한 플랫폼별 절차.
- **기존 도구 연결.** 실제 MCP 기능을 발견하고 공개된 입력 스키마에 맞춰 호출 계획 수립.
- **확인 가능한 결과.** 해시, 트레이스, 동작·구조 검사와 실패한 실험까지 보존.

## 연구 범위

| 대상 | 내장 초기 조사 및 라우팅 | 다음 단계 |
| :--- | :--- | :--- |
| **Windows PE / .NET** | 헤더, 아키텍처, CLR 징후, 섹션, 엔트로피 | [Windows](workflows/windows-triage.md) · [.NET](workflows/windows-dotnet.md) |
| **Android APK / AAB** | 패키지 구조, DEX와 네이티브 라이브러리 목록, split 지원 | [Android](workflows/android-triage.md) · [Splits / AAB](workflows/android-split-aab.md) |
| **DEX / ART** | DEX·CDEX·VDEX 식별과 런타임 산출물 라우팅 | [DEX](workflows/android-dex.md) · [ART](workflows/android-art-runtime.md) |
| **Native ELF / SO** | ELF 식별과 아키텍처, 제공된 문맥에 따른 Android 라우팅 | [ELF](workflows/native-elf-triage.md) · [Android native](workflows/android-native.md) |

가이드는 언패킹, 동적 로딩, 복잡한 보호 기법 연구를 다룹니다. 실제 재구성에는 외부 도구와 대상별 실험 및 검증이 필요합니다.

## 분석 도구 연결

호스트가 MCP 도구를 제공하면 [호스트 네이티브 모드](runtime/host-integration.md)를 사용할 수 있습니다. 별도 브리지가 필요하면:

```bash
python -m pip install -e '.[mcp]'
```

[비활성 템플릿](runtime/config/providers.ready-to-install.json)으로 `providers.json`을 만들고 [Provider Setup](integrations/PROVIDER-SETUP.md)에 따라 설치한 서버를 구성하세요.

```bash
re-skill doctor --config ./providers.json
re-skill discover --config ./providers.json --registry ./integrations/mcp-provider-registry.yaml --output discovery.json
```

`doctor`는 오프라인으로 검사합니다. `discover`는 활성화되어 있고 레지스트리에서 승인한 프로바이더를 시작합니다. stdio와 Streamable HTTP를 지원하며 실행과 변경은 별도 승인 게이트를 거칩니다. IDA, Ghidra, x64dbg, WinDbg, JADX, Frida는 [도구 카탈로그](integrations/mcp-upstream-catalog.yaml)의 후보이며, 목록에 있다는 사실이 호환성을 보증하지는 않습니다.

## 프로젝트 상태

**v1.5.0 · 기술 평가 후보 버전.** Windows 네이티브 도구를 이용한 실험 두 건을 기록했습니다. 더 넓은 샘플 검증은 남아 있습니다. 타사 MCP 프로바이더는 업스트림 설치 지침을 따르며 재검증은 릴리스의 필수 조건이 아닙니다. Windows/Ubuntu CI는 Python 3.11–3.14, 설치, 소스 무결성, 네이티브 데모를 검사합니다. 성공한 실행의 **Artifacts**에서 검증된 소스 ZIP, wheel, 데모 증거를 받을 수 있습니다.

```bash
python -m pip install -e '.[test]'
python -m pytest -q runtime/tests
re-skill regress --strict --file corpus/regression/automated.jsonl
```

자동 게이트에는 실행 가능한 레코드 16개가 있습니다. 별도 연구 데이터에는 5 PARTIAL / 3 MANUAL이 남아 있으며 strict 실행은 의도적으로 종료 코드 2를 반환합니다. 원래 레코드 24개와 어설션은 모두 보존되어 있습니다.

## 자주 묻는 질문

**명령 하나로 모든 VMP 프로그램을 언패킹하나요?** 아니요. CLI는 초기 조사, 라우팅, 증거 작업을 수행합니다. 실측 사례 두 건이 범용 언패커를 뜻하지 않습니다.

**데모가 재현하는 것은 무엇인가요?** 이미 복원된 LLVM IR의 컴파일과 하네스 기능 검사 45개입니다. 트레이스 재생, 입력 검사 100,008회, 보호된 프로그램과의 비교 128회는 별도 증거로 남아 있습니다.

**도구와 보호된 EXE가 포함되어 있나요?** 스크립트, 복원 IR, 텍스트 증거, 실제 스크린샷이 포함됩니다. 네이티브 도구, 독점 SDK, 대상 바이너리, 메모리 덤프는 제외됩니다. 새 보호 샘플을 만들려면 자체 VMProtect 설치와 SDK가 필요합니다.

<a id="documentation"></a>

## 문서

[시작 가이드](docs/getting-started.md) · [아키텍처](docs/architecture.md) · [Agent Skill](SKILL.md) · [증거 정책](references/evidence-policy.md) · [검증 기록](docs/verification.md) · [범위 및 남은 작업](docs/project-status.md)

이 페이지는 현지화된 개요입니다. 상세 보고서와 가이드는 현재 작성 언어를 유지합니다. 번역 유지 관리 방침: [Translations](docs/translations.md).

## 기여

재현 가능한 사례, 버전이 명시된 프로바이더 실험, 회귀 픽스처, 실패 기록을 환영합니다. 환경, 예상 관측, 실제 결과, 증거를 함께 제출하세요. [Contributing](CONTRIBUTING.md).

## 책임 있는 사용과 라이선스

소유한 소프트웨어, 허가된 평가, 격리된 악성코드 분석, CTF, 상호운용성, 교육, 방어 연구를 위한 도구입니다. 신뢰할 수 없는 샘플은 격리된 환경에서 실행하세요. 런타임 자체는 샌드박스가 아닙니다. 업스트림 도구와 프로바이더에는 각자의 라이선스가 적용됩니다. [Security](SECURITY.md).

[MIT](LICENSE) · [English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · **한국어** · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md) · [Русский](README.ru.md)
