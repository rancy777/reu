# PE Fundamentals

## Required model
DOS header → NT headers → file header → optional header → section table → data directories → section/file mappings → loader/runtime structures.

Track:
PE32 vs PE32+, machine, ImageBase, SizeOfImage, SizeOfHeaders, SectionAlignment, FileAlignment, AddressOfEntryPoint, section characteristics, imports/exports, relocations, TLS, resources, exception directory, load config, debug directory, overlay, security directory.

Microsoft's PE format documentation is canonical for structure. Data-directory count must be respected, and directory RVAs must not be assumed to start a section or use conventional section names.

## Address conversion
Keep explicit:
RVA, VA, file offset/raw pointer, mapped address.
Never silently convert between them.

## Runtime model
An executable can be:
- original file
- loader-mapped image
- partially unpacked
- fully unpacked
- self-modifying/generated
- captured
- repaired

A valid reconstructed PE must be tested as a program, not judged by appearance alone.
