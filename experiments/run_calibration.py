"""Held-out diagnostics; never used to tune frozen model or policy."""
import collections
import json
import math
import sys
from raven.probabilities import predict_features,assets,clip
from experiments.common import ROOT,write
from experiments.train import collect

def metrics(rows):
    if not rows:return {'n':0}
    bins=[]
    # Equal-frequency bins show low-probability MSMI behavior instead of one 0–0.1 bin.
    ordered=sorted(rows,key=lambda r:r['p']);step=max(1,math.ceil(len(rows)/10))
    partitions=[];current=[]
    for i,row in enumerate(ordered):
        current.append(row)
        # Do not split equal predictions into arbitrary chronological bins.
        if len(current)>=step and (i+1==len(ordered) or ordered[i+1]['p']!=row['p']):
            partitions.append(current);current=[]
    if current:partitions.append(current)
    for subset in partitions:
        n=len(subset);rate=sum(r['y'] for r in subset)/n
        # Wilson interval for observed bin frequency (dependence not accounted for).
        z=1.96;den=1+z*z/n;center=(rate+z*z/(2*n))/den
        half=z*math.sqrt(rate*(1-rate)/n+z*z/(4*n*n))/den
        bins.append(dict(n=n,p=sum(r['p'] for r in subset)/n,observed=rate,ci95=[center-half,center+half]))
    n=len(rows)
    return dict(n=n,positives=sum(r['y'] for r in rows),brier=sum((r['p']-r['y'])**2 for r in rows)/n,
                log_loss=-sum(r['y']*math.log(clip(r['p']))+(1-r['y'])*math.log(1-clip(r['p'])) for r in rows)/n,
                ece=sum(b['n']*abs(b['p']-b['observed']) for b in bins)/n,bins=bins)

if __name__=='__main__':
    from evaluate import VARIANTS
    from kit import Simulator,generate,HARD
    data=json.loads((ROOT/'results/calibration/heldout_observations.json').read_text()) if '--reuse' in sys.argv else collect([13001,13002],VARIANTS,True)
    # Probe the exact observed-status disclosure contract, including refused fields
    # excluded by normal policy question selection. Never use these for matching.
    disclosure_trials=[]
    for seed in (13001,13002):
        sim=Simulator(generate(seed,40,'disclosure_probe','cold_start'))
        ids=[m['member_id'] for m in sim.observe()['members']][:12]
        for start in range(0,len(ids),4):
            before={m['member_id']:m for m in sim.observe()['members']}
            chosen=ids[start:start+4]
            sim.resolve_asks([{'member_id':i,'field':'constraints'} for i in chosen])
            after={m['member_id']:m for m in sim.observe()['members']}
            for i in chosen:
                for k in HARD:
                    status=before[i]['field_status'][k]
                    disclosure_trials.append({'status':status,'p':float(status!='declined'),
                        'y':int(after[i]['fields'][k] is not None)})
            sim.advance([])
    write('results/calibration/heldout_observations.json',data)
    results=[]
    for target in ('directional','joint','date','msmi'):
        for model,calibrated in [('prior',False),('logistic',False),('logistic',True)]:
            groups=collections.defaultdict(list)
            for r in data['rows']:
                p=predict_features(r['x'],target,model,calibrated)
                if target!='directional':p=(p+predict_features(r['xr'],target,model,calibrated))/2
                row={'p':p,'y':r[target]};groups['all'].append(row);groups[r['stratum']].append(row)
            for group,rows in groups.items():results.append(dict(target=target,model=model,calibrated=calibrated,stratum=group,**metrics(rows)))
    gate=assets()['gate'];grows=[{'p':gate['cells'].get(r['key'],gate['prior']),'y':r['y']} for r in data['gates']]
    write('results/calibration/metrics.json',dict(seeds=[13001,13002],targets=results,gate=metrics(grows),
          disclosure=metrics(disclosure_trials),disclosure_strata={s:metrics([r for r in disclosure_trials if r['status']==s]) for s in ('observed','not_asked','declined')},
          limitations='Selected-introduction calibration under historical baseline mix, not all-pair calibration. Wilson bin intervals ignore within-world dependence. No preference failure label for missing feedback.'))
    write('results/calibration/disclosure_trials.json',disclosure_trials)
