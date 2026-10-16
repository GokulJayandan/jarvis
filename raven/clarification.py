"""P1–P6 planners share legal questions and differ in allocation of information."""
import random
from .constraints import missing_hard,recoverable,SOFT
from .graphs import build
from .portfolio import utility,exhaustive
from .pruning import screen
from .future_value import future_value

def questions(state,cfg):
    budget=max(0,state.get('ask_budget_remaining',0))
    if budget<1: return []
    members={m['member_id']:m for m in state.get('members',[]) if m.get('available')}
    candidates=sorted((i,'constraints') for i,m in members.items() if missing_hard(m) and recoverable(m))
    if not candidates or budget<3: chosen=[]
    elif cfg['planner']=='random':
        random.Random(17+state.get('day',0)).shuffle(candidates)
        chosen=candidates[:budget//3]
    else:
        confirmed,potential=build(state,cfg)
        future={q:cfg['future_weight']*future_value(members[q[0]],state.get('day',0)) for q in candidates}
        if cfg['planner']=='endpoint':
            chosen=[]
            for e in sorted(potential,key=lambda e:(-e.weight,e.a,e.b)):
                for q in sorted(e.requirements):
                    if q not in chosen and len(chosen)<budget//3: chosen.append(q)
        elif cfg['planner']=='singleton':
            chosen=[]
            while len(chosen)<budget//3:
                old=utility(chosen,confirmed,potential,future)
                ranked=sorted((-(utility(chosen+[q],confirmed,potential,future)-old),q) for q in candidates if q not in chosen)
                if not ranked or ranked[0][0]>=-1e-14: break
                chosen.append(ranked[0][1])
        else:
            screened=screen(candidates,potential,cfg['candidate_limit'],future)
            chosen=list(exhaustive(screened,budget,confirmed,potential,future,cfg['portfolio_limit'])[0])
    asks=[{'member_id':q[0],'field':q[1]} for q in chosen]
    remaining=budget-3*len(chosen)
    if cfg['soft_questions'] and remaining:
        # Soft questions are an explicit ablation: known hard-eligible active members first.
        for i,m in sorted(members.items()):
            if missing_hard(m): continue
            for key in SOFT:
                if remaining and m.get('field_status',{}).get(key)=='not_asked':
                    asks.append({'member_id':i,'field':key});remaining-=1
    return asks
