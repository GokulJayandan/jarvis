"""Post-freeze compatibility, strict invocation and report verification."""
import json
import os
import sys
import time
from experiments.common import ROOT,write
from scripts.run_logged import run

def checked(label,cmd):
    code=run(label,cmd)
    if code!=0:raise RuntimeError(f'{label} failed: {code}')

def main():
    deadline=time.monotonic()+7200
    while True:
        path=ROOT/'results/execution/recovery_release_checks.json'
        if path.exists():
            if json.loads(path.read_text())['exit_code']!=0:raise RuntimeError('Release checks failed')
            break
        if time.monotonic()>deadline:raise TimeoutError('Release checks still incomplete')
        time.sleep(5)
    checked('recovery_python312',[str(ROOT/'.tools/python312/python.exe'),'-m','unittest','test_kit','test_runner','test_release',
        'tests.test_constraints','tests.test_portfolio','tests.test_protocol','tests.test_probabilities','tests.test_graphs','tests.test_temporal',
        'tests.test_matching.Matching.test_random_bruteforce_and_odd_cycles','tests.test_recovery','-v'])
    previous=os.environ.get('RAVEN_STRICT');os.environ['RAVEN_STRICT']='1'
    try:
        checked('recovery_strict_smoke',[sys.executable,'evaluate.py','--seeds','101','--output','results/recovery/strict_smoke.json'])
    finally:
        if previous is None:os.environ.pop('RAVEN_STRICT',None)
        else:os.environ['RAVEN_STRICT']=previous
    smoke=json.loads((ROOT/'results/recovery/strict_smoke.json').read_text())
    final=json.loads((ROOT/'results/recovery/final.json').read_text())
    assert smoke['summary']['eligible']
    actual=smoke['episodes'][0];expected=next(r for r in final['episodes'] if r['seed']==101 and r['variant']=='development')
    assert {k:v for k,v in actual.items() if k!='inference_seconds'}=={k:v for k,v in expected.items() if k!='inference_seconds'}
    write('results/recovery/strict_comparison.json',{'same_actions_and_outcomes':True,'episodes':1,'raven_strict':True})
    checked('recovery_report',[sys.executable,'-m','experiments.recovery_report'])
    checked('recovery_verify',[sys.executable,'-m','scripts.verify_recovery'])

if __name__=='__main__':main()
