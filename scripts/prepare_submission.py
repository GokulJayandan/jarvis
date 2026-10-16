"""Prepare a real SHA-pinned issue only after public source and Docker verification."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import urllib.request

root=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='.submission/FINAL_ISSUE_DRAFT.md');args=parser.parse_args()
    source=subprocess.check_output(['git','remote','get-url','origin'],cwd=root,text=True).strip().removesuffix('.git')
    sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
    if not re.fullmatch('[0-9a-f]{40}',sha):raise SystemExit('No valid full commit SHA')
    container=json.loads((root/'results/container_check.json').read_text())
    if not container['summary']['eligible']:raise SystemExit('BLOCKED: successful offline Docker evaluation is required before preparing a submission-ready issue.')
    urllib.request.urlopen(source+'/commit/'+sha,timeout=30).read(1)
    for path in ('report/TECHNICAL_REPORT.md','results/final.json'):
        urllib.request.urlopen(source+'/blob/'+sha+'/'+path,timeout=30).read(1)
    template=json.loads(urllib.request.urlopen('https://api.github.com/repos/RomeoJulietLove/The-Sequential-Matching-Problem/contents/.github/ISSUE_TEMPLATE/final_submission.yml',timeout=30).read())
    if not template.get('sha'):raise SystemExit('Could not verify current official issue template')
    final=json.loads((root/'results/final.json').read_text())
    text=f'''### Team name and size

Jarvis — four participants. Project: RAVEN-Match.

### Public source URL and immutable version

{source}

Full final commit SHA: `{sha}`

### Report and results URLs

Report: {source}/blob/{sha}/report/TECHNICAL_REPORT.md

Results: {source}/tree/{sha}/results

### Build and evaluation commands

```sh
docker build -t sequential-policy:submission .
python evaluate.py --image sequential-policy:submission --seeds 101 --output results/container_check.json
```

### Assets, licences and tools

CPU-only offline Python with packaged JSON coefficients and BSD-licensed blossom.
Official MIT kit and synthetic-data notices retained. No external pretrained models
or personal data. Declared public training seeds and exact dependency provenance:
{source}/blob/{sha}/docs/UPSTREAM_PROVENANCE.md

OpenAI Codex assisted implementation and automated self-review.

### Validation and comparisons

All three official baselines and all six public families on matched seeds 101–103.
Final primary score: {final['summary']['primary_score']} MSMI per 100 arrived members.
Required future-value, pruning-regret and calibration studies are included; negative
results and uncertainty are retained. Docker evaluation passed in the linked results.

Reproduction: {source}/blob/{sha}/docs/REPRODUCIBILITY.md
'''
    target=root/args.output;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text,encoding='utf-8')
    print(str(target));print('Draft only. This script does not submit an issue.')

if __name__=='__main__':main()
