"""Collect pinned public rules, CI evidence and preserved-result checks without editing them."""
import base64
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/hardening'
UPSTREAM='RomeoJulietLove/The-Sequential-Matching-Problem'

def command(*args):
    return subprocess.check_output(args,cwd=ROOT,timeout=90)

def api(path):return json.loads(command('gh','api',path))
def digest(data):return hashlib.sha256(data).hexdigest()
def save(name,obj):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/name).write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n',encoding='utf-8')

def main():
    sha=api(f'repos/{UPSTREAM}/commits/main')['sha']
    paths=['docs/POLICY_INTERFACE.md','docs/DATA_CONTRACT.md','docs/SUBMISSION.md',
           'kit.py','evaluate.py','organise.py','CHANGELOG.md','.github/ISSUE_TEMPLATE/final_submission.yml']
    records=[]
    for path in paths:
        obj=api(f'repos/{UPSTREAM}/contents/{path}?ref={sha}')
        raw=base64.b64decode(obj['content'])
        local=ROOT/path
        records.append(dict(path=path,sha256=digest(raw),local_matches=local.exists() and local.read_bytes()==raw))
    issues=api(f'repos/{UPSTREAM}/issues?state=all&per_page=100')
    corrections=[]
    for issue in issues:
        # Discard other teams' issue bodies; never use them as algorithm evidence.
        if issue['number']!=1:continue
        corrections.append({k:issue[k] for k in ('number','title','body','updated_at','html_url')})
        corrections[-1]['comments']=api(f'repos/{UPSTREAM}/issues/1/comments')
    save('official_sources.json',dict(checked_utc=datetime.now(timezone.utc).isoformat(),upstream_commit=sha,
         files=records,corrections=corrections,issue_index=[{k:i[k] for k in ('number','title','updated_at')} for i in issues]))
    run=api('repos/GokulJayandan/jarvis/actions/runs/38919907335')
    jobs=api('repos/GokulJayandan/jarvis/actions/runs/38919907335/jobs')
    archive=ROOT/'.submission/ci-38919907335'; logs=[]
    for path in sorted((archive/'execution').glob('*.json')):
        meta=json.loads(path.read_text()); log=path.with_suffix('.log')
        logs.append(dict(name=path.name,metadata=meta,actual_log_sha256=digest(log.read_bytes()),
                         hash_matches=digest(log.read_bytes())==meta['log_sha256']))
    assert logs and all(x['hash_matches'] and x['metadata']['exit_code']==0 for x in logs)
    container=json.loads((archive/'container_check.json').read_text())
    local=json.loads((archive/'ci_smoke.json').read_text())
    assert container['episodes'][0]['action_sha256']==local['episodes'][0]['action_sha256']
    image=json.loads((archive/'container_image.json').read_text())[0]
    save('baseline_ci_verified.json',dict(run={k:run[k] for k in ('id','head_sha','status','conclusion','html_url','updated_at')},
         jobs=jobs['jobs'],logs=logs,container=container,image={k:image[k] for k in ('Id','Size','Architecture','Os','Config')},
         action_digest_equal=True))
    print('Official sources and original CI log hashes verified.')

if __name__=='__main__':main()
