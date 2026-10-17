# Recovery submission checklist

**Original Docker and tested-source publication passed.** Current release hardening and submission status is recorded in [FINAL_HARDENING_AUDIT.md](FINAL_HARDENING_AUDIT.md). The unchanged `results/recovery/quality_gates.json` is a historical pre-CI snapshot. The table below records the original recovery gates; final hardening adds a new image verification and immutable submission package.

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
| 14 | Offline Docker build/evaluation | PASS | CI 39042745485: clean build and six official seed-101 scenario evaluations exit 0 |
| 15 | Enforced container resource limits | PASS (tested scope) | 744 calls, no timeout, max 2.577 s; 65.805 MiB instrumented process RSS; 117.925 MiB image |
| 16 | Report and results reconciled | PASS | report_tables.json and generated technical report |
| 17 | Licences and model provenance | PASS | docs/LICENSES.md and unchanged model bytes |
| 18 | Local release source prepared | PASS | release_checks_complete.json; uncommitted state checked separately |
| 19 | Immutable public commit available | PASS (tested source) | Public `66874ac68ea8ab030a92e0a5b1f3542cffc1a411`; final documentation SHA is checked by the package generator after publication |
| 20 | Official submission | READY AFTER PUBLICATION / NOT POSTED | Form-complete generator is ready; immutable issue package is created only after final-SHA CI and public-link verification |
