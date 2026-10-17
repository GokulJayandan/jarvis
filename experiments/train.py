"""Fit exclusively to pre-action observable features and matured public outcomes."""
import collections
import itertools
import json
import math
from pathlib import Path
import random
import time
import numpy as np
from kit import Simulator,generate,baseline_asks,baseline_match,eligibility,HARD
from official_policy import decide
from raven.probabilities import features,gate_key,stratum,sigmoid
from experiments.common import ROOT,write

def collect(seeds, variants, gate_data=False):
    rows=[];gates=[];arrivals=collections.Counter();zones=collections.Counter();disclosures=[]
    for seed in seeds:
        for variant in variants:
            sim=Simulator(generate(seed,200,'experiment',variant))
            decisions=[]
            for day in range(60):
                before=sim.observe();asks=baseline_asks(before)
                asked={a['member_id'] for a in asks}
                candidates=[]
                if gate_data:
                    active=[m for m in before['members'] if m['available']]
                    for a,b in itertools.combinations(active,2):
                        required={m['member_id'] for m in (a,b) if any(m['fields'][k] is None for k in HARD)}
                        if required and required<=asked and eligibility(a,b)['status']=='needs_clarification':
                            candidates.append((a,b,gate_key(a,b)))
                sim.resolve_asks(asks);state=sim.observe();members={m['member_id']:m for m in state['members']}
                for a,b,k in candidates:
                    gates.append({'key':k,'y':int(eligibility(members[a['member_id']],members[b['member_id']])['status']=='feasible'), 'seed':seed,'variant':variant})
                for ask in asks:
                    prior=next(m for m in before['members'] if m['member_id']==ask['member_id'])
                    for k in HARD:
                        if prior['fields'][k] is None:
                            disclosures.append({'status':prior['field_status'][k],'p':float(prior['field_status'][k]!='declined'),
                                                'y':int(members[ask['member_id']]['fields'][k] is not None)})
                mode='random' if seed%2 else 'greedy'
                pairs=decide({'phase':'match','state':state,'memory':None},mode)['pairs']
                for a,b in pairs:
                    decisions.append({'a':a,'b':b,'day':day,'x':features(members[a],members[b],day),
                                      'xr':features(members[b],members[a],day),'stratum':stratum(members[a],members[b])})
                sim.advance(pairs)
            for _ in range(40):sim.advance([])
            observed=sim.observe()
            arrivals.update(m['arrived_day'] for m in observed['members']);zones.update(m['zone'] for m in observed['members'])
            by_intro=collections.defaultdict(list)
            for e in observed['feedback']:by_intro[e['introduction_id']].append(e)
            intro={(tuple(sorted((i['user_a'],i['user_b']))),i['assigned_day']):i for i in observed['introductions']}
            for d in decisions:
                i=intro[tuple(sorted((d['a'],d['b']))),d['day']];es=by_intro[i['introduction_id']]
                rs={e['member_id']:e for e in es if e['event']=='introduction_response'}
                ds=[e for e in es if e['event']=='date_happened' and e['value'] is True]
                ss=[e for e in es if e['event']=='second_meeting_intention']
                yes=lambda ident:int(rs.get(ident,{}).get('value')=='yes')
                qualifies=bool(ds) and ds[0]['occurred_day']-d['day']<=30 and len(ss)==2 and all(e['value']=='yes' and e['occurred_day']-ds[0]['occurred_day']<=3 for e in ss)
                rows.append(dict(d,seed=seed,variant=variant,joint=yes(d['a'])*yes(d['b']),date=int(bool(ds)),
                                 msmi=int(qualifies),directional=yes(d['a']),directional_reverse=yes(d['b']),matured_day=100))
            print(json.dumps({'collection_seed':seed,'variant':variant,'rows':len(rows)}),flush=True)
    return dict(rows=rows,gates=gates,disclosure=disclosures,arrivals=dict(arrivals),zones=dict(zones),episodes=len(seeds)*len(variants))

def logistic_fit(x,y,ridge=20):
    x=np.asarray(x,dtype=float);y=np.asarray(y,dtype=float)
    if x.size==0 and x.ndim==1:
        # Empty research datasets use the same feature schema and a neutral prior.
        x=np.empty((0,len(features({'age':21},{'age':21}))))
    weights=np.zeros(x.shape[1]);prior=(y.sum()+.5)/(len(y)+1)
    weights[0]=math.log(prior/(1-prior))
    penalty=np.eye(len(weights))*ridge;penalty[0,0]=.1
    for _ in range(30):
        p=1/(1+np.exp(-np.clip(x@weights,-30,30)))
        gradient=x.T@(p-y)+penalty@weights
        hessian=(x.T*(p*(1-p)))@x+penalty
        delta=np.linalg.solve(hessian,gradient)
        weights-=np.clip(delta,-1,1)
        if np.max(abs(delta))<1e-7:break
    return weights.tolist(),float(prior)

def fit(train,val):
    targets={}
    for target in ('directional','joint','date','msmi'):
        x=[];y=[]
        for r in train['rows']:
            x.extend([r['x'],r['xr']]);y.extend([r[target],r['directional_reverse'] if target=='directional' else r[target]])
        weights,prior=logistic_fit(x,y)
        # Validation-only intercept calibration, regularized to zero for sparse events.
        z=np.asarray([sum(a*b for a,b in zip(r['x'],weights)) for r in val['rows']])
        labels=np.asarray([r[target] for r in val['rows']]);offset=0.
        for _ in range(15):
            p=1/(1+np.exp(-np.clip(z+offset,-30,30)))
            offset-=float((sum(p-labels)+20*offset)/(sum(p*(1-p))+20))
        targets[target]=dict(weights=weights,prior=prior,offset=offset,scale=1.,n_training=len(y),n_validation=len(labels))
    counts=collections.defaultdict(lambda:[0,0])
    for r in train['gates']:counts[r['key']][0]+=r['y'];counts[r['key']][1]+=1
    n=len(train['gates']);rate=(sum(r['y'] for r in train['gates'])+1)/(n+2)
    gate={'prior':rate,'cells':{k:(s+20*rate)/(n+20) for k,(s,n) in counts.items()},'counts':dict(counts),'n':n}
    total=sum(train['zones'].values())
    future=dict(arrivals={str(k):v/train['episodes'] for k,v in train['arrivals'].items()},
                zone_frequency={k:v/total for k,v in train['zones'].items()},rare_zone_frequency=1/12,
                reciprocal_rate=rate,outcome_prior=targets['msmi']['prior'])
    return dict(version=1,targets=targets,gate=gate,future=future,
                provenance='Pre-action observable public rollouts only; all labels matured at day 100; no hidden-state features.')

if __name__=='__main__':
    from evaluate import VARIANTS
    registry=json.loads((ROOT/'configs'/'seeds.json').read_text())
    train=collect(registry['training'],VARIANTS,True)
    write('results/training/observations.json',train)
    val=collect(registry['validation'],VARIANTS,True)
    write('results/training/validation_observations.json',val)
    model=fit(train,val);write('raven/assets/model.json',model)
    print(json.dumps({'trained':True,'train_rows':len(train['rows']),'validation_rows':len(val['rows'])}),flush=True)
