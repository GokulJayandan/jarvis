"""Prepare exact local publication instructions and a visibly blocked issue draft."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
from experiments.common import ROOT

def main():
    def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
    sha=git('rev-parse','HEAD');branch=git('branch','--show-current');remote=git('remote','get-url','origin')
    assert re.fullmatch('[0-9a-f]{40}',sha)
    assert remote=='https://github.com/GokulJayandan/jarvis.git' and branch=='main'
    assert not git('status','--porcelain'),'Commit reviewed source before preparing exact publication instructions'
    final=json.loads((ROOT/'results/recovery/final.json').read_text())
    selection=json.loads((ROOT/'results/recovery/selection.json').read_text())
    fresh_selected=json.loads((ROOT/f"results/recovery/fresh/{selection['selected']}.json").read_text())
    fresh_reference=json.loads((ROOT/'results/recovery/fresh/V0_frozen.json').read_text())
    source=remote.removesuffix('.git');out=ROOT/'.submission';out.mkdir(exist_ok=True)
    body=f'''# BLOCKED DRAFT — do not submit yet

The following SHA is real and local. The SHA-pinned URLs are proposed locations,
not verified public links: publication has not been authorized. Docker validation
has not succeeded. This draft does not satisfy the final submission form yet.

### Team name and size

Jarvis — four participants. Project: RAVEN-Match.

### Public source URL and immutable version

Repository: {source}

Full local candidate SHA: `{sha}`

### Report and results URLs

Report: {source}/blob/{sha}/report/TECHNICAL_REPORT.md

Results: {source}/tree/{sha}/results/recovery

### Build and evaluation commands

```sh
docker build -t sequential-policy:submission .
python evaluate.py --image sequential-policy:submission --seeds 101 --output results/recovery/container_check.json
```

The source requires CPU only and no runtime API or filesystem persistence.
Actual offline container execution remains BLOCKED until CI succeeds.

### Assets, licences and tools

Official MIT kit, synthetic data notices, BSD-3-Clause research matcher and
packaged synthetic-data-trained JSON models are attributed. The selected policy
is `{selection['selected']}`; unused research components remain for reproducibility.
No external pretrained model, personal member data or private organizer worlds.
OpenAI Codex assisted implementation and automated review. Exact provenance:
{source}/blob/{sha}/docs/LICENSES.md

### Validation and comparisons

All three official baselines and all six scenarios were rerun on seeds 101–103.
Selected primary score: {final['summary']['primary_score']} MSMI per 100 arrivals.
The selection uses newly declared validation, followed by untouched reporting.
Untouched reporting scored {fresh_selected['summary']['primary_score']} MSMI/100
for the selected policy versus {fresh_reference['summary']['primary_score']} for
protected RAVEN. The conservative selection underperformed on that sample; the
configuration was not changed using these held-out outcomes.
Future-value, pruning-regret and disclosure-calibration investigations include
negative results and scope limitations. Container evaluation is NOT passed yet.

Reproduction: {source}/blob/{sha}/docs/RECOVERY_REPRODUCIBILITY.md

After authorized publication and successful CI, commit the successful container
evidence and updated report, obtain that new full SHA, regenerate and verify all
public links, then obtain separate issue-submission authorization. Do not submit
this blocked draft or claim the current local SHA is the final assessed version.
'''
    (out/'RECOVERY_ISSUE_DRAFT.md').write_text(body,encoding='utf-8')
    publication=f'''# Local publication request

Repository: `{remote}`
Branch: `{branch}`
Commit: `{sha}`
Push command (not executed): `git push origin main`

The reviewed source includes synthetic public data, model assets, reports and
real experiment results. Development environments, caches, `.env` files and
local release archives are ignored. The staged-content scan and byte checks
are recorded in `results/recovery/publication_scan.json`. No private organizer
data or credentials were found by those checks; pattern scanning is not a proof
that all possible sensitive material is absent.

Authorization is required by the user's explicit publication rule. Pushing this
commit triggers the Docker CI workflow. No official issue will be submitted by
the push. Docker artifacts must be inspected and incorporated into a subsequent
reviewed release commit before submission.
'''
    (out/'RECOVERY_PUBLICATION.md').write_text(publication,encoding='utf-8')
    print(publication)

if __name__=='__main__':main()
