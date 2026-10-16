# Recovery submission checklist

**Docker and tested-source publication passed.** The documentation-only revision awaits authorized push and public-link verification; the official submission issue requires separate approval. The unchanged `results/recovery/quality_gates.json` is a historical pre-CI snapshot, superseded for release status by this checklist and [CI_VALIDATION.md](CI_VALIDATION.md).

| Gate | Requirement | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Repository and recovery reference | PASS | git origin and recovery tag |
| 2 | Official source and attribution | PASS | byte comparison with protected commit; provenance docs |
| 3 | Starter plus custom tests | PASS | recovery_final_tests.log |
| 4 | Official engine execution | PASS | results/recovery/final.json |
| 5 | Legal JSON and hard eligibility | PASS | tests/test_recovery.py and full episodes |
| 6 | Full episodes | PASS | 18 selected subprocess episodes |
| 7 | Three baselines | PASS | results/recovery/{greedy,no_asks,random}.json |
| 8 | Six scenarios | PASS | six scenario means |
| 9 | Future-value investigation | PASS | screen/A_future.json and original future study |
| 10 | Pruning audit | PASS | evidence_audit.json: 540 exact counts |
| 11 | Calibration recomputation | PASS | evidence_audit.json: recomputed Brier |
| 12 | Waiting and coverage | PASS | report_tables.json |
| 13 | Controlled ablations | PASS | screen and confirm JSON |
| 14 | Offline Docker build/evaluation | PASS | CI 38919907335: actual build and official seed-101 container evaluation exit 0 |
| 15 | Enforced container resource limits | PASS (tested scope) | One official network-disabled episode under CPU/RAM/time limits; image 117.925 MiB; no separate peak-RAM telemetry |
| 16 | Report and results reconciled | PASS | report_tables.json and generated technical report |
| 17 | Licences and model provenance | PASS | docs/LICENSES.md and unchanged model bytes |
| 18 | Local release source prepared | PASS | release_checks_complete.json; uncommitted state checked separately |
| 19 | Immutable public commit available | PASS (tested source) | Public `98c5440dba6a2780f2ffd766c4f576fd796c4abb` and verified report/results; documentation revision publication pending |
| 20 | Authorized official submission | BLOCKED | Requires authorized documentation push, final public-link verification and separate issue approval |
