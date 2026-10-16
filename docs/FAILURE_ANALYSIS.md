# Failure analysis

Recorded environmental failures:

* The initial sandbox process helper failed before executing commands. After the
  user enabled execution, local commands worked. No remote was changed.
* Windows Git autocrlf changed copied dataset byte sequences and caused the first
  checksum verification to fail. Exporting upstream objects with autocrlf disabled
  restored the published bytes; `.gitattributes` protects future checkouts.
* Python's `python.exe` on PATH was a Store alias. A local virtual environment was
  created from the working `py` interpreter (Python 3.14.6); command logging prepends
  its Scripts directory to PATH without changing the global installation.
* Docker is not installed. The exact build command failed to launch; the exact
  official container evaluation exited 2, recording an invalid episode due to the
  missing executable. WSL setup exited 1. These are blocking packaging-verification
  failures, not passing checks. See `results/execution/docker_*` and `wsl_setup.*`.
* A matching comparison test initially looked up unordered pairs using numeric
  rather than string lexicographic order. Corrected the test's canonical keys;
  both the brute-force and installed-NetworkX comparisons pass.
* The first dense resource probe blocked on its own unread stdout pipe when a
  valid 100-pair response exceeded the Windows pipe buffer. The probe now uses
  file-backed stdout/stderr, matching the official runner, and is re-executed.
  This was a measurement-harness defect; no inference algorithm changed.
* Git would normalize Windows-generated model assets and execution logs while
  staging them, invalidating raw-byte fingerprints. Those artifact paths now use
  explicit no-translation attributes, and the index is checked against the measured
  model and log hashes. Inference files and their measured values are unchanged.

Algorithmic limits:

* Declined hard fields permanently prevent an introduction under this contract.
  No prediction imputes them into confirmed feasibility.
* Sparse geography can produce no feasible supply; question budgets do not create
  compatible people. Unserved members remain in the primary-score denominator.
* Delayed dates may miss the qualifying 30-day window. Delayed or absent intention
  responses do not imply personal rejection.
* Joint question value is approximated by allocation with expected edge weights.
  It does not integrate the full answer distribution or shared edge dependencies.
* Future value uses pooled arrival/zone priors and an assumed survival discount.
  It can spend questions on members who never obtain a future match.
* Frozen pooled predictors cannot observe private preference bias, adapt perfectly
  to shift/drift, or remove policy-induced label selection. Calibration is conditional
  on the logged baseline introduction distribution.
* Candidate pruning and capped unpruned search can miss useful portfolios.
  Exact small-state surrogate regret is not a bound on full-episode MSMI loss.
* Selecting among several policies on two seed clusters risks winner's bias. Final
  and fresh test outcomes must be reported without additional tuning.
