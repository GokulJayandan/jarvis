"""Conservative staged-file screening; report locations, never matched values."""
import json
import re
import subprocess
from experiments.common import ROOT,write

def main():
    names=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
    forbidden=re.compile(r'(^|/)(?:\.env(?:\..*)?|id_rsa|id_ed25519|credentials|[^/]*\.(?:pem|pfx|p12))$',re.I)
    patterns={
        'private_key':re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
        'github_token':re.compile(rb'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,})'),
        'aws_access_key':re.compile(rb'AKIA[A-Z0-9]{16}'),
    }
    payload=''.join(':'+n+'\n' for n in names).encode()
    raw=subprocess.check_output(['git','cat-file','--batch'],cwd=ROOT,input=payload)
    pos=0;findings=[];total=0
    for name in names:
        end=raw.index(b'\n',pos);header=raw[pos:end].split();pos=end+1
        assert len(header)==3,'Unstaged/missing index file '+name
        size=int(header[2]);blob=raw[pos:pos+size];pos+=size+1;total+=size
        if forbidden.search(name):findings.append({'path':name,'kind':'sensitive_filename'})
        if b'\0' not in blob:
            for kind,pattern in patterns.items():
                if pattern.search(blob):findings.append({'path':name,'kind':kind})
    assert not any(n.startswith(('.venv/','.tools/','.submission/','dist/','.aws/')) for n in names)
    write('results/recovery/publication_scan.json',{'staged_files':len(names),'staged_bytes':total,'findings':findings,
        'limitations':'Pattern and filename screening, plus source/data provenance review; not a guarantee of detecting every possible secret. Findings omit matched values.',
        'data_scope':'Only official public synthetic data and locally generated public-seed experiment artifacts. No organizer private worlds.'})
    print(json.dumps({'files':len(names),'findings':findings}))
    if findings:raise SystemExit(1)

if __name__=='__main__':main()
