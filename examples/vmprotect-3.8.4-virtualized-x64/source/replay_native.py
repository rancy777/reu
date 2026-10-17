"""Replay a real x64dbg pure-function trace with Triton; fail on symbolic-state disagreement."""
from pathlib import Path
import argparse,hashlib,json,time,pefile
from triton import TritonContext,ARCH,MODE,Instruction,MemoryAccess,EXCEPTION
REGS=['rax','rbx','rcx','rdx','rsi','rdi','rbp','rsp','r8','r9','r10','r11','r12','r13','r14','r15','eflags']
def replay(trace,out,stop,binary):
 out.mkdir(parents=True,exist_ok=True);ctx=TritonContext(ARCH.X86_64)
 for mode in (MODE.AST_OPTIMIZATIONS,MODE.CONSTANT_FOLDING):ctx.setMode(mode,True)
 base=int(trace.read_text(encoding='utf-8-sig').split('|')[0],16)-0x1150
 pe=pefile.PE(str(binary));pe.relocate_image(base);ctx.setConcreteMemoryAreaValue(base,bytes(pe.get_memory_mapped_image()))
 start=time.monotonic();count=0;syncs=0;input_value=None
 def sync_mem(addr,data):
  nonlocal syncs
  if not data or '?' in data or data.startswith('['):return
  data=bytes.fromhex(data)
  for index,value in enumerate(data):
   cell=MemoryAccess(addr+index,1)
   if ctx.getConcreteMemoryValue(cell)!=value:
    if ctx.isMemorySymbolized(cell):raise RuntimeError(f'Symbolic memory mismatch at {addr+index:x}, step {count}')
    ctx.setConcreteMemoryValue(cell,value);syncs+=1
 try:
  for line in trace.read_text(encoding='utf-8-sig').splitlines():
   cols=line.strip().split('|')
   if len(cols)!=20:raise RuntimeError(f'Unexpected trace columns {len(cols)}')
   ip=int(cols[0],16);regs={n:int(v,16) for n,v in zip(REGS,cols[2:19])}
   for name,value in regs.items():
    reg=getattr(ctx.registers,name)
    if name=='eflags':value &= ~0x100 # Windows single-step trap bit is debugger state.
    if ctx.getConcreteRegisterValue(reg)!=value:
     if ctx.isRegisterSymbolized(reg):raise RuntimeError(f'Symbolic register mismatch {name} at {ip:x}, step {count}')
     ctx.setConcreteRegisterValue(reg,value);syncs+=1
   sync_mem(regs['rsp'],cols[19])
   if input_value is None:
    input_value=regs['rcx'] & 0xffffffff
    var=ctx.symbolizeRegister(ctx.registers.ecx,'x');ctx.setConcreteVariableValue(var,input_value)
   expected_ip=ctx.getConcreteRegisterValue(ctx.registers.rip)
   if count and expected_ip!=ip:raise RuntimeError(f'Control-flow mismatch at trace step {count}')
   if ip==stop:break
   ins=Instruction(ip,bytes.fromhex(cols[1])[:16]);status=ctx.processing(ins)
   if status!=EXCEPTION.NO_FAULT:raise RuntimeError(f'Unsupported semantics: {ins}')
   count+=1
   if count%10000==0:print(f'replayed={count}, seconds={time.monotonic()-start:.1f}',flush=True)
  else:raise RuntimeError('Trace did not reach the recorded caller return address')
  ast=ctx.getRegisterAst(ctx.registers.eax)
  if not ast.isSymbolized():raise RuntimeError('Output lost its symbolic input')
  expr=ctx.newSymbolicExpression(ast,'recovered-return')
  (out/'recovered.ll').write_text(ctx.liftToLLVM(expr),encoding='utf-8')
  (out/'recovered.smt2').write_text(ctx.liftToSMT(expr),encoding='utf-8')
  report={'status':'EXPRESSION_RECOVERED_PENDING_VALIDATION','instructions':count,'input':input_value,'output':ctx.getConcreteRegisterValue(ctx.registers.eax),'concrete_syncs':syncs,'seconds':time.monotonic()-start,'trace_sha256':hashlib.sha256(trace.read_bytes()).hexdigest(),'protected_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'path_constraints':len(ctx.getPathConstraints())}
 except Exception as e:report={'status':'FAIL','error':str(e),'instructions':count,'seconds':time.monotonic()-start}
 (out/'replay.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True);return report
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('trace',type=Path);a.add_argument('out',type=Path);a.add_argument('--binary',required=True,type=Path);a.add_argument('--stop',required=True,type=lambda x:int(x,16));v=a.parse_args();r=replay(v.trace,v.out,v.stop,v.binary);raise SystemExit(r['status']=='FAIL')
