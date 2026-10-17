"""Instrumented Linux policy probes under official sandbox flags.

getrusage reports process high-water RSS, not cgroup consumption. The wrapper is
only for measurement; assessed episodes use the unchanged official entrypoint.
"""
import json
from pathlib import Path
import subprocess
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from evaluate import docker_command,validate_response,strict_json
from scripts.hardening_run import write,stats
from tests.hardening_fixtures import request,payload,compatible_sim,near_limit_request

WRAPPER="""import json,resource,runpy,sys,time
sys.argv=['policy.py']
t=time.perf_counter()
runpy.run_path('/app/policy.py',run_name='__main__')
print(json.dumps({'policy_seconds':time.perf_counter()-t,'peak_process_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024}),file=sys.stderr)
"""

def main():
    image=sys.argv[1];out=Path(sys.argv[2]);rows=[]
    for phase in ('ask','match'):
        fixtures=[('empty',request(compatible_sim(0).observe(),phase)),
                  ('dense_200',request(compatible_sim(200).observe(),phase)),
                  ('unknown_200',request(compatible_sim(200,unknown=True).observe(),phase)),
                  ('near_limit_dense',near_limit_request(phase,True)),
                  ('near_limit_unknown',near_limit_request(phase,False))]
        for name,req in fixtures:
            cmd=docker_command(image);cmd[-1:-1]=['--entrypoint','python'];cmd+=['-c',WRAPPER]
            started=time.perf_counter()
            try:p=subprocess.run(cmd,input=payload(req),capture_output=True,timeout=10)
            except subprocess.TimeoutExpired:
                subprocess.run(['docker','rm','-f',cmd[cmd.index('--name')+1]],capture_output=True,timeout=10)
                raise
            elapsed=time.perf_counter()-started
            if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace'))
            validate_response(strict_json(p.stdout.decode()),phase)
            measure=json.loads(p.stderr)
            rows.append(dict(name=name,phase=phase,wall_seconds=elapsed,**measure))
    write(out,dict(rows=rows,peak_process_rss_bytes=max(r['peak_process_rss_bytes'] for r in rows),
          policy_seconds=stats([r['policy_seconds'] for r in rows]),wall_seconds=stats([r['wall_seconds'] for r in rows]),
          caveat='Instrumented process high-water RSS via Linux getrusage. Not cgroup-wide peak. Official uninstrumented episode timings are separate.'))

if __name__=='__main__':main()
