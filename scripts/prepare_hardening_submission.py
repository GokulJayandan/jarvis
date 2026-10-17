"""Prepare, but never post, an immutable final issue and source archive.

Run after the candidate is committed, public, and its code-equivalent Docker CI
has passed. Outputs are kept outside tracked scientific evidence in .submission.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import urllib.request
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[1]
REPO='GokulJayandan/jarvis'
sys.path.insert(0,str(ROOT))
from scripts.verify_hardening_ci import verify

def cmd(*args):return subprocess.check_output(args,cwd=ROOT,timeout=120)
def require(condition,message):
    if not condition:raise RuntimeError(str(message))

def main():
    p=argparse.ArgumentParser();p.add_argument('--commit',default='HEAD');p.add_argument('--ci-run',required=True,type=int)
    p.add_argument('--artifact',required=True);args=p.parse_args()
    sha=cmd('git','rev-parse','--verify',args.commit+'^{commit}').decode().strip()
    require(len(sha)==40,'Full immutable commit SHA required')
    verified=verify(args.artifact,args.ci_run)
    context=['Dockerfile','.dockerignore','kit.py','policy.py','official_policy.py','raven','LICENSE','DATA_LICENSE.md']
    changed=cmd('git','diff','--name-only',verified['head_sha'],sha,'--',*context).decode().splitlines()
    require(not changed,f'Docker build context differs from successful CI: {changed}')
    remote=cmd('git','ls-remote','origin','refs/heads/main').decode().split()[0]
    require(sha==remote,'Candidate is not published as origin/main')
    paths=['README.md','report/TECHNICAL_REPORT.md','results/recovery/final.json',
           'results/recovery/greedy.json','results/recovery/no_asks.json','results/recovery/random.json',
           'docs/FINAL_HARDENING_AUDIT.md','raven/assets/final_config.json','raven/assets/model.json']
    links=[]
    for path in paths:
        url=f'https://raw.githubusercontent.com/{REPO}/{sha}/{path}'
        # No Authorization header: this establishes unauthenticated public access.
        raw=urllib.request.urlopen(url,timeout=45).read()
        expected=cmd('git','show',sha+':'+path)
        require(raw==expected,f'Public bytes do not match Git: {path}')
        links.append(dict(path=path,url=url,sha256=hashlib.sha256(raw).hexdigest(),public_bytes_match=True))
    out=ROOT/'.submission'/('final-hardening-'+sha[:12]);out.mkdir(parents=True,exist_ok=True)
    archive=out/('jarvis-'+sha+'.zip')
    temporary=archive.with_name(archive.name+'.tmp')
    temporary.unlink(missing_ok=True)
    subprocess.run(['git','archive','--format=zip','-o',str(temporary),sha],cwd=ROOT,check=True,timeout=120)
    temporary.replace(archive)
    checksum=hashlib.sha256(archive.read_bytes()).hexdigest()
    (out/(archive.name+'.sha256')).write_text(checksum+'  '+archive.name+'\n',encoding='utf-8')
    blob=f'https://github.com/{REPO}/blob/{sha}/';tree=f'https://github.com/{REPO}/tree/{sha}/'
    body=f'''### Team name and size

Team Jarvis — four participants. Project: RAVEN-Match.

### Public source URL and immutable version

Repository: https://github.com/{REPO}

Full assessed-source commit SHA: `{sha}`

Immutable source: {tree}

The deployed policy is **V1_greedy**: the supplied greedy clarification and soft-agreement greedy matching decisions, followed by independent hard-eligibility, availability, budget and duplicate-action guards. Learned probabilities, portfolio search, exact weighted matching and future-value models are research alternatives, not active deployed decision components. Final hardening repaired three standalone research edge cases without changing the selected configuration, model assets or deployed decisions.

### Report and results URLs

- Technical report: {blob}report/TECHNICAL_REPORT.md
- Mandatory benchmark, selected policy: {blob}results/recovery/final.json
- Baselines: [greedy]({blob}results/recovery/greedy.json), [no clarification]({blob}results/recovery/no_asks.json), [random feasible]({blob}results/recovery/random.json)
- All research comparisons and ablations: {tree}results/recovery
- Contract, adversarial, reproducibility and deployment audit: {blob}docs/FINAL_HARDENING_AUDIT.md
- Machine-readable hardening evidence: {tree}results/hardening

All these files and inference assets are included in the pinned assessed-source version.

### Build and evaluation commands

```sh
python -m pip install -r requirements-dev.txt
python -m unittest -v
python verify_data.py
python evaluate.py --seeds 101,102,103 --variants all --output results/submission_replay_final.json
python evaluate.py --policy official_policy.py --baseline greedy --seeds 101,102,103 --variants all --output results/submission_replay_greedy.json
python evaluate.py --policy official_policy.py --baseline no_asks --seeds 101,102,103 --variants all --output results/submission_replay_no_asks.json
python evaluate.py --policy official_policy.py --baseline random --seeds 101,102,103 --variants all --output results/submission_replay_random.json
docker build --no-cache --pull -t sequential-policy:submission .
python evaluate.py --image sequential-policy:submission --seeds 101 --variants all --output results/submission_replay_container.json
```

Offline CPU inference uses only the Python standard library and supplied files. No runtime dependency downloads, external services, credentials or GPU are required. The Python 3.12.7-slim base is digest-pinned in Dockerfile. Full research/test dependencies are separately pinned; development CI uses Python 3.14. The official runner enforces 2 CPUs, 1 GiB RAM, 10 seconds including startup, no network, 64 PIDs, read-only files, nonroot user and fresh 64 MiB tmpfs. Input, output, memory and diagnostics each have a 1 MiB limit; the image limit is 2 GiB.

### Assets, licences and tools

- Data: organisers' synthetic public kit, upstream `a8e26b35118cfa8e886a02f93984923e43ab64f6`; all 71 data checksums retained and verified. No private organiser worlds, external personal data or external pretrained model.
- Original code/docs retain the upstream MIT notice and synthetic-data terms in LICENSE and DATA_LICENSE.md. Research matching vendors NetworkX 3.6.1 blossom under BSD-3-Clause; the full notice and provenance are included. Python uses its PSF licence. Development-library notices are in docs/dependency_licenses and docs/LICENSES.md.
- The bundled research model was trained on the declared public training seeds only. Training and calibration records are separated from reporting/test seeds. See configs/seeds.json, configs/recovery.json, docs/UPSTREAM_PROVENANCE.md and the report. Training used CPU/NumPy; no hosted model or GPU is required for reproduction.
- Deployed greedy is deterministic and does not use a random inference seed. Research random-question variants use 17 + day; baseline random choices are declared in official_policy.py. No configuration or model was tuned on the untouched reporting sample.
- OpenAI Codex assisted code, tests, release audits and documentation. Automated self-review is not independent human endorsement.

### Validation and comparisons

- The mandatory comparison contains 18 valid episodes per policy (three matched seeds x all six scenario families) for selected, greedy, no-clarification and random-feasible policies. Selected and greedy both recorded 14 qualifying outcomes over 3,600 arrivals, score 0.388889 MSMI/100. This is a tie, not an improvement.
- Hypothesis-driven ablations, future-value and disclosure-calibration experiments are retained. All 540 tractable pruning comparisons were reproduced; they measure a surrogate, not actual MSMI regret or guarantees for large states.
- 93 Python 3.14 tests pass, including raw-byte JSON, independent official legality checks, matching brute-force oracles, deterministic seeded properties, failure injection and exactly 1 MiB boundary fixtures. Portable Python 3.12 compatibility and Linux Docker results are separately labelled in the audit.
- Successful Docker CI: {verified['run_url']} (tested commit `{verified['head_sha']}`). The submitted commit has byte-identical complete Docker build inputs to this successful run; the preparation preflight verifies that equivalence and binds the extracted evidence to GitHub artifact `{verified['github_artifact']['id']}` / `{verified['github_artifact']['digest']}`. The expanded run checks all six families, local/container action and outcome equality, dense/near-limit probes, image size, per-phase latency and Linux process peak RSS. See the audit for measured values and precise limits.
- **Disclosed weakness:** the frozen untouched sample yielded only 3 qualifying outcomes for the selected policy versus 16 for protected research RAVEN, over 18 episodes each. This result remains unchanged and was not used to reselect or tune the algorithm. Few seed clusters and rare events limit statistical conclusions.
- Zero invalid episodes in the public checks do not prove that every private observation will meet all validity or resource limits. No private leaderboard or real-world effectiveness claim is made.
'''
    (out/'ISSUE_BODY.md').write_text(body,encoding='utf-8')
    (out/'ISSUE_TITLE.txt').write_text('Final submission: Team Jarvis — RAVEN-Match\n',encoding='utf-8')
    manifest=dict(created_utc=datetime.now(timezone.utc).isoformat(),repository=REPO,commit=sha,remote_main=remote,
        ci_run=args.ci_run,ci_commit=verified['head_sha'],ci_url=verified['run_url'],
        ci_artifact=verified['github_artifact'],docker_build_context_identical=True,
        public_files=links,archive=archive.name,archive_sha256=checksum,posted=False,
        issue_form='https://github.com/RomeoJulietLove/The-Sequential-Matching-Problem/issues/new?template=final_submission.yml',
        deadline='2026-10-18T23:59:00+05:30')
    (out/'PREFLIGHT.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(package=str(out),commit=sha,archive_sha256=checksum,posted=False),indent=2))

if __name__=='__main__':main()
