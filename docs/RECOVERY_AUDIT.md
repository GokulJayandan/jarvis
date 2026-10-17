# Competitive recovery audit

The starting candidate was clean on `main` at
`a918583473afbb0bc70abe76f1266c39331bf97b`. Origin was verified as
`https://github.com/GokulJayandan/jarvis.git`. The local tag
`recovery/pre-competitive-recovery` protects that commit. No upstream remote was
changed, no repository was created, and nothing was pushed.

`results/recovery/inventory.json` records the protected Git tree (including blob
identifiers and sizes) and separately labels working-file SHA-256 values. It
covers tracked source, tests, report, result files, Docker configuration, model
assets, dependency notices and CI. The original result paths remain unchanged;
new execution logs use the `recovery_` prefix and new experiments live under
`results/recovery/`.

Two replay scopes are distinguished: the full 18-episode preserved soft
configuration runs through the updated dispatcher, with all action hashes and
outcomes compared to the original. An additional smoke episode extracts and
executes the protected commit's exact Git bytes, verified against its original
18-file inference fingerprint (`protected_source_audit.json`). Neither replay
changes the protected commit or original experiment files.

## Reconciled original evidence

The raw 18-episode files contain 14 greedy, 5 no-asks, 10 random and 13 RAVEN
qualifying outcomes, each over 3,600 arrivals. Corresponding scores are 0.3889,
0.1389, 0.2778 and 0.3611 MSMI per 100. Every recorded episode is valid.
`results/recovery/matched_diagnostics.json` contains the seed/scenario paired
table, raw totals and paired uncertainty. Runtime excludes experiment-side
diagnostics and differs between in-process and actual subprocess modes.

The audit independently recomputes held-out calibration Brier scores from saved
pre-action features and mature labels. For all 540 pruning records it verifies
the exact combination count, common budget and arithmetic of regret. These are
540 comparisons over 36 underlying states, not 540 independent populations.
Execution-log checksums are checked against recorded metadata. Evidence:
`results/recovery/evidence_audit.json` and `results/execution/recovery_audit.*`.

The original resource sampler measured only the launched PID. Windows venv Python
was verified to spawn a separate child interpreter, so original RAM figures may
underestimate total memory. Recovery fixes the sampler to include recursive
descendants and reruns final resource checks. Old results are preserved and must
not be interpreted as full-process-tree memory measurements. At pruning limit
12, only 3 of 108 historical comparisons removed candidates; zero observed regret
is therefore much weaker evidence than the headline comparison count suggests.

The old choice among 13 policies used only two validation seeds. That is a weak
basis for selecting a rare-event outcome winner. The recovery registry declares
new screening, confirmation and untouched reporting seeds before evaluation.
Aliases V6=V0 and V7=V1 are explicitly identified rather than counted as distinct
algorithms. Confirmation uses five paired seed clusters; its intervals are still
low-powered and not adjusted for policy selection. The original test seeds are
used for diagnosis and reproduction, never recovery selection.

## Container and publication

The Dockerfile pins Python 3.12.7 by digest, copies only inference source/assets
and notices, runs as an unprivileged user, and has no installation or runtime
network dependency. Dependencies used by research scripts are separate.
The actual local build failed to launch because Docker is absent; the official
container runner returned exit code 2. See `recovery_docker_build.*`,
`recovery_container.*`, and `results/recovery/container_check.json`.

CI now builds the actual Dockerfile on Ubuntu, runs the official evaluator,
compares action hashes and outcomes with the subprocess run, checks image size,
and uploads command logs, exit codes and results even on failure. It has only
`contents: read` permission and requires no secrets. The earlier local failure
is historical. Expanded [CI run 39042745485](https://github.com/GokulJayandan/jarvis/actions/runs/39042745485)
passed the clean build, 93 tests, all six container families, action/outcome
comparison, image-size assertion and Linux boundary/resource probes at public
commit `66874ac68ea8ab030a92e0a5b1f3542cffc1a411`. See
`FINAL_HARDENING_AUDIT.md`; form-complete issue preparation tooling is ready, and the immutable final-SHA package remains unposted.

Public PyPI metadata was checked for every pinned development dependency:
`results/recovery/ci_dependency_check.json` records Python 3.14 compatibility and
published Linux/universal wheels. That file remains a static readiness check. Actual Linux dependency installation
and container execution are now evidenced separately by the successful CI run.

## Current official rules

`results/recovery/official_status.json` records the freshly fetched public main
commit and issue list. Main remains
`a8e26b35118cfa8e886a02f93984923e43ab64f6`. The public submission guide and schedule
correction retain 18 October 2026 at 23:59 IST. No extension was found. Official
simulator, evaluator, validation semantics and dataset bytes are unchanged.

Final gate classifications and recovery results are generated in
`docs/RECOVERY_RELEASE.md`; absence of an executed check must remain NOT TESTED
or BLOCKED, never PASS.
