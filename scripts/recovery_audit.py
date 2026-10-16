"""Reconcile existing evidence without rewriting any original result."""
import hashlib
import json
import subprocess
from pathlib import Path
from experiments.common import ROOT,write,paired_ci

def main():
    paths=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
    inventory=[{'path':p,'bytes':(ROOT/p).stat().st_size,'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest()} for p in paths]
    tree=subprocess.check_output(['git','ls-tree','-r','--long','a918583473afbb0bc70abe76f1266c39331bf97b'],cwd=ROOT,text=True).splitlines()
    write('results/recovery/inventory.json',{'protected_commit':'a918583473afbb0bc70abe76f1266c39331bf97b',
        'protected_git_tree':tree,'working_files_at_audit_time':inventory,
        'note':'Git tree records identify the immutable protected inventory; working hashes include recovery edits made before this audit script ran.'})
    data={name:json.loads((ROOT/'results'/f'{name}.json').read_text()) for name in ('greedy','no_asks','random','final')}
    totals={n:{'episodes':len(d['episodes']),'valid':sum(r['valid'] for r in d['episodes']),
        **{k:sum(r[k] for r in d['episodes']) for k in ('mutual_second_meeting_intention','dates','arrived_members','assignments','mutual_acceptances','served_members','unserved_members','missing_feedback','ask_cost')},
        'msmi_per_100':sum(r['msmi_per_100_arrived_members'] for r in d['episodes'])/len(d['episodes'])} for n,d in data.items()}
    greedy={(r['variant'],r['seed']):r for r in data['greedy']['episodes']}
    rows=[]
    for r in data['final']['episodes']:
        b=greedy[r['variant'],r['seed']]
        out={'scenario':r['variant'],'seed':r['seed']}
        import statistics
        for entry in (r,b):entry['mean_first_introduction_wait_days']=statistics.mean(entry['first_introduction_wait_days']) if entry['first_introduction_wait_days'] else 0
        for k in ('mutual_second_meeting_intention','dates','assignments','ask_cost','coverage','mean_first_introduction_wait_days','missing_feedback','unserved_members','inference_seconds'):
            if k in r:
                out.update({f'greedy_{k}':b[k],f'raven_{k}':r[k],f'delta_{k}':r[k]-b[k]})
        rows.append(out)
    write('results/recovery/matched_diagnostics.json',{'totals':totals,'rows':rows,'paired':paired_ci(data['final']['episodes'],data['greedy']['episodes'])})
    prune=json.loads((ROOT/'results/pruning/regret.json').read_text())['rows']
    assert len(prune)==540 and all(r['reference_exact'] for r in prune)
    import math
    for r in prune:
        expected=sum(math.comb(r['original_candidates'],n) for n in range(1,min(r['original_candidates'],r['budget']//3)+1))
        assert r['oracle_portfolios']==expected
        assert len(r['optimal_portfolio'])*3<=r['budget'] and len(r['pruned_portfolio'])*3<=r['budget']
        assert abs(r['absolute_regret']-max(0,r['best_value']-r['pruned_value']))<1e-12
    calibration=json.loads((ROOT/'results/calibration/metrics.json').read_text())
    from experiments.run_calibration import metrics
    from raven.probabilities import predict_features
    observations=json.loads((ROOT/'results/calibration/heldout_observations.json').read_text())
    verified=[]
    for target in calibration['targets']:
        trials=[]
        for r in observations['rows']:
            if target['stratum']!='all' and r['stratum']!=target['stratum']:continue
            p=predict_features(r['x'],target['target'],target['model'],target['calibrated'])
            if target['target']!='directional':p=(p+predict_features(r['xr'],target['target'],target['model'],target['calibrated']))/2
            trials.append({'p':p,'y':r[target['target']]})
        calculated=metrics(trials)
        assert abs(calculated['brier']-target['brier'])<1e-12
        assert calculated['n']==target['n'] and abs(calculated['log_loss']-target['log_loss'])<1e-12
        assert abs(calculated['ece']-target['ece'])<1e-12 and calculated['bins']==target['bins']
        verified.append({k:target[k] for k in ('target','model','calibrated','stratum','n','brier','log_loss','ece')})
    disclosure=json.loads((ROOT/'results/calibration/disclosure_trials.json').read_text())
    assert metrics(disclosure)==calibration['disclosure']
    for status in ('observed','not_asked','declined'):
        assert metrics([r for r in disclosure if r['status']==status])==calibration['disclosure_strata'][status]
    for directory in ('future','future_joint_reference'):
        future=json.loads((ROOT/f'results/{directory}/future.json').read_text())
        present=json.loads((ROOT/f'results/{directory}/present.json').read_text())
        paired=json.loads((ROOT/f'results/{directory}/paired.json').read_text())
        assert paired['msmi']==paired_ci(future['episodes'],present['episodes'])
    logs=[]
    for p in (ROOT/'results/execution').glob('*.json'):
        record=json.loads(p.read_text());log=p.with_suffix('.log')
        if 'log_sha256' in record:
            assert hashlib.sha256(log.read_bytes()).hexdigest()==record['log_sha256'],str(p)
            logs.append({'label':p.stem,'exit_code':record.get('exit_code')})
    write('results/recovery/evidence_audit.json',{'calibration_recomputed':verified,'pruning_enumeration_verified':540,'execution_logs_verified':logs})
    print(json.dumps(totals,indent=2))

if __name__=='__main__':main()
