"""Large valid public-shaped observations: no hidden state and no fabricated results."""
import copy
from itertools import combinations
from kit import eligibility
from raven.constraints import HARD,SOFT
from experiments.common import write
from experiments.common import fingerprint
from raven.config import config
from experiments.run_robustness import invocation

def state(mode,n=200):
    fields=dict(age_min=18,age_max=65,who_to_meet=['woman','man','non_binary'],
        relationship_structure='monogamous',smoking='no',partner_smoking='any',has_children=False,
        partner_children='any',wants_children='unsure',acceptable_zones=['z'],schedule=['weekend_day'])
    fields.update({k:None for k in SOFT})
    if mode!='complete':fields.update({k:None for k in HARD})
    members=[]
    for i in range(n):
        members.append(dict(member_id='syn_'+format(i,'032x'),pool_id='adversarial',synthetic=True,age=32,
            gender='woman',zone='z',arrived_day=0,available=True,source='synthetic_questionnaire',
            fields=copy.deepcopy(fields),field_status={k:'observed' if v is not None else ('declined' if mode=='declined' else 'not_asked') for k,v in fields.items()},
            field_observed_day={k:0 if v is not None else None for k,v in fields.items()}))
    return dict(schema_version='1.0.0',synthetic=True,day=0,ask_budget_remaining=12,members=members,introductions=[],feedback=[],ask_log=[])

def main():
    measurements=[]
    for mode in ('complete','unknown','declined'):
        s=state(mode);members={m['member_id']:m for m in s['members']}
        for phase in ('ask','match'):
            response,r=invocation({'schema_version':'1.0.0','phase':phase,'state':s,'memory':{}})
            if phase=='ask':
                assert sum(3 if q['field']=='constraints' else 1 for q in response['asks'])<=12
            else:
                assert all(eligibility(members[a],members[b])['status']=='feasible' for a,b in response['pairs'])
                assert len(set(i for p in response['pairs'] for i in p))==2*len(response['pairs'])
                if mode!='complete':assert response['pairs']==[]
            r.update(mode=mode,actions=len(response.get('asks',response.get('pairs',[]))));measurements.append(r)
    write('results/robustness/adversarial.json',dict(calls=measurements,valid=True,configuration=config('final'),source=fingerprint(),
        description='Artificial valid public observations, not scored population outcomes. All 200 profiles form a dense potential or confirmed graph; official eligibility checks returned actions.'))

if __name__=='__main__':main()
