"""Run only after training, validation selection, and baseline runs have finished."""
import json
import os
from pathlib import Path
import sys
from run_logged import run

root=Path(__file__).resolve().parents[1]
if not (root/'results'/'selection.json').exists():raise SystemExit('Selection must finish first')
for baseline in ('greedy','no_asks','random'):
    data=json.loads((root/'results'/f'{baseline}.json').read_text())
    assert data['summary']['eligible'] and len(data['episodes'])==18
entry='''"""Team Jarvis submission adapter; official baselines preserved separately."""
import argparse
from raven.protocol import decide, main

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--baseline',choices=['greedy','no_asks','random'],default='greedy')
    args=parser.parse_args()
    if args.baseline=='greedy':
        main()
    else:
        import json,sys
        from official_policy import decide as official_decide
        print(json.dumps(official_decide(json.load(sys.stdin),args.baseline),allow_nan=False))
'''
(root/'policy.py').write_text(entry,encoding='utf-8',newline='\n')
sys.path.insert(0,str(root))
from experiments.common import fingerprint,write
frozen=fingerprint()
write('results/frozen_source.json',frozen)
for label,cmd in [('final_tests',['python','-m','unittest','-v']),('final_data',['python','verify_data.py'])]:
    if run(label,cmd)!=0:raise SystemExit(label+' failed')
# Fail rather than conceal development exceptions behind the production fallback.
os.environ['RAVEN_STRICT']='1'
if run('final_official',['python','evaluate.py','--seeds','101,102,103','--variants','all','--output','results/final.json'])!=0:
    raise SystemExit('Final evaluation failed')
if fingerprint()!=frozen:raise SystemExit('Inference source changed during final evaluation')
