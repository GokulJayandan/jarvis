"""Public-observation replay diagnostics; never exposes latent fields to a policy."""
import collections
import json
import time
from kit import Simulator,generate
import evaluate
from official_policy import decide as official
from raven.protocol import decide
from raven.config import config
from raven.graphs import build
from raven.portfolio import utility,exhaustive
from raven.pruning import screen
from raven.constraints import missing_hard,recoverable
from experiments.common import ROOT,write

def main(output='results/recovery/observation_diagnostics.json'):
    if (ROOT/output).exists():raise FileExistsError('Choose a new --output path to preserve existing diagnostics')
    episodes=[];oracle=[]
    for mode in ('greedy','frozen'):
        for variant in evaluate.VARIANTS:
            sim=Simulator(generate(101,200,'evaluation',variant));days=[];predictions=[]
            cfg=config('soft')
            for day in range(60):
                state=sim.observe();confirmed,potential=build(state,cfg)
                request={'phase':'ask','state':state,'memory':{}}
                start=time.perf_counter();response=official(request) if mode=='greedy' else decide(request,'soft');ask_time=time.perf_counter()-start
                asks=response['asks'];selected=[(a['member_id'],a['field']) for a in asks]
                gain=utility(selected,confirmed,potential)-utility([],confirmed,potential)
                sim.resolve_asks(asks);state=sim.observe();after,_=build(state,cfg,False)
                request={'phase':'match','state':state,'memory':{}}
                start=time.perf_counter();response=official(request) if mode=='greedy' else decide(request,'soft');match_time=time.perf_counter()-start
                pairs=response['pairs'];weights={tuple(sorted((e.a,e.b))):e.weight for e in after}
                predictions.extend({'pair':sorted(p),'day':day,'p':weights[tuple(sorted(p))]} for p in pairs)
                used={i for p in pairs for i in p}
                unallocated_edges=sum(e.a not in used and e.b not in used for e in after)
                candidates=sorted((m['member_id'],'constraints') for m in state['members'] if m['available'] and missing_hard(m) and recoverable(m))
                if mode=='frozen' and day in (0,10,20,40) and 0<len(candidates)<=16:
                    c,p=build(state,cfg);kept=screen(candidates,p,12)
                    start=time.perf_counter();best,value,count,exact=exhaustive(candidates,12,c,p)
                    seconds=time.perf_counter()-start;chosen,limited,_,_=exhaustive(kept,12,c,p)
                    oracle.append(dict(variant=variant,day=day,seed=101,phase='post_ask',candidates=len(candidates),kept=len(kept),
                        best=best,chosen=chosen,regret=max(0,value-limited),exact=exact,portfolios=count,seconds=seconds))
                days.append(dict(day=day,hard_asks=sum(a['field']=='constraints' for a in asks),soft_asks=sum(a['field']!='constraints' for a in asks),
                    confirmed_before=len(confirmed),confirmed_after=len(after),potential_before=len(potential),surrogate_gain=gain,
                    introductions=len(pairs),available=sum(m['available'] for m in state['members']),unallocated_disjoint_edges=unallocated_edges,
                    inference_seconds=ask_time+match_time))
                sim.advance(pairs)
            for _ in range(40):sim.advance([])
            state=sim.observe();events=collections.defaultdict(list)
            for event in state['feedback']:events[event['introduction_id']].append(event)
            intros={(tuple(sorted((i['user_a'],i['user_b']))),i['assigned_day']):i for i in state['introductions']}
            for prediction in predictions:
                intro=intros[tuple(prediction['pair']),prediction['day']];es=events[intro['introduction_id']]
                dates=[e for e in es if e['event']=='date_happened' and e['value'] is True]
                second=[e for e in es if e['event']=='second_meeting_intention']
                prediction['msmi']=int(bool(dates) and dates[0]['occurred_day']-prediction['day']<=30 and len(second)==2 and all(e['value']=='yes' and e['occurred_day']-dates[0]['occurred_day']<=3 for e in second))
            expected=json.loads((ROOT/'results'/('greedy.json' if mode=='greedy' else 'final.json')).read_text())
            stored=next(r for r in expected['episodes'] if r['seed']==101 and r['variant']==variant)
            assert sum(p['msmi'] for p in predictions)==stored['mutual_second_meeting_intention']
            assert len(predictions)==stored['assignments']
            episodes.append(dict(policy=mode,variant=variant,seed=101,days=days,predictions=predictions,
                feedback_delays=[e['observed_day']-e['occurred_day'] for e in state['feedback'] if e['occurred_day'] is not None],
                feedback_without_occurrence_day=sum(e['occurred_day'] is None for e in state['feedback']),metrics=sim.metrics()))
            write(output,{'episodes':episodes,'production_state_oracles':oracle,
                'scope':'One diagnostic seed across six families, public observations only; oracle restricted to encountered states with at most 16 useful candidates. Not used for selection.'})
            print(mode,variant,len(predictions),flush=True)

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='results/recovery/observation_diagnostics.json')
    main(parser.parse_args().output)
