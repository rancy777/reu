"""Check the reconstruction against the saved dump, independently of execution."""
import hashlib
import json
from pathlib import Path
import struct
import capstone
import pefile

root = Path(__file__).resolve().parents[1]
candidate = root / 'unpacked' / 'reu-challenge.unpacked.exe'
dump = pefile.PE(str(root / 'unpacked' / 'reu-challenge.dump.exe'))
pe = pefile.PE(str(candidate))
record = json.loads((root / 'evidence' / 'reconstruction.json').read_text(encoding='utf-8'))
checks = {}
checks['x64_pe'] = pe.FILE_HEADER.Machine == 0x8664 and pe.OPTIONAL_HEADER.Magic == 0x20B
checks['expected_sections_only'] = [s.Name.rstrip(b'\0').decode() for s in pe.sections] == ['.text', '.rdata', '.pdata', '.idata']
checks['entrypoint_in_restored_text'] = pe.OPTIONAL_HEADER.AddressOfEntryPoint == 0x11F0
checks['compact_file_without_protector_regions'] = len(candidate.read_bytes()) == 5120 and pe.OPTIONAL_HEADER.SizeOfImage == 0x5000
checks['no_tls_loader_callbacks'] = pe.OPTIONAL_HEADER.DATA_DIRECTORY[9].VirtualAddress == 0
checks['no_relocation_reference_to_removed_regions'] = pe.OPTIONAL_HEADER.DATA_DIRECTORY[5].VirtualAddress == 0
checks['nx_preserved'] = bool(pe.OPTIONAL_HEADER.DllCharacteristics & 0x100)
checks['checksum_valid'] = pe.verify_checksum()
iat = {e.address - pe.OPTIONAL_HEADER.ImageBase for lib in pe.DIRECTORY_ENTRY_IMPORT for e in lib.imports}
iat_directory = pe.OPTIONAL_HEADER.DATA_DIRECTORY[12]
checks['iat_directory_covers_all_import_slots'] = all(
    iat_directory.VirtualAddress <= address and address + 8 <= iat_directory.VirtualAddress + iat_directory.Size
    for address in iat)
imports = {lib.dll.decode(): [e.name.decode() for e in lib.imports] for lib in pe.DIRECTORY_ENTRY_IMPORT}
checks['five_expected_os_imports'] = imports == {
    'KERNEL32.dll': ['ExitProcess', 'GetCommandLineA', 'GetStdHandle', 'WriteFile'],
    'USER32.dll': ['MessageBoxW'],
}
restored_text = bytearray(pe.get_data(0x1000, 0x447))
dump_text = bytearray(dump.get_data(0x1000, 0x447))
patches_match = True
for patch in record['import_call_patches']:
    rva = int(patch['rva'], 16)
    patches_match = patches_match and restored_text[rva-0x1000:rva-0x1000+6] == bytes.fromhex(patch['after'])
    restored_text[rva-0x1000:rva-0x1000+6] = bytes.fromhex(patch['before'])
checks['code_matches_runtime_dump_except_nine_import_repairs'] = patches_match and restored_text == dump_text
checks['read_only_data_preserved_from_dump'] = pe.get_data(0x2000, 0x4D4) == dump.get_data(0x2000, 0x4D4)
checks['unwind_data_preserved_from_dump'] = pe.get_data(0x3000, 0x48) == dump.get_data(0x3000, 0x48)

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
unresolved_calls = []
repaired_calls = []
for ins in md.disasm(pe.get_data(0x1000, 0x447), 0x1000):
    if ins.mnemonic != 'call':
        continue
    operand = ins.operands[0]
    if operand.type == capstone.x86.X86_OP_IMM:
        if not 0x1000 <= operand.imm < 0x1447:
            unresolved_calls.append(hex(ins.address))
    elif operand.type == capstone.x86.X86_OP_MEM and operand.mem.base == capstone.x86.X86_REG_RIP:
        target = ins.address + ins.size + operand.mem.disp
        if target not in iat:
            unresolved_calls.append(hex(ins.address))
        else:
            repaired_calls.append(hex(ins.address))
    else:
        unresolved_calls.append(hex(ins.address))
checks['all_external_calls_use_rebuilt_iat'] = not unresolved_calls and len(repaired_calls) == 9
report = {'file': str(candidate), 'sha256': hashlib.sha256(candidate.read_bytes()).hexdigest(),
          'structure': 'PASS' if all(checks.values()) else 'FAIL', 'checks': checks,
          'imports': imports, 'repaired_call_rvas': repaired_calls,
          'unresolved_calls': unresolved_calls, 'scope': 'This exact loader-only benchmark. Does not establish devirtualization.'}
(root / 'evidence' / 'unpacked-structure.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
print(json.dumps(report))
raise SystemExit(not all(checks.values()))
