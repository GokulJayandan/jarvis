"""Verify actual recovery evidence; deliberately does not pass Docker/publication."""
import hashlib
import json
import subprocess
from experiments.common import ROOT,fingerprint,write,paired_ci
from evaluate import summarise,VARIANTS

def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
def run(path,count,seeds):
    data=read(path);rs=data['episodes']
    assert len(rs)==count and all(r['valid'] for r in rs),path
    assert data['summary']==summarise(rs),path
    assert {r['variant'] for r in rs}==set(VARIANTS),path
    assert {r['seed'] for r in rs}==set(seeds),path
    for r in rs:
        assert r['mutual_second_meeting_intention']<=r['dates']<=r['mutual_acceptances']<=r['assignments']
        assert r['served_members']+r['unserved_members']==r['arrived_members']
        assert len(r['first_introduction_wait_days'])==r['served_members']
    return data

def main():
    protected='a918583473afbb0bc70abe76f1266c39331bf97b'
    assert subprocess.check_output(['git','rev-parse','recovery/pre-competitive-recovery'],cwd=ROOT,text=True).strip()==protected
    assert subprocess.check_output(['git','remote','get-url','origin'],cwd=ROOT,text=True).strip()=='https://github.com/GokulJayandan/jarvis.git'
    assert read('results/recovery/frozen_source.json')==fingerprint()
    for name in ('greedy','no_asks','random','final'):run(f'results/recovery/{name}.json',18,[101,102,103])
    from scripts.compare_runs import compare
    for name in ('greedy','no_asks','random'):compare(ROOT/f'results/{name}.json',ROOT/f'results/recovery/{name}.json')
    compare(ROOT/'results/final.json',ROOT/'results/recovery/reproduced_frozen.json')
    protected_audit=read('results/recovery/protected_source_audit.json')
    assert protected_audit['commit']==protected and protected_audit['same_actions_and_outcomes']
    plan=read('configs/recovery.json');original=read('configs/seeds.json')
    old=set(sum([v for v in original.values() if isinstance(v,list)],[]))
    groups=[set(plan[k]) for k in ('screening_validation_seeds','confirmation_validation_seeds','untouched_reporting_seeds')]
    assert not any(g&old for g in groups)
    assert not any(a&b for i,a in enumerate(groups) for b in groups[i+1:])
    shortlist=read('results/recovery/shortlist.json')['names']
    for n in plan['variants']:
        if n not in plan['aliases_not_separate_experiments']:run(f'results/recovery/screen/{n}.json',18,plan['screening_validation_seeds'])
    for n in shortlist:run(f'results/recovery/confirm/{n}.json',30,plan['confirmation_validation_seeds'])
    selection=read('results/recovery/selection.json');greedy=read('results/recovery/confirm/V1_greedy.json')
    for n,ci in selection['comparisons'].items():
        assert ci==paired_ci(read(f'results/recovery/confirm/{n}.json')['episodes'],greedy['episodes'])
    qualifying=[n for n,c in selection['comparisons'].items() if c['ci95'][0]>0]
    expected=min(qualifying,key=lambda n:(-selection['scores'][n],n)) if qualifying else 'V1_greedy'
    assert selection['selected']==expected
    for p in (ROOT/'results/recovery/fresh').glob('*.json'):run(str(p.relative_to(ROOT)),18,plan['untouched_reporting_seeds'])
    if selection['selected']=='V1_greedy':compare(ROOT/'results/recovery/greedy.json',ROOT/'results/recovery/final.json')
    for path in ('kit.py','evaluate.py','organise.py','verify_data.py','test_kit.py','test_release.py','test_runner.py','data_manifest.json','data_checksums.json','LICENSE','DATA_LICENSE.md','official_policy.py','raven/assets/model.json'):
        expected_bytes=subprocess.check_output(['git','show',protected+':'+path],cwd=ROOT)
        assert (ROOT/path).read_bytes()==expected_bytes,path
    for p in (ROOT/'results/execution').glob('*.json'):
        d=json.loads(p.read_text())
        if 'log_sha256' in d:assert hashlib.sha256(p.with_suffix('.log').read_bytes()).hexdigest()==d['log_sha256'],str(p)
    for label in ('recovery_final_tests','recovery_final_data','recovery_release_checks','recovery_reproduce_compare','recovery_search'):
        assert read('results/execution/'+label+'.json')['exit_code']==0,label
    resources=read('results/recovery/robustness/resources.json');adversarial=read('results/recovery/robustness/adversarial.json')
    probes=resources['calls']+adversarial['calls']
    assert len(probes)==48 and adversarial['valid']
    large=read('results/recovery/robustness/max_payload_process_tree.json')
    assert large['valid'] and len(large['calls'])==6 and large['source']==fingerprint()
    probes+=large['calls']
    assert all('descendant' in p['rss_scope'] for p in probes)
    assert resources['source']==adversarial['source']==fingerprint()
    assert all(p['seconds']<10 and p['peak_sampled_rss_bytes']<1024**3 and max(p['request_bytes'],p['response_bytes'])<=1048576 for p in probes)
    assert read('results/recovery/evidence_audit.json')['pruning_enumeration_verified']==540
    tables=read('results/recovery/report_tables.json')
    assert tables['selected']==selection['selected'] and len(tables['scenarios'])==6
    for n in ('greedy','no_asks','random','final'):
        assert tables['totals'][n]['score']==read(f'results/recovery/{n}.json')['summary']['primary_score']
    for item in read('figures/recovery/catalog.json'):assert (ROOT/item['file']).stat().st_size>1000
    gates=[]
    requirements=['Repository and recovery reference','Official source and attribution','Starter plus custom tests','Official engine execution','Legal JSON and hard eligibility','Full episodes','Three baselines','Six scenarios','Future-value investigation','Pruning audit','Calibration recomputation','Waiting and coverage','Controlled ablations','Offline Docker build/evaluation','Enforced container resource limits','Report and results reconciled','Licences and model provenance','Local release source prepared','Immutable public commit available','Authorized official submission']
    evidence=['git origin and recovery tag','byte comparison with protected commit; provenance docs','recovery_final_tests.log','results/recovery/final.json','tests/test_recovery.py and full episodes','18 selected subprocess episodes','results/recovery/{greedy,no_asks,random}.json','six scenario means','screen/A_future.json and original future study','evidence_audit.json: 540 exact counts','evidence_audit.json: recomputed Brier','report_tables.json','screen and confirm JSON','Docker missing: build launch failure; evaluator exit 2','Windows sampled probes only','report_tables.json and generated technical report','docs/LICENSES.md and unchanged model bytes','release_checks_complete.json; uncommitted state checked separately','Public repository still has no published refs','Requires Docker success and explicit publication/issue authorization']
    for i,(name,proof) in enumerate(zip(requirements,evidence),1):
        gates.append(dict(gate=i,requirement=name,status='BLOCKED' if i in (14,15,19,20) else 'PASS',evidence=proof))
    write('results/recovery/quality_gates.json',gates)
    lines=['# Recovery submission checklist','','**NO-GO:** Docker verification and public authorized submission remain blocked.','', '| Gate | Requirement | Status | Evidence |','| --- | --- | --- | --- |']
    lines += [f"| {g['gate']} | {g['requirement']} | {g['status']} | {g['evidence']} |" for g in gates]
    (ROOT/'docs/SUBMISSION_CHECKLIST.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    write('results/recovery/verification.json',{'scientific_artifacts_verified':True,'docker_verified':False,'public_release_verified':False,'source':fingerprint()})
    print(json.dumps({'local_evidence':'PASS','submission':'NO-GO','blocking_gates':[14,15,19,20]},indent=2))

if __name__=='__main__':main()
