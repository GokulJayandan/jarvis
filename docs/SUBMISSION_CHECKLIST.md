# Recovery submission checklist

**NO-GO:** Docker verification and public authorized submission remain blocked.

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
| 14 | Offline Docker build/evaluation | BLOCKED | Docker missing: build launch failure; evaluator exit 2 |
| 15 | Enforced container resource limits | BLOCKED | Windows sampled probes only |
| 16 | Report and results reconciled | PASS | report_tables.json and generated technical report |
| 17 | Licences and model provenance | PASS | docs/LICENSES.md and unchanged model bytes |
| 18 | Local release source prepared | PASS | release_checks_complete.json; uncommitted state checked separately |
| 19 | Immutable public commit available | BLOCKED | Public repository still has no published refs |
| 20 | Authorized official submission | BLOCKED | Requires Docker success and explicit publication/issue authorization |
