"""Exercise the largest constructed valid-shaped requests below the JSON limit."""
import json
from experiments.adversarial import state
from experiments.run_robustness import invocation
from experiments.common import write,fingerprint
from kit import eligibility

def main():
    measurements=[]
    for mode in ('complete','unknown','declined'):
        lo,hi=200,1200
        while lo+1<hi:
            n=(lo+hi)//2;request={'phase':'match','state':state(mode,n),'memory':{}}
            if len(json.dumps(request).encode())<=1048000:lo=n
            else:hi=n
        s=state(mode,lo);members={m['member_id']:m for m in s['members']}
        for phase in ('ask','match'):
            response,measurement=invocation({'phase':phase,'state':s,'memory':{}})
            if phase=='match':
                pairs=response['pairs'];assert len({i for p in pairs for i in p})==2*len(pairs)
                assert all(eligibility(members[a],members[b])['status']=='feasible' for a,b in pairs)
                if mode!='complete':assert not pairs
            else:
                assert sum(3 if a['field']=='constraints' else 1 for a in response['asks'])<=12
            measurement.update(mode=mode,actions=len(response.get('pairs',response.get('asks',[]))))
            measurements.append(measurement)
            print(mode,phase,lo,measurement['seconds'],flush=True)
    write('results/recovery/robustness/max_payload_process_tree.json',{'calls':measurements,'source':fingerprint(),'valid':True,
        'scope':'Constructed public-shaped requests near 1 MiB; offline host subprocess measurements, not Docker-enforced limits.'})

if __name__=='__main__':main()
