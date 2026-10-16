"""Independent output guard, using observed IDs and official hard semantics."""
import json
from .constraints import eligibility,Status,SOFT

def sanitize(state,phase,action):
    members={m['member_id']:m for m in state.get('members',[]) if m.get('available')}
    out=[];used=set()
    if phase=='ask':
        budget=max(0,min(12,state.get('ask_budget_remaining',0)))
        for item in action:
            if not isinstance(item,dict): continue
            i,f=item.get('member_id'),item.get('field')
            if i not in members or f not in ('constraints',)+SOFT or (i,f) in used: continue
            cost=3 if f=='constraints' else 1
            if cost>budget: continue
            out.append({'member_id':i,'field':f});budget-=cost;used.add((i,f))
    else:
        past={tuple(sorted((x['user_a'],x['user_b']))) for x in state.get('introductions',[])}
        for pair in action:
            if not isinstance(pair,(list,tuple)) or len(pair)!=2: continue
            a,b=pair
            if a not in members or b not in members or a in used or b in used or tuple(sorted(pair)) in past: continue
            if eligibility(members[a],members[b])!=Status.CONFIRMED_FEASIBLE: continue
            out.append([a,b]);used.update(pair)
    response={'asks' if phase=='ask' else 'pairs':out,'memory':{}}
    if len(json.dumps(response,allow_nan=False).encode())>1024*1024:
        return {'asks' if phase=='ask' else 'pairs':[],'memory':{}}
    return response
