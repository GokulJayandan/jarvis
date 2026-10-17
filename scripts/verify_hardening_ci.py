"""Verify expanded Linux CI artifacts and emit a compact tracked attestation."""
import argparse
import hashlib
import io
import json
from pathlib import Path
from pathlib import PurePosixPath
import re
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[1]
LIMIT=1024**2
REPO='GokulJayandan/jarvis'
WORKFLOW='.github/workflows/verify.yml'
WORKFLOW_NAME='Verify Jarvis policy and offline container'
ARTIFACT_NAME='container-verification'

def load(path):return json.loads(path.read_text(encoding='utf-8'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n',encoding='utf-8')

def comparable(row):return {k:v for k,v in row.items() if k!='inference_seconds'}

def require(condition,message):
    if not condition:raise RuntimeError(str(message))

def gh_json(path):
    return json.loads(subprocess.check_output(['gh','api',path],text=True,timeout=120))

def github_evidence(run_id,base):
    run=gh_json(f'repos/{REPO}/actions/runs/{run_id}')
    require(run.get('id')==run_id,'GitHub returned a different workflow run')
    require(run.get('status')=='completed' and run.get('conclusion')=='success','Workflow did not complete successfully')
    require(run.get('path')==WORKFLOW,f'Unexpected workflow: {run.get("path")}')
    require(run.get('name')==WORKFLOW_NAME,f'Unexpected workflow name: {run.get("name")}')
    require(run.get('event')=='push' and run.get('head_branch')=='main','Release evidence must be a push to main')
    require((run.get('repository') or {}).get('full_name')==REPO,'Unexpected workflow repository')
    require((run.get('head_repository') or {}).get('full_name')==REPO,'Unexpected workflow head repository')
    response=gh_json(f'repos/{REPO}/actions/runs/{run_id}/artifacts')
    matches=[a for a in response.get('artifacts',[]) if a.get('name')==ARTIFACT_NAME]
    require(len(matches)==1,f'Expected one {ARTIFACT_NAME} artifact; found {len(matches)}')
    artifact=matches[0]
    require(not artifact.get('expired'),'GitHub Actions artifact has expired')
    embedded=artifact.get('workflow_run') or {}
    require(embedded.get('id')==run_id and embedded.get('head_sha')==run.get('head_sha'),'Artifact is not bound to the selected run')
    claimed=artifact.get('digest') or ''
    require(claimed.startswith('sha256:'),'Artifact API did not provide a SHA-256 digest')
    archive=subprocess.check_output(['gh','api',f'repos/{REPO}/actions/artifacts/{artifact["id"]}/zip'],timeout=120)
    actual='sha256:'+hashlib.sha256(archive).hexdigest()
    require(actual==claimed,f'Artifact archive digest mismatch: {actual} != {claimed}')
    zipped={}
    with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
        for info in bundle.infolist():
            if info.is_dir():continue
            name=info.filename.replace('\\','/')
            parts=PurePosixPath(name).parts
            require(name and not name.startswith('/') and '..' not in parts,f'Unsafe artifact path: {name}')
            require(name not in zipped,f'Duplicate artifact path: {name}')
            zipped[name]=bundle.read(info)
    local={p.relative_to(base).as_posix():p for p in base.rglob('*') if p.is_file()}
    require(set(zipped)==set(local),'Local evidence directory does not exactly match the GitHub artifact')
    for name,path in local.items():
        require(hashlib.sha256(zipped[name]).digest()==hashlib.sha256(path.read_bytes()).digest(),f'Artifact byte mismatch: {name}')
    return run,artifact,claimed

def verify(base,run_id):
    base=Path(base).resolve();require(base.is_dir(),f'Missing artifact directory: {base}')
    run,artifact,artifact_digest=github_evidence(run_id,base)
    execution=base/'execution';hardening=base/'hardening'
    records=[]
    for meta_path in sorted(execution.glob('*.json')):
        meta=load(meta_path);log=meta_path.with_suffix('.log')
        require(log.exists(),f'Missing command log: {log}')
        actual=sha(log)
        require(meta.get('exit_code')==0,f'Command failed: {meta_path} exit={meta.get("exit_code")}')
        require(actual==meta.get('log_sha256'),f'Command log digest mismatch: {log}')
        records.append(dict(name=meta_path.stem,exit_code=0,seconds=meta['seconds'],log_sha256=actual))
    required={'ci_tests','ci_data','ci_local','ci_build','ci_container','ci_compare',
              'ci_hardening_local','ci_hardening_container','ci_hardening_compare','ci_hardening_resources'}
    names={r['name'] for r in records}
    require(required<=names,f'Missing command records: {sorted(required-names)}')
    tests=(execution/'ci_tests.log').read_text(encoding='utf-8')
    match=re.search(r'Ran (\d+) tests',tests)
    require(match and int(match.group(1))==93 and '\nOK\n' in tests.replace('\r\n','\n'),'Expected 93 successful Linux tests')
    data=load(execution/'ci_data.log')
    require(data.get('verified') is True and data.get('files')==71,'Expected 71 verified official data files')
    local=load(hardening/'ci_local/episodes.json');container=load(hardening/'ci_container/episodes.json')
    require(local['summary']['eligible'] and container['summary']['eligible'],'Local or container episode summary is ineligible')
    left={(r['variant'],r['seed']):comparable(r) for r in local['episodes']}
    right={(r['variant'],r['seed']):comparable(r) for r in container['episodes']}
    require(left==right and len(left)==6,'Local and container outcomes differ or scenario count is wrong')
    variants={'development','sparse','cold_start','delayed','shift','drift'}
    require({v for v,_ in left}==variants,'Scenario-family coverage is incomplete')
    rows=load(hardening/'ci_container/invocations.json')
    probes=load(hardening/'ci_container/probe_rows.json')
    summary=load(hardening/'ci_container/summary.json')
    require(len(rows)==744 and len(probes)==24,'Unexpected invocation or boundary-probe count')
    require(summary['episodes']==6 and summary['invalid_episodes']==0 and summary['telemetry']['timeouts']==0,'Invalid episode or timeout recorded')
    require(all(not r['timeout'] for r in rows),'Timed-out invocation recorded')
    require(max(r['seconds'] for r in rows)<10,'Invocation exceeded the 10-second limit')
    require(max(r['request_bytes'] for r in rows)==LIMIT,'The exact 1 MiB request boundary was not tested')
    require(max(r['response_bytes'] for r in rows)<=LIMIT,'Response exceeded 1 MiB')
    require(max(r['memory_bytes'] for r in rows)<=LIMIT,'Policy memory exceeded 1 MiB')
    require(max(r['stderr_bytes'] for r in rows)<=LIMIT and all(r['stderr_bytes']==0 for r in rows),'Diagnostics were emitted or exceeded 1 MiB')
    resources=load(hardening/'container_resources.json')
    require(len(resources['rows'])==10,'Unexpected Linux resource-probe count')
    require(resources['peak_process_rss_bytes']<1024**3,'Measured process RSS exceeded 1 GiB')
    require(resources['wall_seconds']['maximum']<10,'Instrumented wall time exceeded 10 seconds')
    images=load(base/'container_image.json');require(len(images)==1,'Expected one container image record')
    image=images[0]
    require(image['Size']<=2*1024**3 and image['Architecture']=='amd64' and image['Os']=='linux','Container platform or image size is invalid')
    require(image['Config']['User']=='65534:65534','Container user is not the required nonroot user')
    require(image['Config']['WorkingDir']=='/app','Unexpected container working directory')
    require(image['Config']['Entrypoint']==['python','policy.py'],'Unexpected container entrypoint')
    artifact_files=[dict(path=p.relative_to(base).as_posix(),bytes=p.stat().st_size,sha256=sha(p))
                    for p in sorted(base.rglob('*')) if p.is_file()]
    return dict(
        verified=True,run_id=run_id,run_url=run['html_url'],head_sha=run['head_sha'],
        workflow=dict(path=run['path'],name=run['name'],event=run['event'],branch=run['head_branch']),
        github_artifact=dict(id=artifact['id'],name=artifact['name'],size_bytes=artifact['size_in_bytes'],digest=artifact_digest,expired=False),
        status=run['status'],conclusion=run['conclusion'],checked_artifact_files=len(artifact_files),
        command_records=records,tests=93,data_checksums=data['files'],
        local_container_actions_and_outcomes_equal=True,
        variants=sorted(v for v,_ in left),episodes=6,invalid_episodes=0,
        invocations=len(rows),boundary_probes=len(probes),timeouts=0,
        timing_seconds=summary['telemetry'],
        linux_process_peak_rss_bytes=resources['peak_process_rss_bytes'],
        linux_process_rss_scope=resources['caveat'],
        instrumented_policy_seconds=resources['policy_seconds'],
        instrumented_wall_seconds=resources['wall_seconds'],
        max_request_bytes=max(r['request_bytes'] for r in rows),
        max_response_bytes=max(r['response_bytes'] for r in rows),
        max_memory_bytes=max(r['memory_bytes'] for r in rows),
        max_diagnostics_bytes=max(r['stderr_bytes'] for r in rows),
        image=dict(id=image['Id'],size_bytes=image['Size'],architecture=image['Architecture'],os=image['Os'],
                   user=image['Config']['User'],working_dir=image['Config']['WorkingDir'],entrypoint=image['Config']['Entrypoint']),
        limits=dict(cpus=2,ram_bytes=1024**3,wall_seconds=10,pids=64,image_bytes=2*1024**3,
                    request_bytes=LIMIT,response_bytes=LIMIT,memory_bytes=LIMIT,diagnostics_bytes=LIMIT),
        artifact_files=artifact_files,
        scope='Empirical public states and constructed valid observations only; finite testing does not prove validity or resource bounds for every private state.')

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--artifact',required=True)
    p.add_argument('--run',type=int,required=True)
    p.add_argument('--output',default='results/hardening/linux_ci_verified.json')
    args=p.parse_args()
    result=verify(args.artifact,args.run)
    write(ROOT/args.output,result)
    print(json.dumps({k:result[k] for k in ('verified','run_url','head_sha','tests','episodes','invalid_episodes','invocations','timeouts','linux_process_peak_rss_bytes')},indent=2))

if __name__=='__main__':main()
