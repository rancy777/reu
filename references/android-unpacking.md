# Android Unpacking

## Workflow
Triage → package/module mapping → DEX/SO inventory → static analysis → runtime loading observation → capture desired representation → validate.

## DEX
Distinguish:
- DEX on disk
- dynamically loaded DEX
- decrypted DEX in memory
- optimized/runtime artifacts

Observe ClassLoader relationships and loading events where authorized.

## Native
Map:
APK lib/<abi>/*.so
→ loaded module
→ JNI registration/exports
→ native call graph
→ runtime-generated/decrypted code if any.

## Complex protection
Do not assume one "main DEX" or one loader. Build a module graph and a runtime timeline.
