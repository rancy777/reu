# README translations

REU has nine README entry points. Choose the language you read most comfortably; every page links to all the others.

| Language | README |
| :--- | :--- |
| English | [English](../README.md) |
| 简体中文 | [简体中文](../README.zh-CN.md) |
| 日本語 | [日本語](../README.ja.md) |
| 한국어 | [한국어](../README.ko.md) |
| Español | [Español](../README.es.md) |
| Français | [Français](../README.fr.md) |
| Deutsch | [Deutsch](../README.de.md) |
| Português (Brasil) | [Português (Brasil)](../README.pt-BR.md) |
| Русский | [Русский](../README.ru.md) |

## Scope

The localized entry points cover the project, both measured cases, real comparison screenshots, installation, agent usage, the native demo, supported targets, MCP setup, project status, FAQ and responsible use. They are concise introductions, not line-for-line copies of every paragraph in the English README.

Detailed workflow guides, case reports, code, CLI output and screenshots retain their current languages. The language selector describes README availability; it does not imply a translated runtime, localized third-party tools or independently repeated experiments for each locale. Shared diagrams retain their English labels, while the surrounding text explains the results in the selected language. Native-tool screenshots remain unedited evidence.

The seven new localized overviews were prepared against **v1.5.0**, using the English and Simplified Chinese entry points and the case reports, on **2026-10-17**. Locale-specific technical wording can still benefit from review by native-speaking contributors. Do not label a translation as independently or professionally reviewed unless that review happened.

## Keep the pages consistent

Use `README.md` as the source for shared product facts. When a change affects installation, prerequisites, protection settings, measured results or limitations, update every affected README in the same change. Keep code blocks, executable names, paths, JSON keys, configuration values and reported results unchanged. Translate explanatory prose and agent prompts, not executable commands or observed output.

Preserve these distinctions in every language:

- The packing and function-virtualization cases use **two different owned samples and configurations**.
- Packing reconstruction used a **known OEP and manual import repairs**.
- Function recovery covers **one pure function**. Its **53 native instructions**, **100,008 input checks** and **128 protected-program comparisons** do not establish full-domain equivalence. The SMT proof remains incomplete.
- The public native-demo helper rebuilds **already recovered IR**, with a separately compiled CLI harness and **45 behavior checks**. It does not recover a new target or repeat the original trace and protected-program comparisons.
- The repository is currently **private**. Cloning requires access. Tool and SDK installation remain separate.
- A catalog entry does not certify an MCP provider. Repeating upstream-provider validation is not a release prerequisite.

Use the current root README filenames, native language names and reciprocal links. Do not add flag icons as language identifiers, placeholder pages, a second language-selector implementation or an automated translation dependency. New translations should contain a useful overview before being added to the selector.

## Review a translation change

Check all relative files, images, in-page anchors and language links. Compare command blocks and JSON output with the English entry point. Review the rendered pages at narrow mobile and desktop widths in light and dark themes; expand the comparison panels too. Long translated text must wrap without hiding the installation commands or removing access to screenshots.

Run the project checks required by [Contributing](../CONTRIBUTING.md), then refresh and verify `MANIFEST.json` with the existing release script. Translated Markdown files belong in the source archive; local previews, rendering scripts and QA images do not.
