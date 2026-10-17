# Docker validation and publication evidence

This page records the original `98c5440` CI evidence and the documentation update
at `93a2267`. Current hardening status is in [FINAL_HARDENING_AUDIT.md](FINAL_HARDENING_AUDIT.md).

Expanded release verification subsequently passed in [run 39042745485](https://github.com/GokulJayandan/jarvis/actions/runs/39042745485)
at `66874ac68ea8ab030a92e0a5b1f3542cffc1a411`: 93 tests, a clean no-cache
image build, six valid container scenarios, exact local/container actions and
outcomes, 744 timed invocations with no timeouts, and Linux boundary/resource
probes. Its checked artifact record is `results/hardening/linux_ci_verified.json`.
The remainder of this page preserves the narrower original-run evidence.

Verified 16 October 2026. The actual CI-tested source commit is
`98c5440dba6a2780f2ffd766c4f576fd796c4abb` on `GokulJayandan/jarvis`, branch `main`.
[GitHub Actions run 38919907335](https://github.com/GokulJayandan/jarvis/actions/runs/38919907335)
completed successfully. The `93a2267` documentation-only revision preserved every
non-documentation file from that tested commit, including the entire Docker
build context, evaluator, inference assets and dependencies. It does not claim
that the new documentation commit itself has already run in CI.

## Deployed policy and research scope

The deployed **V1_greedy** uses the supplied greedy clarification and
soft-agreement greedy matching decisions, followed by RAVEN's independent
hard-eligibility, availability, budget and duplicate-action guards. It does not
use learned outcome probabilities, joint portfolio search, exact weighted
matching or future-value estimates for deployed decisions. Those advanced RAVEN
modules remain evaluated research alternatives with their original experiments
and negative findings preserved. No policy was retuned using the untouched test.

## Executed CI checks

The workflow ran on Ubuntu with Python 3.14 for evaluation and the submitted
Dockerfile's pinned Python 3.12.7 image for inference. All commands below were
actually executed by the unchanged workflow; the command logger records child
exit codes rather than treating file existence as success.

| Check | Result | Evidence in the `container-verification` artifact |
| --- | --- | --- |
| `python -m unittest -v` | PASS: 63 tests | `execution/ci_tests.{json,log}` |
| `python verify_data.py` | PASS | `execution/ci_data.{json,log}` |
| `python evaluate.py --seeds 101 --output results/ci_smoke.json` | PASS, exit 0; `RAVEN_STRICT=1` | `ci_smoke.json`, `execution/ci_local.{json,log}` |
| `docker build -t sequential-policy:submission .` | PASS, exit 0; 5.223 seconds | `execution/ci_build.{json,log}` |
| `python evaluate.py --image sequential-policy:submission --seeds 101 --output results/container_check.json` | PASS, exit 0; 55.025 seconds total | `container_check.json`, `execution/ci_container.{json,log}` |
| `python scripts/compare_runs.py results/ci_smoke.json results/container_check.json` | PASS: same actions and outcomes | `execution/ci_compare.{json,log}` |
| Image inspection and 2 GiB size assertion | PASS: 123,653,457 bytes / 117.925 MiB | `container_image.json`, workflow step logs |

The container test covers **one development episode, seed 101**, with 60 decision
days and 40 follow-up days: **0 invalid episodes out of 1**, 200 arrivals,
108 introductions, 18 mutual acceptances, 15 completed meetings and one qualifying
MSMI (0.5 per 100 arrivals). The official six-family benchmark remains the
separate subprocess evidence in `results/recovery/`. This single container test
does not establish six-family container performance or private validity.

The unchanged official `evaluate.py:docker_command` applies `--network=none`,
2 CPUs, 1 GiB RAM, 64 PIDs, read-only filesystem, dropped capabilities,
non-root user and a 64 MiB temporary filesystem. Each invocation has a 10-second
timeout. No timeout, memory-limit failure or illegal action occurred in the
tested episode. The 55.025 seconds above measures the entire evaluator, not one
policy invocation. CI did not collect separate peak-RAM or worst-invocation
telemetry; the older Windows sampled resource measurements remain separately
labelled and unchanged.

Image ID: `sha256:9ce9bdb4daf022a98f948d0dc8746499d80e33698e343981452ecdc00c1560b8`.
Platform: Linux amd64. Entrypoint: `["python", "policy.py"]`.
User: `65534:65534`. This ID identifies the locally built CI image, not a published
container-registry digest.

## Logs and integrity

Full job logs and the `container-verification` artifact are attached to the
[successful run](https://github.com/GokulJayandan/jarvis/actions/runs/38919907335).
Artifact ID: `12053953909`; reported archive digest:
`sha256:3eea8651cf8cf6d3845f8870c7099f3438ca3ff9c3cd963d90680c4d25d45f63`.
GitHub reports artifact expiry on 14 January 2027; artifact download may require
GitHub authentication. Local copies of the complete log and downloaded artifacts
were retained during release preparation. All six downloaded execution logs were
hashed and matched their accompanying logger metadata:

| Log | SHA-256 |
| --- | --- |
| `ci_tests.log` | `61033ab930c960380db8fb225c1384df036f604f46236d54c133d62cc7cd0337` |
| `ci_data.log` | `48732fdb3be1af0a0d92f4f0223705e5bf4ccecad6301d4e74227f564d7c7cb7` |
| `ci_local.log` | `e2b5696acd91299a32ec8c4c4aea2d1374df9679cbac15b9a79cec31d32a941e` |
| `ci_build.log` | `960aa1175dc56df9ce8a019abf627f363c536021b1ae4ca42bd4e951ff7d91c6` |
| `ci_container.log` | `835a11018a63b616ba6f45af7f4589dfd864922f294c3d394cee9a506d521a3d` |
| `ci_compare.log` | `bdc44b1142693fa1721ce1db3b38aebdedb86459cc59947641dd7cfb64664730` |

Download without overwriting experiment files:

```sh
gh run view 38919907335 --repo GokulJayandan/jarvis --log
gh run download 38919907335 --repo GokulJayandan/jarvis --name container-verification --dir .submission/ci-38919907335
```

## Reproducible documentation update

Experiment scripts, results and figures are deliberately unchanged. Their
generators predate the successful CI run and still generate the old release
status. In a disposable checkout, regenerate then apply the documentation-only
prose overlay:

```sh
python -m experiments.recovery_report
git apply docs/RELEASE_DOCUMENTATION.patch
python scripts/hardening_documentation.py
git diff --exit-code -- README.md report/TECHNICAL_REPORT.md docs/RECOVERY_RELEASE.md results/recovery/report_tables.json figures/recovery
```

The patch changes only `README.md`, `report/TECHNICAL_REPORT.md` and
`docs/RECOVERY_RELEASE.md`. It does not change metric tables or negative findings.
Apply it after regeneration, not to an already updated report. Release verification
regenerated these documents in an isolated copy and checked the patched outputs
byte-for-byte, along with unchanged tables and figures. The historical verifier
`scripts.verify_recovery` also writes pre-CI gate snapshots; run it only in a
disposable audit copy. `results/recovery/quality_gates.json` and failed local
container-result files remain historical records. Current release status is
documented in `SUBMISSION_CHECKLIST.md` and this document.

## Publication and remaining actions

The tested source commit, report and results were fetched publicly at their
SHA-pinned URLs and matched Git object bytes. At the time this baseline evidence
was recorded, documentation commit `93a2267` had not been pushed. Current release
and submission state is recorded in `FINAL_HARDENING_AUDIT.md`; historical pending
publication statements are not current release gates.

The untouched negative result is unchanged: selected guarded greedy produced
3 qualifying outcomes versus protected RAVEN's 16 over 18 episodes per arm.
Successful Docker execution establishes tested engineering validity, not
algorithmic superiority or improved generalization.
