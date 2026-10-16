"""Verify measured inference bytes and execution-log hashes in the Git index."""
import hashlib
import json
from pathlib import Path
import subprocess

root=Path(__file__).resolve().parents[1]
frozen=root/'results/recovery/frozen_source.json'
if not frozen.exists():frozen=root/'results/frozen_source.json'
expected=json.loads(frozen.read_text())['files'].copy()
inference_count=len(expected)
for path in (root/'results/execution').glob('*.json'):
    record=json.loads(path.read_text());log=path.with_suffix('.log')
    if log.exists() and record.get('log_sha256'):
        expected[log.relative_to(root).as_posix()]=record['log_sha256']
payload=''.join(':'+name+'\n' for name in expected).encode()
raw=subprocess.check_output(['git','cat-file','--batch'],cwd=root,input=payload)
position=0;mismatches=[]
for name,digest in expected.items():
    end=raw.index(b'\n',position);header=raw[position:end].split();position=end+1
    if len(header)!=3:raise ValueError('Staged file missing: '+name)
    size=int(header[2]);blob=raw[position:position+size];position+=size+1
    if hashlib.sha256(blob).hexdigest()!=digest:mismatches.append(name)
if mismatches:raise SystemExit('Staged checksum mismatches: '+repr(mismatches))
print(json.dumps({'staged_bytes_verified':True,'inference_files':inference_count,
                  'execution_logs':len(expected)-inference_count},indent=2))
