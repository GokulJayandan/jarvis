"""Export exact installed distribution licence metadata and notices."""
import importlib.metadata
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
target=root/'docs'/'dependency_licenses';target.mkdir(exist_ok=True)
records=[]
for name in [line.split('==')[0] for line in (root/'requirements-dev.txt').read_text().splitlines() if '==' in line]:
    dist=importlib.metadata.distribution(name)
    files=[]
    for path in dist.files or []:
        if ('license' in str(path).lower() or 'copying' in str(path).lower()) and '.dist-info' in str(path):
            source=dist.locate_file(path)
            if source.is_file():
                dest=target/(name+'_'+str(path).split('.dist-info/')[-1].replace('/','_'))
                dest.write_bytes(source.read_bytes());files.append(dest.name)
    records.append({'name':name,'version':dist.version,'license':dist.metadata.get('License-Expression') or dist.metadata.get('License'),'notices':files})
(target/'index.json').write_text(json.dumps(records,indent=2)+'\n')
