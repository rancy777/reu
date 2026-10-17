<div align="center">

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/assets/readme-hero-dark-mobile.svg">
  <source media="(max-width: 600px)" srcset="docs/assets/readme-hero-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/readme-hero-dark.svg">
  <img src="docs/assets/readme-hero.svg" alt="REU — Методика обратной разработки для ИИ-агента: от первичного анализа до проверенной реконструкции." width="100%">
</picture>

# Reverse Engineering & Unpacking

**Методика обратной разработки для ИИ-агента: от первичного анализа до проверенной реконструкции.**

Windows / .NET · Android / DEX · Native / ELF

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&labelColor=253044)](pyproject.toml)
[![Version 1.5.0](https://img.shields.io/badge/Version-1.5.0-5C6F91?style=flat-square&labelColor=253044)](CHANGELOG.md)
[![MIT License](https://img.shields.io/badge/License-MIT-4F8565?style=flat-square&labelColor=253044)](LICENSE)

[**Проверенные примеры**](#measured-cases) · [**Быстрый старт**](#quick-start) · [CI и загрузки](https://github.com/rancy777/reu/actions/workflows/ci.yml?query=branch%3Amain) · [Документация](#documentation)

[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md) · **Русский**

</div>

REU — это **Agent Skill + CLI на Python** для исследования файлов, планирования экспериментов, подключения существующих средств анализа и сохранения проверяемых результатов. Вы предоставляете образец и среду, а REU — порядок исследования, маршрутизацию и записи.

<a id="measured-cases"></a>

## Проверенные примеры

**VMProtect 3.8.4 · Windows x64 · 2026-10-17**

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/assets/readme-cases-dark-mobile.svg">
  <source media="(max-width: 600px)" srcset="docs/assets/readme-cases-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/readme-cases-dark.svg">
  <img src="docs/assets/readme-cases.svg" alt="Проверенные примеры — VMProtect 3.8.4 x64" width="100%">
</picture>

- **[Упаковка → реконструкция автономного EXE](docs/cases/vmprotect-3.8.4-x64.md)** — Дамп во время выполнения и исправление импортов позволили получить самостоятельно запускаемый EXE. **Пройдены 45/45 проверок поведения и 14/14 проверок структуры**. [Исходники и проверка](examples/vmprotect-3.8.4-x64).
- **[Виртуализация функции → нативная семантика](docs/cases/vmprotect-3.8.4-virtualized-x64.md)** — Реальная трасса отладчика → восстановленное выражение → скомпилированная нативная функция. **53 инструкции, 100 008 проверок входных данных и 128 дифференциальных сравнений с защищённой программой**. [Исходники и проверка](examples/vmprotect-3.8.4-virtualized-x64).

Это два собственных образца с разными настройками защиты. В примере распаковки использовались известная OEP и ручное исправление импортов. Восстановлена семантика **одной чистой функции**; тестовая оболочка CLI собрана отдельно. SMT-доказательство эквивалентности для всей области входов не завершено. Это не побайтовое восстановление исходной функции или EXE целиком.

[![Настоящее окно DIE с началом восстановленной нативной функции](docs/assets/vmp-3.8.4-virtualized-x64/07-recovered-native-function.jpg)](docs/assets/vmp-3.8.4-virtualized-x64/07-recovered-native-function.jpg)

Настоящие снимки статического дизассемблирования. Нажмите на изображение, чтобы открыть полный размер. В отчётах сохранены настройки, неудачные попытки, хеши и ограничения.

<details>
<summary>Внутреннее сравнение: до защиты → после защиты → после реконструкции</summary>

**До защиты: исходная точка входа**

![До защиты: исходная точка входа](docs/assets/vmp-3.8.4-x64/18-original-entrypoint.jpg)

**После защиты: точка входа защитного кода**

![После защиты: точка входа защитного кода](docs/assets/vmp-3.8.4-x64/19-protected-entrypoint.jpg)

**После реконструкции: исходная точка входа и исправленные импорты**

![После реконструкции: исходная точка входа и исправленные импорты](docs/assets/vmp-3.8.4-x64/20-unpacked-entrypoint.jpg)

</details>

<details>
<summary>Сравнение функции: исходное вычисление → вход в VM → восстановленные нативные инструкции</summary>

**До виртуализации: вычисление, отмеченное SDK**

![До виртуализации: вычисление, отмеченное SDK](docs/assets/vmp-3.8.4-virtualized-x64/06-original-function.jpg)

**После виртуализации: вход в виртуальную машину VMP**

![После виртуализации: вход в виртуальную машину VMP](docs/assets/vmp-3.8.4-virtualized-x64/05-virtualized-function.jpg)

**После восстановления: нативные инструкции из восстановленной семантики**

![После восстановления: нативные инструкции из восстановленной семантики](docs/assets/vmp-3.8.4-virtualized-x64/07-recovered-native-function.jpg)

</details>

<a id="quick-start"></a>

## Быстрый старт

Нужны **Python 3.11+** и доступ к этому закрытому репозиторию. Выполняйте команды из корня проекта.

```bash
git clone https://github.com/rancy777/reu.git
cd reu
python -m pip install -e .
re-skill route --input runtime/examples/triage.sample.json
```

Сервер MCP и запуск целевого файла не требуются. Включённые синтетические метаданные указывают динамическую загрузку DEX, поэтому выбираются соответствующие процессы анализа. Значение `Unknown` явно остаётся неизвестным.

<details>
<summary>Фрагмент фактического вывода</summary>

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

Для первичного анализа файла, который вы имеете право исследовать:

```bash
re-skill triage --file ./sample.exe --route
```

Фиксирует SHA-256, изучает поддерживаемые структуры файла и рекомендует процесс анализа, **не запуская цель**.

### Использование с агентом

Установите полный локальный Skill. Если каталог назначения уже существует, установка остановится.

```bash
python scripts/install_skill.py
```

```text
$reverse-engineering-unpacking
Проанализируй ./sample.exe; у меня есть право его исследовать.
Начни с анализа только для чтения: SHA-256, архитектура и признаки защиты.
Предложи следующий эксперимент, объясни, что он проверяет, и сохрани доказательства. Разделяй факты, гипотезы и неизвестное.
```

Каталог по умолчанию — `~/.agents/skills/reverse-engineering-unpacking`. Установите CLI отдельно. При работе в другом каталоге сообщите агенту абсолютный путь к исполняемому файлу.

### Повторная сборка нативного демо

Требуются **Windows x64, Python 3.11 x64, средства сборки C++ x64 Visual Studio и Windows SDK**. Из корня проекта:

```powershell
powershell -NoProfile -File .\examples\vmprotect-3.8.4-virtualized-x64\source\rebuild_demo.ps1
```

Загружает фиксированную версию llvmlite в новую среду, компилирует опубликованный восстановленный IR, собирает DLL и оболочку CLI. Выполняет **45 проверок поведения** переименованного EXE, размещённого отдельно. VMProtect и проприетарный SDK не нужны. Результаты: `runtime-artifacts/vmp-native-demo`; существующий каталог не перезаписывается. Это повторная сборка записанного результата, а не распаковка новой цели и не повтор сравнений с защищённой программой. [Исходники и проверка](examples/vmprotect-3.8.4-virtualized-x64/README.md).

## Зачем REU

- **Понятный следующий шаг.** Процессы по платформам с гипотезами, ожидаемыми наблюдениями и диагностикой неудач.
- **Подключение имеющихся инструментов.** Обнаружение реальных возможностей MCP и планирование вызовов по предоставленным схемам входных данных.
- **Проверяемые результаты.** Сохранение хешей, трасс, проверок и неудачных экспериментов.

## Область исследования

| Цель | Встроенный первичный анализ и маршрутизация | Продолжение |
| :--- | :--- | :--- |
| **Windows PE / .NET** | Заголовки, архитектура, признаки CLR, секции и энтропия | [Windows](workflows/windows-triage.md) · [.NET](workflows/windows-dotnet.md) |
| **Android APK / AAB** | Структура пакета, состав DEX/нативных библиотек и разделённые пакеты | [Android](workflows/android-triage.md) · [Splits / AAB](workflows/android-split-aab.md) |
| **DEX / ART** | Определение DEX, CDEX и VDEX; артефакты выполнения | [DEX](workflows/android-dex.md) · [ART](workflows/android-art-runtime.md) |
| **Native ELF / SO** | Идентификация и архитектура ELF; маршрутизация Android по переданному контексту | [ELF](workflows/native-elf-triage.md) · [Android native](workflows/android-native.md) |

Руководства охватывают распаковку, динамическую загрузку и сложную защиту. Для реконструкции нужны внешние инструменты, эксперименты с конкретной целью и проверка.

## Подключение инструментов

Если среда уже предоставляет инструменты MCP, используйте [нативный режим хоста](runtime/host-integration.md). Для отдельного моста:

```bash
python -m pip install -e '.[mcp]'
```

Создайте `providers.json` из [отключённого шаблона](runtime/config/providers.ready-to-install.json) и настройте установленный сервер по [Provider Setup](integrations/PROVIDER-SETUP.md).

```bash
re-skill doctor --config ./providers.json
re-skill discover --config ./providers.json --registry ./integrations/mcp-provider-registry.yaml --output discovery.json
```

`doctor` проверяет конфигурацию офлайн. `discover` запускает включённых и одобренных реестром провайдеров. Мост поддерживает stdio и Streamable HTTP с отдельными разрешениями на выполнение и изменения. IDA, Ghidra, x64dbg, WinDbg, JADX и Frida — кандидаты из [каталога](integrations/mcp-upstream-catalog.yaml); наличие в списке не подтверждает совместимость.

## Состояние проекта

**v1.5.0 · инженерная версия для оценки.** Записаны два эксперимента с нативными инструментами Windows; покрытие других образцов ещё предстоит расширить. Сторонние провайдеры MCP следуют своим инструкциям, повторная проверка не является условием выпуска. CI на Windows/Ubuntu проверяет Python 3.11–3.14, установку, целостность исходников и нативное демо. Успешные запуски предоставляют проверенные ZIP исходников, wheels и свидетельства демо в **Artifacts**.

```bash
python -m pip install -e '.[test]'
python -m pytest -q runtime/tests
re-skill regress --strict --file corpus/regression/automated.jsonl
```

Автоматический контроль содержит 16 исполняемых записей. Отдельный исследовательский набор сохраняет 5 PARTIAL / 3 MANUAL; строгий режим намеренно возвращает код 2. Все исходные 24 записи и утверждения сохранены.

## Частые вопросы

**Одна команда распаковывает любую программу VMP?** Нет. CLI выполняет первичный анализ, маршрутизацию и операции с доказательствами. Два проверенных примера не являются универсальным распаковщиком.

**Что воспроизводит нативное демо?** Компиляцию уже восстановленного LLVM IR и 45 функциональных проверок оболочки. Воспроизведение трассы, 100 008 проверок входов и 128 сравнений с защищённой программой имеют отдельные доказательства.

**Включены ли инструменты и защищённые EXE?** Включены скрипты, восстановленный IR, текстовые доказательства и настоящие снимки экрана. Нативные инструменты, проприетарные SDK, целевые бинарные файлы и дампы памяти исключены. Для нового защищённого образца нужны собственные VMProtect и SDK.

<a id="documentation"></a>

## Документация

[Начало работы](docs/getting-started.md) · [Архитектура](docs/architecture.md) · [Agent Skill](SKILL.md) · [Правила доказательств](references/evidence-policy.md) · [Проверка](docs/verification.md) · [Границы и оставшиеся задачи](docs/project-status.md)

Это локализованный обзор. Подробные отчёты и руководства сохраняют свой текущий язык. Правила сопровождения переводов: [Translations](docs/translations.md).

## Участие в проекте

Приветствуются воспроизводимые примеры, эксперименты провайдеров с указанием версий, регрессионные фикстуры и документированные неудачи. Укажите среду, ожидаемое наблюдение, фактический результат и доказательства. [Contributing](CONTRIBUTING.md).

## Ответственное использование и лицензия

Для собственного ПО, разрешённых проверок, изолированного анализа вредоносного ПО, CTF, совместимости, обучения и защитных исследований. Запускайте недоверенные образцы в изолированной среде. Среда выполнения не является песочницей. Внешние инструменты и провайдеры сохраняют собственные лицензии. [Security](SECURITY.md).

[MIT](LICENSE) · [English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md) · **Русский**
