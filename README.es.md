<div align="center">

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/assets/readme-hero-dark-mobile.svg">
  <source media="(max-width: 600px)" srcset="docs/assets/readme-hero-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/readme-hero-dark.svg">
  <img src="docs/assets/readme-hero.svg" alt="REU — Un método de ingeniería inversa para tu agente de IA: del análisis inicial a una reconstrucción verificada." width="100%">
</picture>

# Reverse Engineering & Unpacking

**Un método de ingeniería inversa para tu agente de IA: del análisis inicial a una reconstrucción verificada.**

Windows / .NET · Android / DEX · Native / ELF

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&labelColor=253044)](pyproject.toml)
[![Version 1.5.0](https://img.shields.io/badge/Version-1.5.0-5C6F91?style=flat-square&labelColor=253044)](CHANGELOG.md)
[![MIT License](https://img.shields.io/badge/License-MIT-4F8565?style=flat-square&labelColor=253044)](LICENSE)

[**Casos medidos**](#measured-cases) · [**Inicio rápido**](#quick-start) · [CI y descargas](https://github.com/rancy777/reu/actions/workflows/ci.yml?query=branch%3Amain) · [Documentación](#documentation)

[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · **Español** · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md) · [Русский](README.ru.md)

</div>

REU combina **Agent Skill + CLI de Python** para examinar archivos, planificar experimentos, conectar herramientas de análisis existentes y conservar resultados verificables. Tú aportas la muestra y el entorno; REU aporta el proceso de investigación, el enrutamiento y los registros.

<a id="measured-cases"></a>

## Casos medidos

**VMProtect 3.8.4 · Windows x64 · 2026-10-17**

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/assets/readme-cases-dark-mobile.svg">
  <source media="(max-width: 600px)" srcset="docs/assets/readme-cases-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/readme-cases-dark.svg">
  <img src="docs/assets/readme-cases.svg" alt="Casos medidos — VMProtect 3.8.4 x64" width="100%">
</picture>

- **[Empaquetado → reconstrucción ejecutable independiente](docs/cases/vmprotect-3.8.4-x64.md)** — El volcado en ejecución y la reparación de importaciones produjeron un EXE autónomo. **45/45 comprobaciones de comportamiento y 14/14 de estructura superadas**. [Código y validación](examples/vmprotect-3.8.4-x64).
- **[Virtualización de funciones → semántica nativa](docs/cases/vmprotect-3.8.4-virtualized-x64.md)** — Traza real del depurador → expresión recuperada → función nativa compilada. **53 instrucciones, 100 008 comprobaciones de entrada y 128 comparaciones diferenciales con el programa protegido**. [Código y validación](examples/vmprotect-3.8.4-virtualized-x64).

Son dos muestras propias con configuraciones de protección distintas. El caso de empaquetado utilizó un OEP conocido y reparaciones manuales de importaciones. La recuperación de la función abarca **una sola función pura**, con un arnés de pruebas CLI compilado por separado; la equivalencia SMT para todo el dominio sigue sin demostrarse. No es una restauración byte a byte de la función original ni del EXE completo.

[![Ventana real de DIE con el inicio de la función nativa recuperada](docs/assets/vmp-3.8.4-virtualized-x64/07-recovered-native-function.jpg)](docs/assets/vmp-3.8.4-virtualized-x64/07-recovered-native-function.jpg)

Capturas reales de desensamblado estático. Haz clic para ver la imagen a tamaño completo. Los informes conservan la configuración, los intentos fallidos, los hashes y los límites.

<details>
<summary>Comparación interna: antes → protegido → reconstruido</summary>

**Antes de proteger: punto de entrada original**

![Antes de proteger: punto de entrada original](docs/assets/vmp-3.8.4-x64/18-original-entrypoint.jpg)

**Protegido: punto de entrada del protector**

![Protegido: punto de entrada del protector](docs/assets/vmp-3.8.4-x64/19-protected-entrypoint.jpg)

**Reconstruido: punto de entrada original e importaciones reparadas**

![Reconstruido: punto de entrada original e importaciones reparadas](docs/assets/vmp-3.8.4-x64/20-unpacked-entrypoint.jpg)

</details>

<details>
<summary>Comparación de funciones: cálculo original → entrada a la VM → instrucciones nativas recuperadas</summary>

**Antes de virtualizar: cálculo marcado con el SDK**

![Antes de virtualizar: cálculo marcado con el SDK](docs/assets/vmp-3.8.4-virtualized-x64/06-original-function.jpg)

**Virtualizado: entrada a la máquina virtual de VMP**

![Virtualizado: entrada a la máquina virtual de VMP](docs/assets/vmp-3.8.4-virtualized-x64/05-virtualized-function.jpg)

**Recuperado: instrucciones nativas compiladas a partir de la semántica recuperada**

![Recuperado: instrucciones nativas compiladas a partir de la semántica recuperada](docs/assets/vmp-3.8.4-virtualized-x64/07-recovered-native-function.jpg)

</details>

<a id="quick-start"></a>

## Inicio rápido

Necesitas **Python 3.11+** y acceso a este repositorio privado. Ejecuta los comandos desde la raíz del proyecto.

```bash
git clone https://github.com/rancy777/reu.git
cd reu
python -m pip install -e .
re-skill route --input runtime/examples/triage.sample.json
```

No necesitas un servidor MCP ni ejecutar el archivo objetivo. Los metadatos sintéticos incluidos declaran carga dinámica de DEX, por lo que se seleccionan esos flujos. `Unknown` se mantiene explícitamente como desconocido.

<details>
<summary>Extracto de la salida real</summary>

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

Para analizar inicialmente un archivo que tengas autorización para examinar:

```bash
re-skill triage --file ./sample.exe --route
```

Registra SHA-256, inspecciona las estructuras compatibles y recomienda un flujo **sin ejecutar el archivo objetivo**.

### Usar con tu agente

Instala el Skill local completo. El instalador se detiene si el destino ya existe.

```bash
python scripts/install_skill.py
```

```text
$reverse-engineering-unpacking
Analiza ./sample.exe, que tengo autorización para examinar.
Empieza con un análisis de solo lectura: SHA-256, arquitectura e indicios de protección.
Propón el siguiente experimento, explica qué verifica y conserva las pruebas. Distingue hechos, hipótesis e incógnitas.
```

El destino predeterminado es `~/.agents/skills/reverse-engineering-unpacking`. Instala la CLI por separado y proporciona al agente la ruta absoluta del ejecutable si trabajas desde otro directorio.

### Recompilar la demostración nativa

Requiere **Windows x64, Python 3.11 x64, herramientas de compilación C++ x64 de Visual Studio y Windows SDK**. Desde la raíz del proyecto:

```powershell
powershell -NoProfile -File .\examples\vmprotect-3.8.4-virtualized-x64\source\rebuild_demo.ps1
```

Descarga una versión fijada de llvmlite en un entorno nuevo, compila el IR recuperado publicado y enlaza la DLL y el arnés CLI. Ejecuta **45 comprobaciones de comportamiento** sobre un EXE renombrado y aislado. No requiere VMProtect ni un SDK propietario. Guarda los resultados en `runtime-artifacts/vmp-native-demo` y rechaza un directorio ya existente. Recompila un resultado de recuperación registrado: no desempaqueta una muestra nueva ni repite las comparaciones con el programa protegido. [Código y validación](examples/vmprotect-3.8.4-virtualized-x64/README.md).

## Por qué REU

- **Saber qué investigar después.** Flujos por plataforma con hipótesis, observaciones esperadas y diagnóstico de fallos.
- **Usar las herramientas existentes.** Descubrir capacidades MCP reales y planificar llamadas según sus esquemas de entrada activos.
- **Poder examinar los resultados.** Conservar hashes, trazas, comprobaciones y experimentos fallidos.

## Alcance de la investigación

| Objetivo | Análisis inicial y enrutamiento integrados | Continuar con |
| :--- | :--- | :--- |
| **Windows PE / .NET** | Cabeceras, arquitectura, indicios de CLR, secciones y entropía | [Windows](workflows/windows-triage.md) · [.NET](workflows/windows-dotnet.md) |
| **Android APK / AAB** | Estructura del paquete, inventario DEX/nativo y rutas para paquetes divididos | [Android](workflows/android-triage.md) · [Splits / AAB](workflows/android-split-aab.md) |
| **DEX / ART** | Identificación de DEX, CDEX y VDEX; artefactos de ejecución | [DEX](workflows/android-dex.md) · [ART](workflows/android-art-runtime.md) |
| **Native ELF / SO** | Identidad y arquitectura ELF; ruta Android con el contexto aportado | [ELF](workflows/native-elf-triage.md) · [Android native](workflows/android-native.md) |

Las guías cubren desempaquetado, carga dinámica y protecciones complejas. La reconstrucción requiere herramientas externas, experimentos específicos y validación.

## Conectar herramientas

Si tu entorno ya expone herramientas MCP, utiliza el [modo nativo del host](runtime/host-integration.md). Para un puente independiente:

```bash
python -m pip install -e '.[mcp]'
```

Crea `providers.json` a partir de la [plantilla deshabilitada](runtime/config/providers.ready-to-install.json) y configura tu servidor instalado con [Provider Setup](integrations/PROVIDER-SETUP.md).

```bash
re-skill doctor --config ./providers.json
re-skill discover --config ./providers.json --registry ./integrations/mcp-provider-registry.yaml --output discovery.json
```

`doctor` comprueba la configuración sin conexión. `discover` inicia proveedores habilitados y aprobados por el registro. El puente admite stdio y Streamable HTTP, con autorizaciones separadas para ejecución y modificación. IDA, Ghidra, x64dbg, WinDbg, JADX y Frida son candidatos del [catálogo](integrations/mcp-upstream-catalog.yaml); figurar en él no certifica compatibilidad.

## Estado del proyecto

**v1.5.0 · versión candidata para evaluación técnica.** Se han registrado dos experimentos con herramientas nativas de Windows; ampliar las muestras sigue pendiente. Los proveedores MCP de terceros siguen sus instrucciones originales; repetir su validación no es un requisito de publicación. La CI de Windows/Ubuntu comprueba Python 3.11–3.14, instalación, integridad del código y demostración nativa. Las ejecuciones correctas ofrecen ZIP de código verificado, wheels y evidencias en **Artifacts**.

```bash
python -m pip install -e '.[test]'
python -m pytest -q runtime/tests
re-skill regress --strict --file corpus/regression/automated.jsonl
```

La puerta automática contiene 16 registros ejecutables. El conjunto de investigación independiente conserva 5 PARTIAL / 3 MANUAL; su modo estricto termina deliberadamente con código 2. Se mantienen los 24 registros originales y sus aserciones.

## Preguntas frecuentes

**¿Un comando desempaqueta cualquier programa VMP?** No. La CLI hace análisis inicial, enrutamiento y operaciones sobre evidencias. Estos dos casos no constituyen un desempaquetador universal.

**¿Qué reproduce la demostración?** La compilación de LLVM IR ya recuperado y 45 pruebas funcionales del arnés. La reproducción de trazas, las 100 008 entradas y las 128 comparaciones con el programa protegido tienen evidencias separadas.

**¿Incluye herramientas y ejecutables protegidos?** Incluye scripts, IR recuperado, evidencias de texto y capturas reales. Excluye herramientas nativas, SDK propietarios, binarios objetivo y volcados de memoria. Una muestra protegida nueva requiere tu instalación de VMProtect y su SDK.

<a id="documentation"></a>

## Documentación

[Primeros pasos](docs/getting-started.md) · [Arquitectura](docs/architecture.md) · [Agent Skill](SKILL.md) · [Política de evidencias](references/evidence-policy.md) · [Verificación](docs/verification.md) · [Alcance y trabajo pendiente](docs/project-status.md)

Esta página es un resumen localizado. Los informes y guías detallados conservan su idioma actual. Política de mantenimiento: [Translations](docs/translations.md).

## Contribuir

Aporta casos reproducibles, experimentos de proveedores con versiones identificadas, fixtures de regresión o fallos documentados. Incluye entorno, observación esperada, resultado real y evidencias. [Contributing](CONTRIBUTING.md).

## Uso responsable y licencia

Para software propio, evaluaciones autorizadas, análisis aislado de malware, CTF, interoperabilidad, educación e investigación defensiva. Ejecuta las muestras no confiables en un entorno aislado. El runtime no es un sandbox. Las herramientas y proveedores externos conservan sus propias licencias. [Security](SECURITY.md).

[MIT](LICENSE) · [English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · **Español** · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português (Brasil)](README.pt-BR.md) · [Русский](README.ru.md)
