"""Real subprocess timing/RAM sampling and public sequential stress checks."""
import json
import os
import random
import subprocess
import sys
import tempfile
import time
import psutil
from evaluate import validate_response
from kit import generate,Simulator,baseline_asks,baseline_match
from raven.protocol import decide
from raven.config import config
from raven.graphs import build
from raven.clarification import questions
from raven.matching import allocate
from experiments.common import write,fingerprint

def invocation(request):
    raw=json.dumps(request).encode();start=time.perf_counter()
    out_file=tempfile.TemporaryFile();err_file=tempfile.TemporaryFile()
    p=subprocess.Popen([sys.executable,'raven_policy.py'],stdin=subprocess.PIPE,stdout=out_file,stderr=err_file)
    p.stdin.write(raw);p.stdin.close();peak=0;max_processes=0
    while p.poll() is None:
        try:
            parent=psutil.Process(p.pid)
            family=[parent]+parent.children(recursive=True)
            rss=0
            for process in family:
                try:rss+=process.memory_info().rss
                except psutil.NoSuchProcess:pass
            peak=max(peak,rss);max_processes=max(max_processes,len(family))
        except psutil.NoSuchProcess:pass
        if time.perf_counter()-start>9:
            p.kill();raise RuntimeError('Internal nine-second resource check exceeded')
        time.sleep(.005)
    out_file.seek(0);err_file.seek(0);out=out_file.read();err=err_file.read()
    out_file.close();err_file.close();elapsed=time.perf_counter()-start
    if p.returncode or err:raise RuntimeError(err.decode())
    response=validate_response(json.loads(out),request['phase'])
    return response,dict(seconds=elapsed,peak_sampled_rss_bytes=peak,rss_scope='sum of launcher and recursive descendant RSS; shared pages may be counted twice',max_processes=max_processes,request_bytes=len(raw),response_bytes=len(out),memory_bytes=len(json.dumps(response['memory']).encode()),phase=request['phase'],members=len(request['state']['members']))

if __name__=='__main__':
    calls=[];sequential=[];profiles=[]
    for variant in ('development','sparse','cold_start','delayed','shift','drift'):
        sim=Simulator(generate(15001,200,'stress',variant));memory=None
        for day in range(60):
            for phase in ('ask','match'):
                state=sim.observe();request={'schema_version':'1.0.0','phase':phase,'state':state,'memory':memory}
                if day in (0,20,59):
                    response,measurement=invocation(request);measurement.update(day=day,variant=variant);calls.append(measurement)
                    assert response==decide(request)
                else:response=decide(request)
                memory=response['memory']
                if phase=='ask':sim.resolve_asks(response['asks'])
                else:sim.advance(response['pairs'])
        for _ in range(40):sim.advance([])
        sequential.append(dict(variant=variant,seed=15001,valid=True,**sim.metrics()))
    for n in (0,200,400):
        sim=Simulator(generate(15002,n,'large','cold_start'));state=sim.observe()
        for phase in ('ask','match'):
            response,measurement=invocation({'phase':phase,'state':state,'memory':{'old':'x'*100000}})
            measurement.update(variant='large',day=0);calls.append(measurement)
    # Actual phase costs on a representative public initial observation.
    state=Simulator(generate(15003,200)).observe();cfg=config('joint')
    start=time.perf_counter();raw=json.dumps(state);json.loads(raw);profiles.append({'stage':'json_round_trip','seconds':time.perf_counter()-start})
    start=time.perf_counter();edges=build(state,cfg);profiles.append({'stage':'dual_graphs_and_prediction','seconds':time.perf_counter()-start})
    start=time.perf_counter();allocate(edges[0]);profiles.append({'stage':'matching','seconds':time.perf_counter()-start})
    start=time.perf_counter();questions(state,cfg);profiles.append({'stage':'ask_including_graphs','seconds':time.perf_counter()-start})
    from raven.graphs import ConfirmedEdge
    from itertools import combinations
    rng=random.Random(15003)
    for n in (50,100,200):
        dense=[ConfirmedEdge(f'{a:03}',f'{b:03}',rng.random()) for a,b in combinations(range(n),2)]
        start=time.perf_counter();pairs=allocate(dense);elapsed=time.perf_counter()-start
        assert elapsed<8 and len(set(i for p in pairs for i in p))==2*len(pairs)
        profiles.append(dict(stage='dense_allocation_with_work_guard',members=n,edges=len(dense),seconds=elapsed,solver='greedy' if len(dense)>6000 else 'blossom'))
    write('results/robustness/resources.json',dict(calls=calls,sequential=sequential,profiles=profiles,source=fingerprint(),
          profiles_scope='Research component microbenchmarks; guarded official greedy does not invoke the graph/predictor/portfolio components. Calls measure the actual selected policy.',
          environment={'python':sys.version,'cpu_count':os.cpu_count(),'ram':psutil.virtual_memory().total},
          limitations='Windows process-tree RSS sampled approximately every 5 ms, may miss peaks and may count shared pages twice. Launcher and descendant interpreter are included. These are not container-enforced CPU/RAM measurements.'))
