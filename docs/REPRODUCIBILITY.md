# Reproducibility

Recovery release commands and current evidence paths are in
[RECOVERY_REPRODUCIBILITY.md](RECOVERY_REPRODUCIBILITY.md). The commands and
measurements below describe the protected original research candidate. Current
configuration and final measurements are in `results/recovery/`.

Run from the existing Jarvis repository root. Original remote:
https://github.com/GokulJayandan/jarvis.git, branch `main`. No upstream fork or push.

## Environment

Measured host: Windows 11 build 26200, Intel i3-1115G4, four logical CPUs,
8,266,694,656 bytes installed RAM; Python 3.14.6. Exact available RAM and runtime
measurements are in `results/robustness/resources.json`. Some development jobs ran
concurrently; timings are not a controlled cross-machine performance ranking.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

Python's Store alias was unavailable, so logged commands prepend `.venv/Scripts`
to subprocess PATH without changing the global installation. The official commands
themselves use `python`. Inference needs no pip dependencies; training, plots and
external solver tests use pinned development packages on Python 3.14.6.
An additional portable Windows Python 3.12.7 check passed 53 standard-library-only
tests, including official runner tests and brute-force matching verification.
See `results/execution/python312_compat.*`. The official embedded interpreter was
downloaded from `https://www.python.org/ftp/python/3.12.7/python-3.12.7-embed-amd64.zip`
into ignored `.tools/`; it is not distributed with the submission. This checks the
specified Python version on Windows, not Linux or Docker sandbox behavior.

## Mandatory checks

```text
python -m unittest -v
python verify_data.py
python evaluate.py --seeds 101 --output results/starter_smoke.json
```

Smoke ran before replacing the original starter policy. Initial data verification
failed because Git autocrlf changed bytes. Export upstream objects with
`git -c core.autocrlf=false archive`; never edit checksums. Corrected starter tests
and checksum verification passed.

The exact commands below ran on the untouched entrypoint:

```text
python evaluate.py --baseline greedy --seeds 101,102,103 --variants all --output results/greedy.json
python evaluate.py --baseline no_asks --seeds 101,102,103 --variants all --output results/no_asks.json
python evaluate.py --baseline random --seeds 101,102,103 --variants all --output results/random.json
```

After the custom entrypoint is installed, use `python -m experiments.run_baselines`,
which adds `--policy official_policy.py`. The official runner always passes
`--baseline greedy`, even for a custom default; the unchanged adapter preserves
unambiguous baseline reproduction.

```text
python evaluate.py --seeds 101,102,103 --variants all --output results/final.json
docker build -t sequential-policy:submission .
python evaluate.py --image sequential-policy:submission --seeds 101 --output results/container_check.json
```

Final evaluation uses `RAVEN_STRICT=1` to expose programming errors that might
otherwise trigger a legal empty fallback. The evaluator and validators are unchanged.

**Container status: BLOCKED.** Docker is missing; build launch failed. Official
container evaluation exited 2 and records an invalid episode for that environmental
error. WSL installation attempt exited 1. No successful image build, offline run,
image digest or enforced resource result is claimed. A working Docker host is needed.

## Research reproduction

```text
python scripts/vendor_matching.py
python -m experiments.train
python -m experiments.run_ablations
python -m experiments.run_pruning
python -m experiments.run_calibration
python -m experiments.run_future_value
python -m experiments.run_robustness
python -m experiments.generate_figures
python -m experiments.generate_report
python -m scripts.check_provenance
```

Vendoring requires pinned NetworkX and preserves its notices. Training reconstructs
public worlds only. Never run `organise.py prepare` for this submission. Training
observations retain pre-action features and matured labels, not hidden state.
`configs/seeds.json` declares all populations and inference seed 17. Manifest test
pools stay outside fitting and selection. Do not reselect after final results.

`scripts/run_logged.py LABEL COMMAND...` stores command, timestamp, exit code,
elapsed time, log and checksum under `results/execution`. Results distinguish
in-process research from subprocess evaluation. Source fingerprints and asset hashes
accompany research runs. Figures and report tables read stored JSON only.

## Packaging and publication

The image includes policy, constants/baseline helpers, raven and licence notices.
It excludes datasets, experiments, results, .git and credentials. Validate using
the official offline read-only flags before publication. See the submission
checklist and independent automated review. Publication and the official issue
require explicit authorization.
The prepared GitHub Actions workflow installs the pinned research dependencies,
runs tests, builds the image, executes the official offline Docker episode, checks
image size, and compares action hashes/outcomes against local execution. It has
not run: publication is not authorized. After an authorized push, its uploaded
artifact can supply Docker evidence without installing Docker on this Windows PC.
