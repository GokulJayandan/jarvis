"""Freeze the declared selection and run versioned official release checks."""
import concurrent.futures
import json
import runpy
import subprocess
import sys
import time
from pathlib import Path
from unittest.mock import patch
from experiments.common import ROOT,write,fingerprint
from raven.config import config
from scripts.run_logged import run

def command(item):
    label,args=item
    code=run(label,[sys.executable,*args])
    if code!=0:raise RuntimeError(f'{label}: exit {code}')

def main():
    if '--wait' in sys.argv:
        deadline=time.monotonic()+7200
        while not (ROOT/'results/recovery/selection.json').exists():
            log=ROOT/'results/execution/recovery_search.json'
            if log.exists() and json.loads(log.read_text()).get('exit_code')!=0:
                raise RuntimeError('Search failed; release freeze cancelled')
            if time.monotonic()>deadline:raise TimeoutError('Search did not complete')
            time.sleep(5)
    selected=json.loads((ROOT/'results/recovery/selection.json').read_text())
    target=ROOT/'raven/assets/final_config.json'
    prior=target.read_bytes()
    backup=ROOT/'results/recovery/original_final_config.json'
    if backup.exists():raise FileExistsError('Release freeze already attempted; inspect evidence before resuming')
    backup.write_bytes(prior)
    frozen=dict(config('joint'),**selected['overrides'])
    target.write_text(json.dumps(frozen,indent=2)+'\n',encoding='utf-8')
    write('results/recovery/frozen_source.json',fingerprint())
    write('results/recovery/release_selection.json',{'selected':selected['selected'],'configuration':frozen,
        'protected_candidate':'a918583473afbb0bc70abe76f1266c39331bf97b','source':fingerprint()})
    command(('recovery_final_tests',['-m','unittest','-v']))
    command(('recovery_final_data',['verify_data.py']))
    jobs=[]
    for mode in ('greedy','no_asks','random'):
        jobs.append(('recovery_baseline_'+mode,['evaluate.py','--policy','official_policy.py','--baseline',mode,
            '--seeds','101,102,103','--variants','all','--output',f'results/recovery/{mode}.json']))
    jobs.append(('recovery_final',['evaluate.py','--seeds','101,102,103','--variants','all','--output','results/recovery/final.json']))
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(command,jobs))
    for mode in ('greedy','no_asks','random'):
        command(('recovery_compare_'+mode,['scripts/compare_runs.py',f'results/{mode}.json',f'results/recovery/{mode}.json']))
    if selected['selected']=='V1_greedy':
        command(('recovery_final_equals_greedy',['scripts/compare_runs.py','results/recovery/greedy.json','results/recovery/final.json']))
    command(('recovery_fresh',['-m','experiments.recovery','fresh']))
    # Existing resource harnesses are executed unchanged; redirect only artifact destinations.
    def redirect(path,obj):write(path.replace('results/robustness/','results/recovery/robustness/'),obj)
    with patch('experiments.common.write',side_effect=redirect):
        runpy.run_module('experiments.run_robustness',run_name='__main__')
        runpy.run_module('experiments.adversarial',run_name='__main__')
    assert fingerprint()==json.loads((ROOT/'results/recovery/frozen_source.json').read_text())
    write('results/recovery/release_checks_complete.json',{'valid':True,'source':fingerprint()})

if __name__=='__main__':main()
