"""Small JSON logistic assets. No simulator or fitted-library imports at inference."""
from functools import lru_cache
import json
import math
from pathlib import Path
from .constraints import SOFT, HARD

def clip(p): return min(1 - 1e-6, max(1e-6, float(p)))
def sigmoid(z): return clip(1 / (1 + math.exp(-max(-30, min(30, z)))))

def features(a, b, day=0):
    fa,fb=a.get('fields',{}),b.get('fields',{})
    values=[1.0]
    for key in SOFT:
        x,y=fa.get(key),fb.get(key)
        values.extend([float(x is not None and y is not None and x==y),
                       float(x is not None and y is not None and x!=y),
                       float(x is None),float(y is None)])
    for m in (a,b):
        statuses=m.get('field_status',{})
        values.extend([sum(statuses.get(k)=='declined' for k in SOFT)/7,
                       sum(statuses.get(k)=='not_asked' for k in SOFT)/7])
    values.extend([min(day,60)/60, abs(a['age']-b['age'])/25])
    return values

def stratum(a,b):
    statuses=[m.get('field_status',{}).get(k) for m in (a,b) for k in SOFT]
    if 'declined' in statuses: return 'declined_soft'
    if 'not_asked' in statuses: return 'not_asked_soft'
    return 'fully_observed_soft'

@lru_cache(maxsize=1)
def assets():
    path=Path(__file__).parent/'assets'/'model.json'
    if not path.exists(): raise FileNotFoundError('Required trained model asset missing')
    return json.loads(path.read_text())

def predict_features(x, target='msmi', model='logistic', calibrated=True):
    spec=assets()['targets'][target]
    if model=='prior': return spec['prior']
    z=sum(v*w for v,w in zip(x,spec['weights']))
    if calibrated: z=z*spec.get('scale',1)+spec.get('offset',0)
    return sigmoid(z)

def predict(a,b,day=0,target='msmi',model='logistic',calibrated=True):
    # Pair targets are symmetric; directional models deliberately retain actor order.
    p=predict_features(features(a,b,day),target,model,calibrated)
    if target=='directional': return p
    q=predict_features(features(b,a,day),target,model,calibrated)
    return (p+q)/2

def gate_key(a,b):
    missing=[sum(m['fields'].get(k) is None for k in HARD) for m in (a,b)]
    return str(int(a['zone']==b['zone']))+':'+str(sum(n>0 for n in missing))+':'+str(min(3,abs(a['age']-b['age'])//5))

def feasibility_probability(a,b):
    model=assets()['gate']
    return model['cells'].get(gate_key(a,b),model['prior'])
