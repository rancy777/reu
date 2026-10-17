"""Validate the recovered native function and a source-built CLI harness; no fixed success verdict."""
from pathlib import Path
import argparse,ctypes,hashlib,json,random,subprocess,tempfile,time
import pefile,capstone
from validate_behavior import expected,validate

def verify(dll,exe,protected,out):
 started=time.monotonic();checks={};out.parent.mkdir(parents=True,exist_ok=True)
 lib=ctypes.WinDLL(str(dll.resolve()));fn=lib.ReuRecoveredTransform;fn.argtypes=[ctypes.c_uint32];fn.restype=ctypes.c_uint32
 rng=random.Random(38420261017);values=[0,1,2,42,0x7fffffff,0x80000000,0xfffffffe,0xffffffff]+[rng.randrange(2**32) for _ in range(100000)]
 for x in values:
  if fn(x)!=expected(x):raise ValueError(f'Recovered native behavior mismatch at input {x}')
 checks['native_values']=len(values)
 for x in values[:128]:
  result=subprocess.run([str(protected.resolve()),'--value',str(x)],capture_output=True,timeout=10)
  if result.returncode or result.stdout.strip()!=str(fn(x)).encode():raise ValueError(f'Protected differential mismatch at {x}')
 checks['protected_differential_values']=128
 for path in (dll,exe):
  pe=pefile.PE(str(path));names=[s.Name.rstrip(b'\0').decode() for s in pe.sections]
  if names not in [['.text','.rdata'],['.text','.rdata','.pdata']]:raise ValueError('Unexpected recovered PE sections')
  if any(b'vmprotect' in d.dll.lower() for d in getattr(pe,'DIRECTORY_ENTRY_IMPORT',[])):raise ValueError('Recovered binary still imports the VMProtect SDK')
 pe=pefile.PE(str(dll));rva=next(e.address for e in pe.DIRECTORY_ENTRY_EXPORT.symbols if e.name==b'ReuRecoveredTransform')
 md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);instructions=[]
 for ins in md.disasm(pe.get_data(rva,1024),pe.OPTIONAL_HEADER.ImageBase+rva):
  instructions.append(ins)
  if ins.mnemonic=='ret':break
 if not instructions or instructions[-1].mnemonic!='ret':raise ValueError('No native return')
 if getattr(pe,'DIRECTORY_ENTRY_IMPORT',[]):raise ValueError('Recovered function DLL has external imports')
 if any(i.mnemonic.startswith(('call','j','loop')) for i in instructions):raise ValueError('Recovered function still has nontrivial external control flow')
 checks['native_instructions']=len(instructions);checks['dll_imports']=0;checks['vm_calls']=0
 (out.parent/'recovered-function-disassembly.txt').write_text('\n'.join(f'{i.address:x} {i.bytes.hex():24} {i.mnemonic} {i.op_str}' for i in instructions)+'\n')
 with tempfile.TemporaryDirectory(prefix='reu-vf-accept-') as directory:
  isolated=Path(directory)/'independent.exe';isolated.write_bytes(exe.read_bytes());behavior=validate(isolated)
  if behavior['behavior']!='PASS':raise ValueError('Isolated native harness failed')
 checks['isolated_exe_checks']=behavior['passed']
 identities={str(p.name):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in (dll,exe,protected)}
 report={'result':'PASS','checks':checks,'artifacts':identities,'seconds':time.monotonic()-started,'scope':'One known pure uint32 function recovered from a real protected trace and compiled to native code; harness CLI source rebuilt separately. Sampling, not exhaustive proof.'}
 out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return report
if __name__=='__main__':
 import sys;sys.stdout.reconfigure(encoding='utf-8');a=argparse.ArgumentParser();a.add_argument('--dll',required=True,type=Path);a.add_argument('--exe',required=True,type=Path);a.add_argument('--protected',required=True,type=Path);a.add_argument('--out',required=True,type=Path);v=a.parse_args()
 try:
  report=verify(v.dll,v.exe,v.protected,v.out);print(json.dumps(report,ensure_ascii=False,indent=2));print('函数语义重建验证成功（仅当前自有纯函数样本）')
 except Exception as e:
  v.out.write_text(json.dumps({'result':'FAIL','error':str(e)},ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('函数语义重建验证失败：'+str(e));raise SystemExit(1)
