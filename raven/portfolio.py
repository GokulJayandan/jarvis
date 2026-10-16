"""Complementarity-aware bounded portfolio optimization of an explicit surrogate."""
from itertools import combinations

def utility(selected, confirmed, potential, future=None):
    chosen=frozenset(selected)
    edges=[(e.weight,e.a,e.b) for e in confirmed]
    edges.extend((e.weight,e.a,e.b) for e in potential if e.requirements<=chosen)
    used=set(); value=0.0
    for w,a,b in sorted(edges,key=lambda e:(-e[0],e[1],e[2])):
        if a not in used and b not in used:
            value+=w;used.update((a,b))
    return value+sum((future or {}).get(q,0) for q in chosen)

def exhaustive(candidates,budget,confirmed,potential,future=None,limit=None):
    """Exact over enumerated candidates if limit=None; utility is a surrogate."""
    best=();value=utility((),confirmed,potential,future);evaluated=0
    for n in range(1,min(len(candidates),budget//3)+1):
        for qs in combinations(candidates,n):
            if limit is not None and evaluated>=limit:
                return best,value,evaluated,False
            evaluated+=1
            v=utility(qs,confirmed,potential,future)
            if v>value+1e-14 or (abs(v-value)<1e-14 and (len(qs),qs)<(len(best),best)):
                best,value=qs,v
    return best,value,evaluated,True
