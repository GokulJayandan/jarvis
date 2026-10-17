"""Regenerate historical figures/tables and apply release prose in a fresh audit copy."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import time
import zipfile
import shutil
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.hardening_run import write

def main():
    target=ROOT/'.submission'/('hardening-doc-replay-'+str(time.time_ns()))
    target.mkdir(parents=True)
    raw=subprocess.check_output(['git','archive','--format=zip','HEAD'],cwd=ROOT)
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:archive.extractall(target)
    shutil.copy2(ROOT/'scripts/hardening_documentation.py',target/'scripts/hardening_documentation.py')
    commands=[[sys.executable,'-m','experiments.recovery_report'],
              ['git','--git-dir='+str(ROOT/'.git'),'--work-tree='+str(target),'apply','docs/RELEASE_DOCUMENTATION.patch'],
              [sys.executable,'scripts/hardening_documentation.py']]
    for cmd in commands:
        proc=subprocess.run(cmd,cwd=target,capture_output=True)
        if proc.returncode:raise RuntimeError(proc.stderr.decode(errors='replace')[:3000])
    names=['README.md','report/TECHNICAL_REPORT.md','docs/RECOVERY_RELEASE.md','results/recovery/report_tables.json']
    names += [p.relative_to(ROOT).as_posix() for p in sorted((ROOT/'figures/recovery').glob('*')) if p.is_file()]
    rows=[]
    for name in names:
        a=(ROOT/name).read_bytes();b=(target/name).read_bytes()
        # Prose text comparisons normalize checkout line endings; figure/table bytes exact.
        text=name.endswith('.md')
        equal=(a.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n')) if text else a==b
        rows.append(dict(path=name,equal=equal,sha256=hashlib.sha256(a).hexdigest(),text_line_endings_normalized=text))
    write(ROOT/'results/hardening/document_reproduction_verified.json',dict(files=rows,all_equal=all(r['equal'] for r in rows),
        method='Historical generator + original CI prose patch + idempotent hardening prose overlay in new git archive copy'))
    if not all(r['equal'] for r in rows):raise RuntimeError(str([r['path'] for r in rows if not r['equal']]))
    print('All report prose, tables and recovery figures reproduced:',len(rows))

if __name__=='__main__':main()
