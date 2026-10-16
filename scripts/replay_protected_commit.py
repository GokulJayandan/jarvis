"""Execute immutable protected Git bytes, separate from the recovery dispatcher."""
import hashlib
import json
import subprocess
import sys
from experiments.common import ROOT,write

def main():
    commit='a918583473afbb0bc70abe76f1266c39331bf97b'
    def blob(path):return subprocess.check_output(['git','show',commit+':'+path],cwd=ROOT)
    expected=json.loads(blob('results/frozen_source.json'))['files']
    target=ROOT/'.tools/recovery_protected_a918';checks={}
    paths=list(expected)+['kit.py','official_policy.py','LICENSE','DATA_LICENSE.md','raven/vendor/LICENSE.networkx']
    for path in paths:
        raw=blob(path);p=target/path;p.parent.mkdir(parents=True,exist_ok=True)
        if p.exists():assert p.read_bytes()==raw
        else:p.write_bytes(raw)
        checks[path]=hashlib.sha256(raw).hexdigest()
        if path in expected:assert checks[path]==expected[path]
    output=ROOT/'results/recovery/protected_commit_smoke.json'
    if output.exists():raise FileExistsError('Preserve existing protected-source smoke result')
    subprocess.run([sys.executable,'evaluate.py','--policy',str(target/'policy.py'),'--seeds','101','--output',str(output)],cwd=ROOT,check=True)
    observed=json.loads(output.read_text())['episodes'][0]
    original=json.loads((ROOT/'results/final.json').read_text())['episodes']
    reference=next(r for r in original if r['seed']==101 and r['variant']=='development')
    assert {k:v for k,v in observed.items() if k!='inference_seconds'}=={k:v for k,v in reference.items() if k!='inference_seconds'}
    write('results/recovery/protected_source_audit.json',{'commit':commit,'source_files':checks,'same_actions_and_outcomes':True,'episodes':1,
        'scope':'Exact immutable protected Git bytes, executed through the unchanged official subprocess evaluator. The full 18-episode configuration replay is separately retained.'})

if __name__=='__main__':main()
