# Native SO / ELF Analysis

## Static
ELF class/endianness/machine, program headers, sections, dynamic table, relocations, symbols, GNU properties, unwind information, JNI exports/registration, strings, suspicious encrypted blobs.

## Runtime
Track load base, modules, memory permissions, JNI_OnLoad, dynamically registered natives, thread creation, executable anonymous mappings, self-modifying/decrypted regions.

## Cross-layer
Map:
Java/Kotlin call
→ JNI boundary
→ native symbol/registered method
→ native function
→ data/crypto/loader
→ return path.

Use Unidbg only when controlled emulation can answer the question without requiring the full Android environment.
