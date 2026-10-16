"""Predeclared validation suite. All candidate decisions precede held-out testing."""
import json
from concurrent.futures import ProcessPoolExecutor
from evaluate import VARIANTS
from raven.config import config
from experiments.common import ROOT,write
from experiments.run_suite import run

NAMES=['official_greedy','joint','future','future_high','prior','uncalibrated','greedy_match','singleton','endpoint','random_questions','soft','unpruned','waiting']

def evaluate_candidate(name,seeds):
    path='results/ablations/'+name+'.json'
    if (ROOT/path).exists():
        result=json.loads((ROOT/path).read_text())
        if len(result['episodes'])==len(seeds)*len(VARIANTS) and result['summary']['eligible']:
            return name,result['summary']
    return name,run(name,seeds,VARIANTS,path)['summary']

if __name__=='__main__':
    registry=json.loads((ROOT/'configs'/'seeds.json').read_text())
    seeds=registry['validation'][:2]
    results={}
    with ProcessPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(evaluate_candidate,name,seeds) for name in NAMES]
        for future in futures:
            name,summary=future.result();results[name]=summary
    # Few downstream outcomes make fine-grained selection noisy. Pick primary,
    # then official tie-breaks except runtime (different algorithms measured here).
    winner=max(results,key=lambda name:(results[name]['primary_score'],results[name]['overall']['coverage'],
               results[name]['overall']['mutual_acceptances_per_100'],-results[name]['overall']['ask_cost']))
    chosen=config(winner) if not winner.startswith('official_') else {'official_baseline':winner.removeprefix('official_')}
    write('raven/assets/final_config.json',chosen)
    write('results/selection.json',dict(winner=winner,seeds=seeds,all_candidates=results,
          warning='Exploratory selection among 13 candidates and two seed clusters; final and fresh test populations remain held out.'))
    print('FROZEN: '+winner,flush=True)
