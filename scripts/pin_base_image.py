"""Resolve the public official Python base manifest, without a Docker daemon."""
import hashlib
import json
from pathlib import Path
import urllib.request

root=Path(__file__).resolve().parents[1]
tag='3.12.7-slim'
token=json.loads(urllib.request.urlopen('https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/python:pull',timeout=30).read())['token']
url='https://registry-1.docker.io/v2/library/python/manifests/'+tag
request=urllib.request.Request(url,headers={'Authorization':'Bearer '+token,
    'Accept':'application/vnd.oci.image.index.v1+json, application/vnd.docker.distribution.manifest.list.v2+json'})
with urllib.request.urlopen(request,timeout=30) as response:
    raw=response.read();digest=response.headers['Docker-Content-Digest']
assert digest=='sha256:'+hashlib.sha256(raw).hexdigest()
dockerfile=root/'Dockerfile';lines=dockerfile.read_text().splitlines();lines[0]='FROM python:'+tag+'@'+digest
dockerfile.write_text('\n'.join(lines)+'\n')
record={'base_image':'python:'+tag,'manifest_digest':digest,'registry_url':url,
        'manifest':json.loads(raw),'note':'Verified base-image manifest only. Not a built submission image or a successful Docker test.'}
(root/'results'/'base_image_manifest.json').write_text(json.dumps(record,indent=2)+'\n')
print(digest)
