"""Fail on missing or inconsistent scientific evidence before packaging."""
import hashlib
import json
from pathlib import Path
from evaluate import summarise,VARIANTS
from experiments.common import ROOT
from experiments.common import fingerprint
from experiments.common import paired_ci

def read(path):return json.loads((ROOT/path).read_text())

def main():
    assert read('results/frozen_source.json')==fingerprint(),'Frozen inference source changed'
    for name in ('greedy','no_asks','random','final'):
        result=read('results/'+name+'.json')
        assert len(result['episodes'])==18,name
        assert all(r['valid'] for r in result['episodes']),name
        assert result['summary']==summarise(result['episodes']),name
        assert {r['variant'] for r in result['episodes']}==set(VARIANTS),name
        assert {r['seed'] for r in result['episodes']}=={101,102,103},name
        for r in result['episodes']:
            assert r['mutual_second_meeting_intention']<=r['dates']<=r['mutual_acceptances']<=r['assignments']
            assert r['served_members']+r['unserved_members']==r['arrived_members']
            assert len(r['first_introduction_wait_days'])==r['served_members']
    selection=read('results/selection.json')
    assert len(selection['all_candidates'])==13
    for name in selection['all_candidates']:
        result=read('results/ablations/'+name+'.json')
        assert len(result['episodes'])==12 and result['summary']['eligible']
    regret=read('results/pruning/regret.json')['rows']
    assert len(regret)==540 and all(r['reference_exact'] for r in regret)
    assert all(r['absolute_regret']>=0 for r in regret)
    cal=read('results/calibration/metrics.json')
    assert len(cal['targets'])>=12 and all(r['n']>0 for r in cal['targets'])
    assert all(cal['disclosure_strata'][s]['n']>0 for s in ('observed','not_asked','declined'))
    for name in ('present','future'):
        result=read('results/future/'+name+'.json')
        assert len(result['episodes'])==18 and result['summary']['eligible']
        assert result['configuration']=='final'
        assert result['overrides']['future_weight']==(0 if name=='present' else .5)
    assert read('results/future/paired.json')['msmi']==paired_ci(read('results/future/future.json')['episodes'],read('results/future/present.json')['episodes'])
    resources=read('results/robustness/resources.json')
    assert len(resources['calls'])==42
    adversarial=read('results/robustness/adversarial.json')
    assert adversarial['valid'] and len(adversarial['calls'])==6
    assert adversarial['source']==fingerprint()
    assert all(r['seconds']<10 and r['request_bytes']<=1048576 and r['response_bytes']<=1048576 for r in resources['calls'])
    source=read('results/provenance.json')
    unchanged={r['path']:r['unchanged'] for r in source['files']}
    official_hash=next(r['upstream_sha256'] for r in source['files'] if r['path']=='policy.py')
    assert hashlib.sha256((ROOT/'official_policy.py').read_bytes()).hexdigest()==official_hash
    for path in ('kit.py','evaluate.py','organise.py','verify_data.py','test_kit.py','test_release.py','test_runner.py','data_manifest.json','data_checksums.json','LICENSE','DATA_LICENSE.md'):
        assert unchanged[path],path
    assert all(v for k,v in unchanged.items() if k.startswith('data/'))
    registry=read('configs/seeds.json')
    train=set(registry['training']);validation=set(registry['validation'])
    heldout=set(registry['final_reporting']+registry['fresh_test']+registry['manifest_test'])
    assert not train&validation and not train&heldout and not validation&heldout
    catalog=read('figures/catalog.json')
    assert len(catalog)==12
    for item in catalog:assert (ROOT/item['file']).stat().st_size>1000
    tables=read('results/report_tables.json')
    assert len(tables['summary'])==4 and len(tables['scenario'])==24
    print(json.dumps({'bundle_verified':True,'official_episodes':72,'validation_episodes':156,'figures':12,
          'scope':'Local scientific artifacts only. Docker and public submission remain separate gates.'},indent=2))

if __name__=='__main__':main()
