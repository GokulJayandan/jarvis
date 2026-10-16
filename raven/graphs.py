"""Potential and confirmed edges remain distinct data types."""
from dataclasses import dataclass
from itertools import combinations
from .constraints import eligibility, Status, missing_hard, recoverable
from .probabilities import predict, feasibility_probability

@dataclass(frozen=True)
class ConfirmedEdge:
    a: str
    b: str
    weight: float

@dataclass(frozen=True)
class PotentialEdge:
    a: str
    b: str
    weight: float
    requirements: frozenset

def build(state, cfg, include_potential=True):
    members=sorted((m for m in state.get('members',[]) if m.get('available')),key=lambda m:m['member_id'])
    past={tuple(sorted((i['user_a'],i['user_b']))) for i in state.get('introductions',[])}
    confirmed,potential=[],[]
    day=state.get('day',0)
    for a,b in combinations(members,2):
        ai,bi=a['member_id'],b['member_id']
        if (ai,bi) in past: continue
        status=eligibility(a,b)
        if status==Status.CONFIRMED_INFEASIBLE: continue
        if status==Status.UNKNOWN_PENDING_CLARIFICATION and (not include_potential or not recoverable(a) or not recoverable(b)): continue
        weight=predict(a,b,day,model=cfg['predictor'],calibrated=cfg['calibration'])
        weight+=cfg['waiting_weight']*min(30,day-min(a['arrived_day'],b['arrived_day']))
        if status==Status.CONFIRMED_FEASIBLE:
            confirmed.append(ConfirmedEdge(ai,bi,weight))
        else:
            required=frozenset((m['member_id'],'constraints') for m in (a,b) if missing_hard(m))
            potential.append(PotentialEdge(ai,bi,weight*feasibility_probability(a,b),required))
    return confirmed,potential
