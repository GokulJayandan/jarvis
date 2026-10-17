"""Read-only checks of frozen selection, old evidence, data splits, and publication index."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.hardening_run import write,ROOT
from evaluate import summarise

BASE='98c5440dba6a2780f2ffd766c4f576fd796c4abb'
def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
def digest(b):return hashlib.sha256(b).hexdigest()

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',default='results/hardening/preflight.json');args=p.parse_args()
    frozen=['policy.py','official_policy.py','kit.py','evaluate.py','Dockerfile','.dockerignore',
            'raven/protocol.py','raven/config.py','raven/constraints.py','raven/validation.py',
            'raven/assets/final_config.json','raven/assets/model.json']
    frozen_rows=[]
    for path in frozen:
        old=subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
        same=old==(ROOT/path).read_bytes();assert same,path
        frozen_rows.append(dict(path=path,sha256=digest(old),unchanged=True))
    historical=[]
    for group in ('screen','confirm'):
        for path in sorted((ROOT/'results/recovery'/group).glob('*.json')):
            obj=json.loads(path.read_text()); rows=obj['episodes']; summary=summarise(rows)
            assert summary==obj['summary'] and summary['eligible'],str(path)
            historical.append(dict(path=path.relative_to(ROOT).as_posix(),episodes=len(rows),valid=sum(r['valid'] for r in rows)))
    assert sum(x['episodes'] for x in historical)==318
    benchmark={}
    for name in ('greedy','no_asks','random','final'):
        obj=read('results/recovery/'+name+'.json');assert summarise(obj['episodes'])==obj['summary']
        benchmark[name]=dict(episodes=len(obj['episodes']),valid=sum(r['valid'] for r in obj['episodes']),
             msmi=sum(r['mutual_second_meeting_intention'] for r in obj['episodes']),score=obj['summary']['primary_score'])
    def outcome(row):return {k:v for k,v in row.items() if k!='inference_seconds'}
    assert [outcome(r) for r in read('results/recovery/final.json')['episodes']]==[outcome(r) for r in read('results/recovery/greedy.json')['episodes']]
    old={ (r['variant'],r['seed']):outcome(r) for r in read('results/recovery/final.json')['episodes']}
    for row in read('results/hardening/local/episodes.json')['episodes']:assert outcome(row)==old[row['variant'],row['seed']]
    fresh={name:sum(r['mutual_second_meeting_intention'] for r in read('results/recovery/fresh/'+name+'.json')['episodes']) for name in ('V0_frozen','V1_greedy')}
    assert fresh=={'V0_frozen':16,'V1_greedy':3}
    logs=[]
    for path in sorted((ROOT/'results/execution').glob('*.json')):
        obj=json.loads(path.read_text());log=path.with_suffix('.log')
        if obj.get('log_sha256') and log.exists():
            assert digest(log.read_bytes())==obj['log_sha256'],str(log)
            logs.append(dict(path=log.relative_to(ROOT).as_posix(),sha256=obj['log_sha256'],exit_code=obj.get('exit_code')))
    registry=read('configs/seeds.json'); train=read('results/training/observations.json');val=read('results/training/validation_observations.json')
    train_seeds={r['seed'] for r in train['rows']}; val_seeds={r['seed'] for r in val['rows']}
    tests=set(registry['fresh_test']+registry['final_reporting']+registry['manifest_test']+[22201,22202,22203])
    assert train_seeds<=set(registry['training']) and val_seeds<=set(registry['validation'])
    assert not train_seeds&val_seeds and not tests&(train_seeds|val_seeds)
    assert all(r['matured_day']==100 and 0<=r['day']<60 for r in train['rows']+val['rows'])
    resource_counts={name:len(read('results/recovery/robustness/'+name+'.json')['calls']) for name in ('resources','adversarial','max_payload_process_tree')}
    assert sum(resource_counts.values())==54
    py312=(ROOT/'results/execution/recovery_python312.log').read_text()
    assert re.search(r'Ran 55 tests',py312) and '\nOK' in py312
    # Scan staged names/content; never print suspected secret contents.
    from scripts import scan_publication
    scans=[]
    with __import__('unittest.mock',fromlist=['patch']).patch.object(scan_publication,'write',side_effect=lambda _,obj:scans.append(obj)):
        scan_publication.main()
    write(ROOT/args.output,dict(frozen_deployed_files=frozen_rows,historical_validation=historical,
        validation_episodes=318,benchmark=benchmark,untouched_results=fresh,legacy_python312_tests=55,
        historical_resources=resource_counts,execution_logs=logs,publication_scan=scans[0],
        split_audit=dict(training_seeds=sorted(train_seeds),validation_seeds=sorted(val_seeds),test_seeds=sorted(tests),disjoint=True),
        new_six_episode_action_outcomes_identical_to_original=True,
        caveat='Historical results and log integrity checked, not newly rerun 318 selection episodes. No held-out selection.'))
    print('Frozen deployment, 318 historical validation episodes, 54 historical probes, split separation and log integrity verified.')

if __name__=='__main__':main()
