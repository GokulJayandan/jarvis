"""Declared, paired recovery search. Never overwrites original experiments."""
import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import evaluate
from experiments.common import ROOT, write, paired_ci, fingerprint
from experiments.run_suite import run

PLAN=json.loads((ROOT/'configs/recovery.json').read_text())
BASE=Path('results/recovery')

def job(args):
    stage,name,seeds,output_root=args
    path=Path(output_root)/stage/(name+'.json')
    if (ROOT/path).exists():
        raise FileExistsError('Preserve completed evidence: '+str(path))
    return run('joint',seeds,evaluate.VARIANTS,str(path),overrides=PLAN['variants'][name])

def batch(stage,names,seeds):
    with ProcessPoolExecutor(max_workers=2) as pool:
        list(pool.map(job,[(stage,n,seeds,str(BASE)) for n in names]))

def load(stage,name):
    return json.loads((ROOT/BASE/stage/(name+'.json')).read_text())

def score(data):
    return sum(r['msmi_per_100_arrived_members'] for r in data['episodes'])/len(data['episodes'])

def search():
    write(str(BASE/'registered_plan.json'),dict(PLAN,source=fingerprint()))
    names=[n for n in PLAN['variants'] if n not in PLAN['aliases_not_separate_experiments']]
    batch('screen',names,PLAN['screening_validation_seeds'])
    ranked=sorted((n for n in names if n not in ('V0_frozen','V1_greedy')),key=lambda n:(-score(load('screen',n)),n))
    shortlist=['V0_frozen','V1_greedy']+ranked[:2]
    write(str(BASE/'shortlist.json'),{'names':shortlist,'screen_scores':{n:score(load('screen',n)) for n in names}})
    batch('confirm',shortlist,PLAN['confirmation_validation_seeds'])
    baseline=load('confirm','V1_greedy')
    comparisons={n:paired_ci(load('confirm',n)['episodes'],baseline['episodes']) for n in shortlist if n!='V1_greedy'}
    qualifying=[n for n,c in comparisons.items() if c['ci95'][0]>0]
    selected=min(qualifying,key=lambda n:(-score(load('confirm',n)),n)) if qualifying else 'V1_greedy'
    write(str(BASE/'selection.json'),dict(selected=selected,overrides=PLAN['variants'][selected],comparisons=comparisons,
          scores={n:score(load('confirm',n)) for n in shortlist},source=fingerprint(),
          reason='Predeclared conservative validation rule; intervals are descriptive with five seed clusters and not multiplicity-adjusted.'))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['search','reproduce','fresh'])
    parser.add_argument('--output-root',default='results/recovery',help='Use a new relative directory to preserve earlier experiments')
    args=parser.parse_args();BASE=Path(args.output_root)
    if BASE.is_absolute() or '..' in BASE.parts:raise ValueError('Use a workspace-relative result directory')
    if args.stage=='search':search()
    elif args.stage=='reproduce':
        if (ROOT/BASE/'reproduced_frozen.json').exists():raise FileExistsError('Choose a new --output-root to preserve the previous replay')
        run('soft',[101,102,103],evaluate.VARIANTS,str(BASE/'reproduced_frozen.json'),subprocess_mode=True)
    else:
        selection=json.loads((ROOT/BASE/'selection.json').read_text())
        batch('fresh',sorted({selection['selected'],'V0_frozen','V1_greedy'}),PLAN['untouched_reporting_seeds'])
