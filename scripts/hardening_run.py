"""Reproducible validity audit; never selects policy parameters or overwrites research results.

python scripts/hardening_run.py --output results/hardening/local
python scripts/hardening_run.py --output results/hardening/linux --image sequential-policy:submission
"""
import argparse
import copy
import hashlib
import io
import json
import math
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from evaluate import LIMIT,VARIANTS,episode,validate_response,strict_json,docker_command,summarise
from kit import generate
from tests.hardening_fixtures import compatible_sim,near_limit_request,request,payload

def write(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n',encoding='utf-8')

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def stats(values):
    if not values:return None
    ordered=sorted(values)
    return dict(n=len(values),median=statistics.median(values),p95=ordered[math.ceil(.95*len(values))-1],
                p99=ordered[math.ceil(.99*len(values))-1],maximum=max(values),method='nearest-rank percentiles')

class Meter:
    def __init__(self,image=None):self.image=image;self.rows=[]
    def invoke(self,command,req,timeout=10):
        compact=payload(req)
        # Ordinary episodes use the official runner's exact serialization. Only
        # explicit 1 MiB wire-boundary fixtures use their compact byte encoding.
        boundary=len(compact)==LIMIT
        raw=compact if boundary else json.dumps(req,allow_nan=False).encode()
        if len(raw)>LIMIT:raise ValueError('Request exceeds limit')
        cmd=docker_command(self.image) if self.image else [sys.executable,str(ROOT/'policy.py')]
        started=time.perf_counter(); samples=[]; stop=threading.Event()
        env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1';env.pop('RAVEN_STRICT',None)
        # Sum local launcher and descendant RSS. Container memory uses the separate
        # Linux getrusage probe, never the host Docker client's RSS.
        with tempfile.TemporaryDirectory() as cwd, tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
            proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=out,stderr=err,cwd=cwd,env=env)
            def sample():
                if self.image:return
                try:
                    import psutil
                    p=psutil.Process(proc.pid)
                    while not stop.wait(.005):
                        try:
                            total=0
                            for child in [p]+p.children(recursive=True):
                                try:total+=child.memory_info().rss
                                except psutil.Error:pass
                            samples.append(total)
                        except psutil.Error:break
                except ImportError:pass
            worker=threading.Thread(target=sample,daemon=True);worker.start()
            try:proc.communicate(raw,timeout=timeout)
            except subprocess.TimeoutExpired:
                proc.kill();proc.communicate()
                if self.image:
                    subprocess.run(['docker','rm','-f',cmd[cmd.index('--name')+1]],capture_output=True,timeout=10)
                self.rows.append(dict(phase=req['phase'],timeout=True,request_bytes=len(raw)))
                raise
            finally:stop.set();worker.join(timeout=1)
            elapsed=time.perf_counter()-started
            size=out.tell();errsize=err.tell();out.seek(0);err.seek(0)
            if proc.returncode or max(size,errsize)>LIMIT:raise ValueError('Process/output failure '+err.read(2048).decode(errors='replace'))
            rawout=out.read(); diagnostics=err.read()
            response=validate_response(strict_json(rawout.decode('utf-8')),req['phase'])
            if diagnostics:raise ValueError('Unexpected fallback/diagnostic on valid observation: '+diagnostics[:1000].decode(errors='replace'))
            self.rows.append(dict(phase=req['phase'],day=req['state']['day'],seconds=elapsed,timeout=False,
                members=len(req['state']['members']),request_bytes=len(raw),response_bytes=size,
                request_encoding='compact_wire_boundary' if boundary else 'official_json_dumps',
                memory_bytes=len(json.dumps(response['memory']).encode()),stderr_bytes=errsize,
                sampled_peak_rss_bytes=max(samples) if samples else None,
                rss_scope='sum of root and recursive descendants; shared pages may be counted twice' if samples else None,
                action_sha256=hashlib.sha256(json.dumps(response,sort_keys=True).encode()).hexdigest()))
            return response,elapsed

def suite(out,stdlib=False):
    if stdlib:
        modules=['test_kit','test_release','test_runner']+['tests.'+f.stem for f in sorted((ROOT/'tests').glob('test_*.py')) if f.stem!='test_calibration']
        tests=unittest.defaultTestLoader.loadTestsFromNames(modules)
        def walk(s):
            for t in s:
                if isinstance(t,unittest.TestSuite):yield from walk(t)
                else:yield t
        tests=unittest.TestSuite(t for t in walk(tests) if t.id()!='tests.test_matching.Matching.test_against_networkx')
    else:
        tests=unittest.defaultTestLoader.discover(str(ROOT),top_level_dir=str(ROOT))
    with (out/'tests.log').open('w',encoding='utf-8') as stream:
        result=unittest.TextTestRunner(stream=stream,verbosity=2).run(tests)
    data=dict(tests=result.testsRun,failures=[(t.id(),s) for t,s in result.failures],errors=[(t.id(),s) for t,s in result.errors],
              skipped=[(t.id(),s) for t,s in result.skipped],successful=result.wasSuccessful(),log_sha256=sha(out/'tests.log'))
    write(out/'tests.json',data)
    if not result.wasSuccessful():raise RuntimeError('Test failure; see '+str(out/'tests.log'))
    print('Tests:',result.testsRun,'passed; skipped',len(result.skipped),flush=True)

def pruning(out):
    from experiments import run_pruning
    captured=[]
    with patch.object(run_pruning,'write',side_effect=lambda _,obj:captured.append(obj)):run_pruning.main()
    result=captured[0];original=json.loads((ROOT/'results/pruning/regret.json').read_text())
    write(out/'pruning_replayed.json',result)
    ignored={'oracle_seconds','pruned_seconds','peak_python_bytes'}
    assert len(result['rows'])==len(original['rows'])==540, (len(result['rows']),len(original['rows']))
    for a,b in zip(result['rows'],original['rows']):
        left=json.loads(json.dumps({k:v for k,v in a.items() if k not in ignored}))
        right={k:v for k,v in b.items() if k not in ignored}
        assert left==right, {k:(left.get(k),right.get(k)) for k in left if left[k]!=right.get(k)}
        assert a['best_value']-a['pruned_value']>=-1e-12
    write(out/'pruning_replayed.json',result)
    print('540 pruning cases reproduced exactly (excluding timing/memory).',flush=True)

def probes(meter,out):
    for phase in ('ask','match'):
        for n in (0,1,2,40,200):
            for unknown in (False,True):meter.invoke([],request(compatible_sim(n,unknown=unknown).observe(),phase))
        for dense in (False,True):meter.invoke([],near_limit_request(phase,dense))
    write(out/'probe_rows.json',meter.rows)
    print('Boundary probes:',len(meter.rows),flush=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--image')
    p.add_argument('--stdlib',action='store_true');p.add_argument('--episodes',type=int,default=1)
    p.add_argument('--tests-only',action='store_true')
    p.add_argument('--probes-only',action='store_true')
    p.add_argument('--skip-tests',action='store_true');args=p.parse_args()
    out=ROOT/args.output;out.mkdir(parents=True,exist_ok=True)
    if (out/'summary.json').exists():raise RuntimeError('Refusing to overwrite completed audit; choose new output directory')
    write(out/'environment.json',dict(python=sys.version,platform=platform.platform(),image=args.image,
        git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        source={str(f.relative_to(ROOT)).replace('\\','/'):sha(f) for f in [ROOT/'policy.py',ROOT/'Dockerfile',*sorted((ROOT/'raven').rglob('*.py')),*sorted((ROOT/'raven/assets').glob('*.json'))]}))
    if not args.skip_tests:suite(out,args.stdlib)
    if args.tests_only:return
    data=subprocess.run([sys.executable,str(ROOT/'verify_data.py')],cwd=ROOT,capture_output=True)
    (out/'data.log').write_bytes(data.stdout+data.stderr)
    if data.returncode:raise RuntimeError('Data checksum verification failed')
    pruning(out)
    meter=Meter(args.image);probes(meter,out);probe_count=len(meter.rows)
    if args.probes_only:
        write(out/'resource_summary.json',dict(invocations=len(meter.rows),
            seconds=stats([r['seconds'] for r in meter.rows]),
            sampled_peak_rss_bytes=max((r['sampled_peak_rss_bytes'] or 0 for r in meter.rows)),
            rss_scope='sum of root and recursive descendants; shared pages may be counted twice; 5 ms sampling can miss peaks'))
        return
    rows=[]
    for variant in VARIANTS:
        for seed in range(101,101+args.episodes):
            with patch('evaluate.invoke',side_effect=meter.invoke):
                try:row=episode(generate(seed,200,'evaluation',variant),[])
                except Exception as e:row=dict(valid=False,error=repr(e))
            row.update(variant=variant,seed=seed);rows.append(row)
            write(out/'episodes.json',dict(episodes=rows,summary=summarise(rows)))
            write(out/'invocations.json',meter.rows)
            print(variant,seed,'valid=',row['valid'],flush=True)
    telemetry={phase:stats([r['seconds'] for r in meter.rows if r.get('seconds') is not None and r['phase']==phase]) for phase in ('ask','match')}
    telemetry['all']=stats([r['seconds'] for r in meter.rows if r.get('seconds') is not None])
    for key in ('request_bytes','response_bytes','memory_bytes','stderr_bytes','sampled_peak_rss_bytes'):
        telemetry[key]=max((r[key] for r in meter.rows if r.get(key) is not None),default=None)
    telemetry['timeouts']=sum(r['timeout'] for r in meter.rows)
    telemetry['empty_state_startup_seconds']=stats([r['seconds'] for r in meter.rows[:probe_count] if r.get('members')==0])
    summary=dict(mode='container' if args.image else 'trusted_local',telemetry=telemetry,
        invalid_episodes=sum(not r['valid'] for r in rows),episodes=len(rows),probes=probe_count,
        scope='Empirical tested states only. No guarantee for all private observations. No policy selection.',summary=summarise(rows))
    if args.image:
        inspect=json.loads(subprocess.check_output(['docker','image','inspect',args.image]))[0]
        write(out/'image.json',inspect);summary['image_size_bytes']=inspect['Size'];assert inspect['Size']<=2*1024**3
    write(out/'summary.json',summary)
    if summary['invalid_episodes']:raise SystemExit(2)

if __name__=='__main__':main()
