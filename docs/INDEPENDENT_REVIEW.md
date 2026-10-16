# Automated independent self-review

This is structured automated self-review by the coding agent, not a human or
independently staffed audit. Evidence is linked; private validity is not guaranteed.

| Review | Severity | Finding and evidence | Action taken | Remaining risk |
| --- | --- | --- | --- | --- |
| A: Contract | High | Exact output keys, budgets, feasibility and availability in official kit | Independent sanitizer; differential tests; evaluator unchanged | Unseen observations and private runtime conditions |
| B: Algorithms | High | Potential edges must never be introduced | Separate types, hard checker, final validation; brute-force and NetworkX matching checks | Surrogate clarification values approximate dependent outcomes |
| B: Pruning | Medium | Screening can remove useful portfolios | Exact small-state regret study and capped unpruned episode ablation | Small-state surrogate regret is not MSMI regret |
| C: Statistics | High | Sparse outcomes, selective labels, delayed observation and candidate selection | Pre-action features; day-100 labels; seed-disjoint splits; paired seed-cluster bootstrap | Few independent seeds, validation winner bias, no all-pair calibration |
| D: Generalization | High | Shift, drift, sparse geography and refusals | Six public families; additional fresh-seed future comparisons | No private leaderboard or real-world effectiveness claim |
| E: Runtime | Blocking | Docker missing; container evaluation exited 2 | Attempted actual build/evaluation and WSL setup; retained failure logs | Offline sandbox limits and Python 3.12 image remain unverified |
| E: Local engineering | Medium | Windows line endings broke data checksums | Restored upstream object bytes and added .gitattributes | Verify after every clone; do not alter official manifests |
| E: Fallbacks | Medium | Valid empty fallback could hide errors | Final evaluator uses RAVEN_STRICT=1; robustness treats stderr as failure | Production fallback can sacrifice score on untested malformed states |
| F: Submission | Blocking | Public immutable commit/report/results and issue not published | Existing origin preserved; source and issue preparation tooling included | Publication needs authorization; do not submit before Docker passes |

All tables and figures are produced from committed-intended JSON, never manually
entered metrics. Tests, full episodes and environment failures must be read from
their logs and exit codes. A file's existence alone is not treated as a passing
Docker test. In-process research runs are labelled distinctly from subprocess
and container runs. Models never receive simulator seeds or hidden state.
