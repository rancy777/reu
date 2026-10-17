<div align="center">

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/assets/readme-hero-dark-mobile.svg">
  <source media="(max-width: 600px)" srcset="docs/assets/readme-hero-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/readme-hero-dark.svg">
  <img src="docs/assets/readme-hero.svg" alt="REU — Ein methodischer Ablauf für das Reverse Engineering mit KI-Agenten: von der ersten Analyse bis zur überprüften Rekonstruktion." width="100%">
</picture>

# Reverse Engineering & Unpacking

**Ein methodischer Ablauf für das Reverse Engineering mit KI-Agenten: von der ersten Analyse bis zur überprüften Rekonstruktion.**

Windows / .NET · Android / DEX · Native / ELF

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&labelColor=253044)](pyproject.toml)
[![Version 1.5.0](https://img.shields.io/badge/Version-1.5.0-5C6F91?style=flat-square&labelColor=253044)](CHANGELOG.md)
[![MIT License](https://img.shields.io/badge/License-MIT-4F8565?style=flat-square&labelColor=253044)](LICENSE)

[**Gemessene Fallstudien**](#measured-cases) · [**Schnellstart**](#quick-start) · [CI und Downloads](https://github.com/rancy777/reu/actions/workflows/ci.yml?query=branch%3Amain) · [Dokumentation](#documentation)

[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md) · **Deutsch** · [Português (Brasil)](README.pt-BR.md) · [Русский](README.ru.md)

</div>

REU besteht aus **Agent Skill + Python-CLI**. Es unterstützt die Untersuchung von Dateien, die Planung von Experimenten, die Anbindung vorhandener Analysewerkzeuge und die Aufzeichnung überprüfbarer Ergebnisse. Sie stellen Probe und Analyseumgebung bereit; REU liefert Vorgehen, Routing und Dokumentation.

<a id="measured-cases"></a>

## Gemessene Fallstudien

**VMProtect 3.8.4 · Windows x64 · 2026-10-17**

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/assets/readme-cases-dark-mobile.svg">
  <source media="(max-width: 600px)" srcset="docs/assets/readme-cases-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/readme-cases-dark.svg">
  <img src="docs/assets/readme-cases.svg" alt="Gemessene Fallstudien — VMProtect 3.8.4 x64" width="100%">
</picture>

- **[Packing → eigenständig ausführbare Rekonstruktion](docs/cases/vmprotect-3.8.4-x64.md)** — Ein Laufzeit-Dump und die Reparatur der Imports führten zu einer eigenständig ausführbaren EXE. **45/45 Verhaltensprüfungen und 14/14 Strukturprüfungen bestanden**. [Quellcode und Prüfbelege](examples/vmprotect-3.8.4-x64).
- **[Funktionsvirtualisierung → native Semantik](docs/cases/vmprotect-3.8.4-virtualized-x64.md)** — Echte Debugger-Aufzeichnung → rekonstruierter Ausdruck → kompilierte native Funktion. **53 Befehle, 100 008 Eingabeprüfungen und 128 Differenzvergleiche mit dem geschützten Programm**. [Quellcode und Prüfbelege](examples/vmprotect-3.8.4-virtualized-x64).

Zwei selbst erstellte Proben mit unterschiedlichen Schutzeinstellungen. Beim Packing wurden ein bekannter OEP und manuelle Import-Reparaturen verwendet. Die Wiederherstellung betrifft **eine einzelne reine Funktion** mit separat gebautem CLI-Testharness; ein SMT-Äquivalenzbeweis für den gesamten Eingabebereich steht aus. Die Originalfunktion oder die gesamte EXE wurde nicht bytegetreu wiederhergestellt.

[![Echtes DIE-Fenster mit dem Anfang der rekonstruierten nativen Funktion](docs/assets/vmp-3.8.4-virtualized-x64/07-recovered-native-function.jpg)](docs/assets/vmp-3.8.4-virtualized-x64/07-recovered-native-function.jpg)

Echte Aufnahmen der statischen Disassemblierung. Anklicken zeigt das Bild in voller Größe. Einstellungen, fehlgeschlagene Versuche, Hashes und Grenzen stehen in den Fallberichten.

<details>
<summary>Interner Vergleich: vor dem Schutz → geschützt → rekonstruiert</summary>

**Vor dem Schutz: ursprünglicher Einstiegspunkt**

![Vor dem Schutz: ursprünglicher Einstiegspunkt](docs/assets/vmp-3.8.4-x64/18-original-entrypoint.jpg)

**Geschützt: Einstiegspunkt des Schutzprogramms**

![Geschützt: Einstiegspunkt des Schutzprogramms](docs/assets/vmp-3.8.4-x64/19-protected-entrypoint.jpg)

**Rekonstruiert: ursprünglicher Einstiegspunkt und reparierte Imports**

![Rekonstruiert: ursprünglicher Einstiegspunkt und reparierte Imports](docs/assets/vmp-3.8.4-x64/20-unpacked-entrypoint.jpg)

</details>

<details>
<summary>Funktionsvergleich: ursprüngliche Berechnung → VM-Einstieg → rekonstruierte native Befehle</summary>

**Vor der Virtualisierung: mit dem SDK markierte Berechnung**

![Vor der Virtualisierung: mit dem SDK markierte Berechnung](docs/assets/vmp-3.8.4-virtualized-x64/06-original-function.jpg)

**Virtualisiert: Einstieg in die VMP-VM**

![Virtualisiert: Einstieg in die VMP-VM](docs/assets/vmp-3.8.4-virtualized-x64/05-virtualized-function.jpg)

**Rekonstruiert: aus der wiederhergestellten Semantik kompilierte native Befehle**

![Rekonstruiert: aus der wiederhergestellten Semantik kompilierte native Befehle](docs/assets/vmp-3.8.4-virtualized-x64/07-recovered-native-function.jpg)

</details>

<a id="quick-start"></a>

## Schnellstart

Sie benötigen **Python 3.11+** und Zugriff auf dieses private Repository. Führen Sie die Befehle im Projektstamm aus.

```bash
git clone https://github.com/rancy777/reu.git
cd reu
python -m pip install -e .
re-skill route --input runtime/examples/triage.sample.json
```

Weder ein MCP-Server noch die Ausführung der Zieldatei ist erforderlich. Die mitgelieferten synthetischen Metadaten deklarieren dynamisches DEX-Laden und wählen dadurch die zugehörigen Workflows. `Unknown` bleibt ausdrücklich unbekannt.

<details>
<summary>Ausschnitt der tatsächlichen Ausgabe</summary>

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

Für die erste Analyse einer Datei, zu deren Untersuchung Sie berechtigt sind:

```bash
re-skill triage --file ./sample.exe --route
```

Erfasst SHA-256, untersucht unterstützte Dateistrukturen und empfiehlt einen Workflow, **ohne die Zieldatei auszuführen**.

### Mit Ihrem Agenten verwenden

Installieren Sie den vollständigen lokalen Skill. Existiert das Zielverzeichnis bereits, bricht der Installer ab.

```bash
python scripts/install_skill.py
```

```text
$reverse-engineering-unpacking
Analysiere ./sample.exe; ich bin zur Untersuchung berechtigt.
Beginne lesend mit SHA-256, Architektur und Anzeichen für Schutzmechanismen.
Schlage das nächste Experiment vor, erkläre seine Prüfaussage und sichere die Belege. Trenne Fakten, Hypothesen und Unbekanntes.
```

Das Standardziel ist `~/.agents/skills/reverse-engineering-unpacking`. Installieren Sie die CLI separat und geben Sie dem Agenten bei Arbeit in anderen Verzeichnissen den absoluten Pfad zur ausführbaren Datei.

### Native Demo neu bauen

Erforderlich sind **Windows x64, Python 3.11 x64, die C++-x64-Buildtools von Visual Studio und ein Windows SDK**. Im Projektstamm:

```powershell
powershell -NoProfile -File .\examples\vmprotect-3.8.4-virtualized-x64\source\rebuild_demo.ps1
```

Lädt eine festgelegte llvmlite-Version in eine neue Umgebung, kompiliert die veröffentlichte rekonstruierte IR und bindet DLL und CLI-Testharness. Führt **45 Verhaltensprüfungen** an einer umbenannten, allein abgelegten EXE aus. VMProtect und proprietäres SDK sind nicht erforderlich. Ausgabe: `runtime-artifacts/vmp-native-demo`; vorhandene Verzeichnisse werden abgelehnt. Dies baut ein dokumentiertes Ergebnis erneut, entpackt aber kein neues Ziel und wiederholt keine Vergleiche mit dem geschützten Programm. [Quellcode und Prüfbelege](examples/vmprotect-3.8.4-virtualized-x64/README.md).

## Warum REU

- **Den nächsten Untersuchungsschritt kennen.** Plattformabläufe mit Hypothesen, erwarteten Beobachtungen und Fehlerdiagnose.
- **Vorhandene Werkzeuge anbinden.** Tatsächliche MCP-Funktionen erkennen und Aufrufe anhand der bereitgestellten Eingabeschemas planen.
- **Ergebnisse nachprüfbar machen.** Hashes, Aufzeichnungen, Prüfungen und fehlgeschlagene Experimente erhalten.

## Forschungsumfang

| Ziel | Integrierte Erstanalyse und Routing | Weiter mit |
| :--- | :--- | :--- |
| **Windows PE / .NET** | Header, Architektur, CLR-Indikatoren, Sektionen und Entropie | [Windows](workflows/windows-triage.md) · [.NET](workflows/windows-dotnet.md) |
| **Android APK / AAB** | Paketstruktur, DEX-/Native-Inventar und Split-Pakete | [Android](workflows/android-triage.md) · [Splits / AAB](workflows/android-split-aab.md) |
| **DEX / ART** | Erkennung von DEX, CDEX und VDEX; Laufzeitartefakte | [DEX](workflows/android-dex.md) · [ART](workflows/android-art-runtime.md) |
| **Native ELF / SO** | ELF-Identifikation und Architektur; Android-Routing mit übergebenem Kontext | [ELF](workflows/native-elf-triage.md) · [Android native](workflows/android-native.md) |

Die Anleitungen behandeln Entpacken, dynamisches Laden und komplexe Schutzmechanismen. Eine erfolgreiche Rekonstruktion erfordert externe Werkzeuge, zielspezifische Experimente und Validierung.

## Werkzeuge anbinden

Stellt Ihre Umgebung bereits MCP-Werkzeuge bereit, verwenden Sie den [nativen Host-Modus](runtime/host-integration.md). Für eine separate Bridge:

```bash
python -m pip install -e '.[mcp]'
```

Erstellen Sie `providers.json` aus der [deaktivierten Vorlage](runtime/config/providers.ready-to-install.json) und konfigurieren Sie Ihren installierten Server mit [Provider Setup](integrations/PROVIDER-SETUP.md).

```bash
re-skill doctor --config ./providers.json
re-skill discover --config ./providers.json --registry ./integrations/mcp-provider-registry.yaml --output discovery.json
```

`doctor` prüft offline. `discover` startet aktivierte, vom Register genehmigte Provider. Die Bridge unterstützt stdio und Streamable HTTP mit getrennten Freigaben für Ausführung und Änderungen. IDA, Ghidra, x64dbg, WinDbg, JADX und Frida sind Kandidaten im [Werkzeugkatalog](integrations/mcp-upstream-catalog.yaml); ein Eintrag bestätigt keine Kompatibilität.

## Projektstatus

**v1.5.0 · technischer Release-Kandidat.** Zwei Experimente mit nativen Windows-Werkzeugen sind dokumentiert; eine breitere Probenabdeckung steht aus. MCP-Provider von Dritten folgen ihren eigenen Installationsanweisungen; deren erneute Validierung ist keine Release-Voraussetzung. Die Windows-/Ubuntu-CI prüft Python 3.11–3.14, Installation, Quellintegrität und native Demo. Erfolgreiche Läufe bieten geprüfte Quell-ZIPs, Wheels und Demo-Belege unter **Artifacts**.

```bash
python -m pip install -e '.[test]'
python -m pytest -q runtime/tests
re-skill regress --strict --file corpus/regression/automated.jsonl
```

Das automatische Prüftor enthält 16 ausführbare Datensätze. Der separate Forschungsdatensatz erhält 5 PARTIAL / 3 MANUAL; sein strikter Lauf liefert absichtlich Exitcode 2. Alle 24 ursprünglichen Datensätze und Assertions bleiben erhalten.

## Häufige Fragen

**Entpackt ein Befehl jedes VMP-Programm?** Nein. Die CLI übernimmt Erstanalyse, Routing und Belegverwaltung. Die zwei gemessenen Fälle sind kein universeller Unpacker.

**Was reproduziert die native Demo?** Die Kompilierung bereits rekonstruierter LLVM-IR und 45 Funktionstests des Testharness. Trace-Replay, 100 008 Eingabeprüfungen und 128 Vergleiche mit dem geschützten Programm sind separat belegt.

**Sind Werkzeuge und geschützte Programme enthalten?** Enthalten sind Skripte, rekonstruierte IR, Textbelege und echte Screenshots. Native Werkzeuge, proprietäre SDKs, Zielbinärdateien und Speicherdumps sind ausgeschlossen. Für eine neue geschützte Probe benötigen Sie Ihre eigene VMProtect-Installation und das SDK.

<a id="documentation"></a>

## Dokumentation

[Erste Schritte](docs/getting-started.md) · [Architektur](docs/architecture.md) · [Agent Skill](SKILL.md) · [Belegrichtlinie](references/evidence-policy.md) · [Verifikation](docs/verification.md) · [Umfang und offene Arbeiten](docs/project-status.md)

Diese Seite ist eine lokalisierte Übersicht. Ausführliche Berichte und Anleitungen behalten ihre bisherige Sprache. Pflege der Übersetzungen: [Translations](docs/translations.md).

## Mitwirken

Beiträge können reproduzierbare Fälle, Provider-Experimente mit Versionsangaben, Regression-Fixtures oder dokumentierte Fehlschläge sein. Bitte Umgebung, erwartete Beobachtung, tatsächliches Ergebnis und Belege angeben. [Contributing](CONTRIBUTING.md).

## Verantwortungsvolle Nutzung und Lizenz

Für eigene Software, autorisierte Prüfungen, isolierte Malware-Analyse, CTFs, Interoperabilität, Lehre und defensive Forschung. Führen Sie nicht vertrauenswürdige Proben isoliert aus. Die Laufzeitumgebung ist keine Sandbox. Externe Werkzeuge und Provider behalten ihre jeweiligen Lizenzen. [Security](SECURITY.md).

[MIT](LICENSE) · [English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md) · **Deutsch** · [Português (Brasil)](README.pt-BR.md) · [Русский](README.ru.md)
