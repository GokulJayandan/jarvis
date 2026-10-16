# Contract audit — release 1.0.0

Authoritative upstream: RomeoJulietLove/The-Sequential-Matching-Problem,
commit a8e26b35118cfa8e886a02f93984923e43ab64f6. Inspected 16 October 2026.

* `docs/POLICY_INTERFACE.md`, `evaluate.invoke/validate_response`: one UTF-8
  JSON request per new process; exact output keys `asks,memory` or `pairs,memory`.
  Request: `schema_version,phase,state,memory`. Memory resets to null per episode.
  CLI passes `--baseline greedy` even when no baseline argument is supplied to
  evaluate.py; custom policy therefore uses this default for RAVEN, with
  `official_policy.py` retained for unambiguous baseline reproduction.
* `kit.Simulator.observe`: arrived members only; no seed, truth, propensity,
  future arrival or private coefficient is visible. `available` is authoritative.
* `kit.eligibility`: same ID, pool and adult checks; then reciprocal age,
  explicit gender preferences, zones, smoking and existing-children preferences;
  equal relationship structure, no explicit yes/no children-plan conflict,
  overlapping schedules. All eleven HARD fields must be present at both ends.
  A known blocker takes priority over any missing values. Declined is unknown.
* `kit.Simulator.resolve_asks`: available IDs only, `constraints` costs 3,
  each of seven named SOFT fields costs 1, daily total 12. Duplicate member/field
  requests within a batch fail. The validator permits repeated and already
  answered questions, but our planner avoids them. No delayed ask replies.
  `declined` fields never disclose; every other requested field discloses its
  exact self-report. Thus answer availability is deterministic from the
  observed status; uncertainty concerns the answer value, not whether it arrives.
* `kit.Simulator.advance`: complete atomic batch validation; distinct available
  members, one use each, no repeated unordered pair, confirmed eligibility.
  Empty batches wait. Availability incorporates busy periods, exits and observed
  pauses. Do not infer availability from unobserved events.
* `kit.Simulator.receive_feedback/metrics`, `evaluate.episode`: pending is not
  failure. Responses have seven-day deadlines. Qualifying MSMI requires a date
  within 30 days and both Yes intentions within three days of that date.
  Missing responses are missing preferences, even when a matured recorded-event
  target is zero. 60 decision days plus 40 no-action follow-up days.
* `evaluate.episode/summarise`: denominator frozen at decision day 59; each
  qualifying pair counts once. Average MSMI/100 within each family, then equally
  across six families. Tie-breaks: coverage, mutual acceptances/100, lower ask
  cost, lower inference seconds. Any invalid episode makes a run ineligible.
* `data_manifest.json`: six training, two validation, two development-test pools.
  Snapshot profiles are day 30, never substitute them for pre-decision profiles.
  Our training collects observations before actions and labels after follow-up.
* `evaluate.docker_command`, `organise.grade`: offline read-only image; no host
  mounts, 2 CPUs, 1 GiB, 64 processes, 64 MiB tmpfs, ten seconds including startup;
  request/response/memory/stderr each 1 MiB, image 2 GiB. No private worlds used.
* `docs/SUBMISSION.md`, `.github/ISSUE_TEMPLATE/final_submission.yml`: public
  repository/full SHA or immutable archive/checksum; report, results, dependencies,
  provenance and successful Docker evaluation. Submission requires explicit
  authorization. GitHub issue 1 and CHANGELOG retain 18 October 23:59 IST.

The official evaluator, simulator, validators, dataset and tests are kept intact.
Windows checkout CRLF caused initial checksum failure. Re-exporting Git object
bytes using `git -c core.autocrlf=false archive` fixed it without altering data.
