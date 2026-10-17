from pathlib import Path
import argparse,json,hashlib
from llvmlite import binding as llvm

def compile_ir(source,out):
 out.mkdir(parents=True,exist_ok=True);llvm.initialize_native_target();llvm.initialize_native_asmprinter()
 machine=llvm.Target.from_default_triple().create_target_machine(opt=3,codemodel="default",jit=False)
 text=source.read_text().replace('@__triton','@ReuRecoveredTransform')
 mod=llvm.parse_assembly(text);mod.verify();mod.triple=llvm.get_default_triple();mod.data_layout=str(machine.target_data)
 pb=llvm.create_pass_builder(machine,llvm.create_pipeline_tuning_options(speed_level=3));pb.getModulePassManager().run(mod,pb);mod.verify()
 (out/'recovered.optimized.ll').write_text(str(mod),encoding='utf-8');(out/'recovered.asm').write_text(machine.emit_assembly(mod),encoding='utf-8');(out/'recovered.obj').write_bytes(machine.emit_object(mod))
 report={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'llvm_version':list(llvm.llvm_version_info),'target':mod.triple,'function':'ReuRecoveredTransform','input':'Recovered LLVM IR only; no C++ algorithm or original object is read'}
 (out/'compile-recovered.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('source',type=Path);a.add_argument('out',type=Path);v=a.parse_args();compile_ir(v.source,v.out)
