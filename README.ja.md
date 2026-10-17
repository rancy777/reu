<div align="center">

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/assets/readme-hero-dark-mobile.svg">
  <source media="(max-width: 600px)" srcset="docs/assets/readme-hero-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/readme-hero-dark.svg">
  <img src="docs/assets/readme-hero.svg" alt="REU — AI エージェントに、初期調査から検証済みの再構築までを進めるリバースエンジニアリングの手順を。" width="100%">
</picture>

# Reverse Engineering & Unpacking

**AI エージェントに、初期調査から検証済みの再構築までを進めるリバースエンジニアリングの手順を。**

Windows / .NET · Android / DEX · Native / ELF

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&labelColor=253044)](pyproject.toml)
[![Version 1.5.0](https://img.shields.io/badge/Version-1.5.0-5C6F91?style=flat-square&labelColor=253044)](CHANGELOG.md)
[![MIT License](https://img.shields.io/badge/License-MIT-4F8565?style=flat-square&labelColor=253044)](LICENSE)

[**実測ケース**](#measured-cases) · [**クイックスタート**](#quick-start) · [CI とダウンロード](https://github.com/rancy777/reu/actions/workflows/ci.yml?query=branch%3Amain) · [ドキュメント](#documentation)

[English](README.md) · [简体中文](README.zh-CN.md) · **日本語** · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md) · [Русский](README.ru.md)

</div>

REU は **Agent Skill + Python CLI** です。検体を調べ、実験を計画し、既存の解析ツールに接続して、検証可能な記録を残します。検体と解析環境は利用者が用意し、REU が調査の手順、ルーティング、証拠の整理を支援します。

<a id="measured-cases"></a>

## 実測ケース

**VMProtect 3.8.4 · Windows x64 · 2026-10-17**

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/assets/readme-cases-dark-mobile.svg">
  <source media="(max-width: 600px)" srcset="docs/assets/readme-cases-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/readme-cases-dark.svg">
  <img src="docs/assets/readme-cases.svg" alt="実測ケース — VMProtect 3.8.4 x64" width="100%">
</picture>

- **[パッキング → 単体で動作する EXE の再構築](docs/cases/vmprotect-3.8.4-x64.md)** — 実行時ダンプとインポート修復により、単独で実行できる EXE を再構築。**45/45 件の動作検査、14/14 件の構造検査に合格**。 [ソースと検証記録](examples/vmprotect-3.8.4-x64).
- **[関数の仮想化 → ネイティブな意味の再構築](docs/cases/vmprotect-3.8.4-virtualized-x64.md)** — 実際のデバッガートレース → 復元した式 → コンパイルしたネイティブ関数。**53 命令、100,008 件の入力検査、保護版との 128 件の差分比較**。 [ソースと検証記録](examples/vmprotect-3.8.4-virtualized-x64).

自作の 2 つの検体を、異なる保護設定で検証しています。パッキングのケースでは既知の OEP と手動のインポート修復を使用しました。仮想化のケースは **1 つの純粋関数** の意味の再構築です。CLI テストハーネスは別途ビルドしており、全入力領域に対する SMT 等価性証明は未完了です。元の関数や EXE 全体をバイト単位で復元したものではありません。

[![復元したネイティブ関数を表示する実際の DIE ウィンドウ](docs/assets/vmp-3.8.4-virtualized-x64/07-recovered-native-function.jpg)](docs/assets/vmp-3.8.4-virtualized-x64/07-recovered-native-function.jpg)

実際の静的逆アセンブル画面です。画像をクリックすると原寸で確認できます。設定、失敗した試行、ハッシュ、適用範囲はケースレポートに記録しています。

<details>
<summary>内部比較：保護前 → 保護後 → 再構築後</summary>

**保護前：元のエントリーポイント**

![保護前：元のエントリーポイント](docs/assets/vmp-3.8.4-x64/18-original-entrypoint.jpg)

**保護後：保護器のエントリーポイント**

![保護後：保護器のエントリーポイント](docs/assets/vmp-3.8.4-x64/19-protected-entrypoint.jpg)

**再構築後：元のエントリーポイントと修復したインポート**

![再構築後：元のエントリーポイントと修復したインポート](docs/assets/vmp-3.8.4-x64/20-unpacked-entrypoint.jpg)

</details>

<details>
<summary>関数の内部比較：元の演算 → VM 入口 → 復元したネイティブ命令</summary>

**仮想化前：SDK でマークした演算関数**

![仮想化前：SDK でマークした演算関数](docs/assets/vmp-3.8.4-virtualized-x64/06-original-function.jpg)

**仮想化後：VMP 仮想マシンへの入口**

![仮想化後：VMP 仮想マシンへの入口](docs/assets/vmp-3.8.4-virtualized-x64/05-virtualized-function.jpg)

**再構築後：復元した意味からコンパイルしたネイティブ命令**

![再構築後：復元した意味からコンパイルしたネイティブ命令](docs/assets/vmp-3.8.4-virtualized-x64/07-recovered-native-function.jpg)

</details>

<a id="quick-start"></a>

## クイックスタート

**Python 3.11+** と、この非公開リポジトリへのアクセス権が必要です。プロジェクトのルートから実行してください。

```bash
git clone https://github.com/rancy777/reu.git
cd reu
python -m pip install -e .
re-skill route --input runtime/examples/triage.sample.json
```

MCP サーバーも対象ファイルの実行も不要です。付属の合成メタデータは DEX の動的ロードを宣言しているため、対応するワークフローに振り分けられます。`Unknown` は不明のまま明示されます。

<details>
<summary>実際の出力の抜粋</summary>

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

解析する権限のあるファイルを初期調査するには：

```bash
re-skill triage --file ./sample.exe --route
```

SHA-256、対応するファイル構造、推奨ワークフローを記録し、**対象を実行しません**。

### エージェントから使う

Skill 全体をローカルにインストールします。インストール先が既に存在する場合は停止します。

```bash
python scripts/install_skill.py
```

```text
$reverse-engineering-unpacking
解析する権限のある ./sample.exe を調べてください。
まず読み取り専用で SHA-256、アーキテクチャ、保護の兆候を調査してください。
次の実験と検証事項を提案し、証拠を保存してください。事実・仮説・不明点を区別してください。
```

既定のインストール先は `~/.agents/skills/reverse-engineering-unpacking` です。CLI は別途インストールしてください。他の作業ディレクトリでは、実行ファイルの絶対パスをエージェントに伝えます。

### ネイティブデモを再ビルドする

**Windows x64、Python 3.11 x64、Visual Studio の C++ x64 ビルドツール、Windows SDK** が必要です。プロジェクトのルートから：

```powershell
powershell -NoProfile -File .\examples\vmprotect-3.8.4-virtualized-x64\source\rebuild_demo.ps1
```

固定バージョンの llvmlite を新しい環境にダウンロードし、公開済みの復元 IR から DLL と CLI ハーネスをビルドします。名前を変えて単独配置した EXE に **45 件の動作検査** を実施します。VMProtect や独自 SDK は不要です。出力先は `runtime-artifacts/vmp-native-demo` で、既存ディレクトリは上書きしません。これは記録済みの復元結果の再ビルドであり、新しい検体のアンパックや保護版との比較の再実行ではありません。 [ソースと検証記録](examples/vmprotect-3.8.4-virtualized-x64/README.md).

## REU を使う理由

- **次の調査を明確に。** 仮説、期待する観測結果、失敗時の診断を含む手順。
- **既存のツールを活用。** 実際の MCP 機能を検出し、公開された入力スキーマに合わせて呼び出しを計画。
- **結果を検証可能に。** ハッシュ、トレース、動作・構造検査、失敗した実験も記録。

## 調査範囲

| 対象 | 組み込みの初期調査とルーティング | 次の手順 |
| :--- | :--- | :--- |
| **Windows PE / .NET** | ヘッダー、アーキテクチャ、CLR の兆候、セクション、エントロピー | [Windows](workflows/windows-triage.md) · [.NET](workflows/windows-dotnet.md) |
| **Android APK / AAB** | パッケージ構造、DEX とネイティブライブラリ、split 対応 | [Android](workflows/android-triage.md) · [Splits / AAB](workflows/android-split-aab.md) |
| **DEX / ART** | DEX・CDEX・VDEX の識別と実行時アーティファクト | [DEX](workflows/android-dex.md) · [ART](workflows/android-art-runtime.md) |
| **Native ELF / SO** | ELF の識別とアーキテクチャ、指定された文脈による Android への振り分け | [ELF](workflows/native-elf-triage.md) · [Android native](workflows/android-native.md) |

ガイドはアンパック、動的ロード、複雑な保護の調査を扱います。実際の再構築には外部ツール、対象ごとの実験、検証が必要です。

## 解析ツールを接続する

ホストが MCP ツールを公開している場合は [ホストネイティブモード](runtime/host-integration.md) を利用できます。独立したブリッジを使う場合：

```bash
python -m pip install -e '.[mcp]'
```

[無効化済みテンプレート](runtime/config/providers.ready-to-install.json) から `providers.json` を作成し、[Provider Setup](integrations/PROVIDER-SETUP.md) に従ってインストール済みサーバーを設定します。

```bash
re-skill doctor --config ./providers.json
re-skill discover --config ./providers.json --registry ./integrations/mcp-provider-registry.yaml --output discovery.json
```

`doctor` はオフライン検査です。`discover` は有効でレジストリ承認済みのプロバイダーを起動します。stdio と Streamable HTTP に対応し、実行と変更には別々の認可ゲートがあります。IDA、Ghidra、x64dbg、WinDbg、JADX、Frida は [ツールカタログ](integrations/mcp-upstream-catalog.yaml) の候補であり、掲載自体は互換性の認定ではありません。

## プロジェクトの状態

**v1.5.0 · 技術評価用候補版。** Windows のネイティブツールを使った 2 件の実験を記録しています。幅広い検体への対応は今後の課題です。サードパーティーの MCP は各提供元の導入手順に従い、再検証をリリースの前提にはしていません。Windows/Ubuntu の CI は Python 3.11–3.14、インストール、ソースの整合性、ネイティブデモを検査します。成功した実行の **Artifacts** に、検証済みソース ZIP、wheel、デモの証拠が保存されます。

```bash
python -m pip install -e '.[test]'
python -m pytest -q runtime/tests
re-skill regress --strict --file corpus/regression/automated.jsonl
```

自動ゲートは実行可能な 16 レコードです。別の研究データは 5 PARTIAL / 3 MANUAL を保持し、strict 実行は意図的に終了コード 2 を返します。元の 24 レコードとアサーションは保持されています。

## よくある質問

**1 コマンドで任意の VMP をアンパックできますか？** いいえ。CLI の役割は初期調査、ルーティング、証拠操作です。2 件の実測ケースは汎用アンパッカーを意味しません。

**デモは何を再現しますか？** 既に復元された LLVM IR のコンパイルと、ハーネスの 45 件の機能検査です。トレース再生、100,008 件の入力検査、128 件の保護版比較には別の証拠があります。

**ツールや保護済み EXE は含まれますか？** スクリプト、復元 IR、テキストの証拠、実際のスクリーンショットを含みます。ネイティブツール、独自 SDK、対象バイナリ、メモリダンプは含みません。新しい保護検体の作成には自分の VMProtect と SDK が必要です。

<a id="documentation"></a>

## ドキュメント

[導入ガイド](docs/getting-started.md) · [アーキテクチャ](docs/architecture.md) · [Agent Skill](SKILL.md) · [証拠ポリシー](references/evidence-policy.md) · [検証記録](docs/verification.md) · [適用範囲と残作業](docs/project-status.md)

このページはローカライズされた概要です。詳細レポートとガイドは現在の記述言語のままです。翻訳の更新方針： [Translations](docs/translations.md).

## 貢献する

再現可能なケース、バージョンを明記したプロバイダー実験、回帰フィクスチャ、失敗の記録を歓迎します。環境、期待する観測、実際の結果、証拠を添えてください。 [Contributing](CONTRIBUTING.md).

## 責任ある利用とライセンス

自作ソフトウェア、認可された評価、隔離環境でのマルウェア解析、CTF、相互運用、教育、防御研究を対象とします。信頼できない検体は隔離環境で実行してください。ランタイム自体はサンドボックスではありません。上流のツールとプロバイダーには各自のライセンスが適用されます。 [Security](SECURITY.md).

[MIT](LICENSE) · [English](README.md) · [简体中文](README.zh-CN.md) · **日本語** · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md) · [Русский](README.ru.md)
