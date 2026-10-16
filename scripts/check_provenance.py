"""Hash copied official files and model/inference assets for review."""
import hashlib
import json
from pathlib import Path
import subprocess
from experiments.common import write,fingerprint

root=Path(__file__).resolve().parents[1]
reference=root.parent/'raven-official-reference'
sha=subprocess.check_output(['git','-C',str(reference),'rev-parse','HEAD'],text=True).strip()
paths=subprocess.check_output(['git','-C',str(reference),'ls-tree','-r','--name-only','HEAD'],text=True).splitlines()
records=[]
for path in paths:
    expected=subprocess.check_output(['git','-C',str(reference),'show',sha+':'+path])
    p=root/path
    records.append(dict(path=path,upstream_sha256=hashlib.sha256(expected).hexdigest(),
                        local_sha256=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None,
                        unchanged=p.exists() and p.read_bytes()==expected))
write('results/provenance.json',dict(upstream_commit=sha,files=records,inference=fingerprint()))
text=f'''# Upstream provenance

Official source: https://github.com/RomeoJulietLove/The-Sequential-Matching-Problem

Pinned commit: `{sha}`. Release: 1.0.0. Downloaded 16 October 2026.
Reference checkout: sibling `raven-official-reference`, unchanged and never pushed.
The local Jarvis origin remains https://github.com/GokulJayandan/jarvis.git.

Dataset manifest SHA-256: `{hashlib.sha256((root/'data_manifest.json').read_bytes()).hexdigest()}`.

All upstream tracked files were copied from Git object bytes with autocrlf disabled.
`results/provenance.json` records each upstream and local checksum and modifications.
The original policy remains `official_policy.py`; `policy.py` is the submission adapter.
Official evaluator, simulator, action validators, data and tests are not modified.
README, Docker packaging and ignore rules are adapted; originals remain at the pinned
upstream URL. MIT notice remains in LICENSE; synthetic-data conditions remain in
DATA_LICENSE.md. All supplied profiles and outcomes are invented synthetic records.

NetworkX 3.6.1 blossom is copied under BSD-3-Clause in `raven/vendor/`, with licence,
exact source URL, original checksum and documented decorator-only changes. No
third-party package import is required by inference. No external dataset or pretrained
model is used. Model assets derive only from declared public training observations.

AI tool: OpenAI Codex assisted implementation, testing and report authoring. Reviews
are automated self-review, not independent human endorsement. Other teams' issue
contents were encountered while checking corrections; their implementation was not
downloaded or used. No private organiser world was prepared, accessed or reconstructed.
'''
(root/'docs'/'UPSTREAM_PROVENANCE.md').write_text(text,encoding='utf-8')
