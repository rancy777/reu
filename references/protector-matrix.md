# Protector / Packer Matrix

This is a hypothesis registry, not a list of guaranteed behaviors.

| Family | Platform | Version | Arch | Static clues | Runtime clues | Route | Scope | Confidence |
|---|---|---|---|---|---|---|---|---|
| UPX | Windows/PE | version-required | x86/x64 | signature/sections/import patterns | unpacking transition may be observable | triage → runtime → validation | sample/version | needs verification |
| VMProtect | Windows/PE | version-required | x86/x64 | protection-specific signatures/structure | generated/virtualized code may appear | runtime + static correlation | version/config/sample | needs verification |
| Themida | Windows/PE | version-required | x86/x64 | signatures/section/import anomalies | anti-analysis/runtime behavior may appear | runtime + static correlation | version/config/sample | needs verification |
| WinLicense | Windows/PE | version-required | x86/x64 | protector clues | runtime behavior | runtime + static | version/config/sample | needs verification |
| ASProtect | Windows/PE | version-required | x86/x64 | signature/loader clues | runtime loader behavior | runtime + reconstruction | version/sample | needs verification |
| Obsidium | Windows/PE | version-required | x86/x64 | signature/structure clues | runtime behavior | runtime + static | version/sample | needs verification |
| Enigma | Windows/PE | version-required | x86/x64 | signature/loader clues | runtime behavior | runtime + static | version/sample | needs verification |
| .NET protectors | Windows/.NET | version-required | Any supported | metadata/IL anomalies | JIT/runtime/loader behavior | .NET workflow | version/config/sample | needs verification |
| Android packer/protector | Android | product/version-required | ABI-required | package/DEX/SO anomalies | ClassLoader/runtime/native behavior | Android dynamic/native workflow | product/version/sample | needs verification |
| Custom loader | Any | sample-specific | arch-required | anomalous layout/imports | runtime materialization | custom workflow | sample-specific | needs verification |
| Virtualization protection | Windows/Native | version/config-required | arch-required | dispatcher/handler patterns | virtual machine execution | VM analysis workflow | version/config/sample | needs verification |

## Required fields for new entries

- family
- product/vendor if known
- version
- platform
- architecture
- sample scope
- static indicators
- runtime indicators
- counter-evidence
- analysis route
- sources
- evidence cards
- last verified
- confidence

## Classification labels

Use:
- Known behavior
- Version-specific behavior
- Sample-specific behavior
- Community-reported behavior
- Hypothesis

Never promote "community-reported" to "known behavior" without corroboration.
