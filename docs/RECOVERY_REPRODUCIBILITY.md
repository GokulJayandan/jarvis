# Recovery reproduction

The protected original source is tag `recovery/pre-competitive-recovery`, commit
`a918583473afbb0bc70abe76f1266c39331bf97b`. Original results remain at their original
paths. Current release results are under `results/recovery/`; do not confuse
`results/final.json` (historical soft policy) with the recovery final file.

The exact environment and dependency versions remain in `requirements-dev.txt`
and `docs/REPRODUCIBILITY.md`. On this Windows host use
`.venv\Scripts\python.exe` because the global `python` command is a Store alias.
Linux CI uses the setup-python executable. Commands below use `python` as the
active environment interpreter.

```sh
python -m unittest -v
python verify_data.py
python evaluate.py --policy official_policy.py --baseline greedy --seeds 101,102,103 --variants all --output results/recovery/greedy.json
python evaluate.py --policy official_policy.py --baseline no_asks --seeds 101,102,103 --variants all --output results/recovery/no_asks.json
python evaluate.py --policy official_policy.py --baseline random --seeds 101,102,103 --variants all --output results/recovery/random.json
python evaluate.py --seeds 101,102,103 --variants all --output results/recovery/final.json
docker build -t sequential-policy:submission .
python evaluate.py --image sequential-policy:submission --seeds 101 --output results/recovery/container_check.json
```

Use a new output path for repeated evaluations to preserve existing evidence.
The baseline `--policy` argument is essential: the official runner always passes
`--baseline greedy` to the default custom adapter. The official evaluator is
unchanged. `scripts/run_logged.py LABEL COMMAND...` records exact arguments,
timestamps, exit codes and SHA-256 of output; use a new LABEL on every attempt.

The full controlled recovery is reproducible from the protected candidate plus
recovery code, in a clean checkout with empty `results/recovery` run directories:

```sh
python -m scripts.recovery_audit
python -m experiments.recovery reproduce
python -m experiments.recovery_diagnostics
python -m experiments.recovery search
python scripts/run_logged.py recovery_release_checks python -m scripts.recovery_release_checks
python -m scripts.recovery_max_payload
python -m scripts.recovery_finish
python -m experiments.recovery_report
python -m scripts.verify_recovery
```

Search refuses to overwrite completed run files. To repeat selection and the
protected-candidate replay from the current checkout without replacing evidence:

```sh
python -m experiments.recovery search --output-root results/recovery_repeat
python -m experiments.recovery reproduce --output-root results/recovery_repeat
python -m experiments.recovery fresh --output-root results/recovery_repeat
```

These repeat runs do not change the deployed configuration. The release script preserves the
old configuration, freezes the declared selection, executes official subprocess
benchmarks, compares baseline and selected action hashes, runs untouched seeds,
and redirects resource-probe output to recovery paths. Training coefficients are
never refitted in recovery. Models and inference source are hashed at selection
and freeze; all run files record overrides. The source fingerprint does not hash
experiment scripts; their immutable provenance is the final Git commit.

`recovery_finish` waits for the logged release-check command to finish, as shown
in the clean-checkout orchestration above. It executes the Python 3.12 standard-library
test subset and a strict-mode official subprocess smoke run, then regenerates
and verifies the report. The largest-input probe sums launcher and descendant
RSS; historical launcher-only memory results are retained but superseded for
current resource claims.

For report-only regeneration, run `python -m experiments.recovery_report`,
`git apply docs/RELEASE_DOCUMENTATION.patch`, then
`python scripts/hardening_documentation.py`. The unmodified generator
reconstructs measured tables/figures and the historical report; the two prose-only
overlays restore the baseline and expanded post-CI documentation. Use a disposable copy for verification
and compare generated tables/figures byte-for-byte. See `CI_VALIDATION.md`.
The historical `scripts.verify_recovery` rewrites old gate-status files; do not
use its pre-CI Docker/publication verdict as current evidence. Do not run historical policy-selection/training
scripts as a release step: those intentionally overwrite the old default assets.
Original calibration/pruning figures remain valid for their historical studies.

CI runs `.github/workflows/verify.yml` with read-only repository permission and
no secrets. Expanded run [39042745485](https://github.com/GokulJayandan/jarvis/actions/runs/39042745485)
passed on public commit `66874ac68ea8ab030a92e0a5b1f3542cffc1a411`: 93 tests,
a clean Docker build, six valid container scenarios, exact subprocess/container
actions and outcomes, image-size enforcement and Linux boundary/resource probes.
The earlier run 38919907335 remains baseline evidence. Downloaded logs and
artifacts were hash-verified; see `FINAL_HARDENING_AUDIT.md` and
`results/hardening/linux_ci_verified.json`. Form-complete issue preparation tooling is ready; the immutable final-SHA package
is generated after publication. The research/evaluation results are unchanged.
