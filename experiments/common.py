import hashlib
import json
from pathlib import Path
import random
import statistics

ROOT=Path(__file__).resolve().parents[1]

def write(path,obj):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n',encoding='utf-8')

def fingerprint():
    paths=sorted(list((ROOT/'raven').rglob('*.py'))+list((ROOT/'raven'/'assets').glob('*.json'))+[ROOT/'policy.py'])
    files={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    return {'files':files,'sha256':hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest()}

def paired_ci(rows_a,rows_b,key='msmi_per_100_arrived_members',iterations=3000):
    b={(r['variant'],r['seed']):r for r in rows_b if r.get('valid')}
    pairs=[(r['variant'],r['seed'],r[key]-b[r['variant'],r['seed']][key]) for r in rows_a if r.get('valid') and (r['variant'],r['seed']) in b]
    seeds=sorted(set(s for _,s,_ in pairs));variants=sorted(set(v for v,_,_ in pairs))
    if not pairs:return {'n':0}
    # Resample matched seed clusters, keeping family weights equal and dependence intact.
    matrix={(v,s):d for v,s,d in pairs};rng=random.Random(7381)
    means=[]
    for _ in range(iterations):
        sample=rng.choices(seeds,k=len(seeds))
        means.append(statistics.mean(statistics.mean(matrix[v,s] for s in sample if (v,s) in matrix) for v in variants))
    means.sort()
    return {'n_episodes':len(pairs),'n_seed_clusters':len(seeds),'mean_difference':statistics.mean(d for _,_,d in pairs),
            'ci95':[means[int(.025*iterations)],means[int(.975*iterations)]],
            'method':'paired seed-cluster percentile bootstrap; six equally weighted families; descriptive with few clusters'}
