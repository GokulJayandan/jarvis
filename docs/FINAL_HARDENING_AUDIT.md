# Final hardening audit

Audit completed 17 October 2026. Local hardening and expanded Linux Docker verification PASS for the tested scope. No universal private-state validity claim.

## Release preservation

| Item | Observed value |
| --- | --- |
| Starting local SHA | `93a226737b2963f660653a9064ca0fb232bd4907` |
| Remote main SHA | `98c5440dba6a2780f2ffd766c4f576fd796c4abb` (`git ls-remote`) |
| Branch | `main` |
| Working tree at start | Clean; local branch one commit ahead |
| Origin fetch/push | `https://github.com/GokulJayandan/jarvis.git` |
| Existing recovery reference | `recovery/pre-competitive-recovery` -> `a918583473afbb0bc70abe76f1266c39331bf97b` |
| New tested-source recovery tag | `recovery/pre-final-hardening-98c5440` -> `98c5440dba6a2780f2ffd766c4f576fd796c4abb` |
| New starting-HEAD recovery tag | `recovery/pre-final-hardening-local-93a2267` -> `93a226737b2963f660653a9064ca0fb232bd4907` |
| Baseline CI | https://github.com/GokulJayandan/jarvis/actions/runs/38919907335 |
| Expanded hardening CI | https://github.com/GokulJayandan/jarvis/actions/runs/39042745485 |

The published baseline exists locally as a commit. The additional local commit changes documentation only (12 files); its Docker and publication statements require reconciliation with original logs. No reset, removal, overwrite of existing evidence, algorithm selection, or held-out tuning is authorized by this audit.

## Scope

The selected configuration remains V1_greedy. Research-only modules are assessed separately. Existing untouched-sample weakness remains disclosed. New results go to `results/hardening/`; original experiment results remain intact. Official requirements, valid synthetic contract states, malformed defensive inputs, research API tests, and empirical deployment measurements are separately labelled.

The current public policy contract requires 2 CPUs, 1 GiB RAM, 10 seconds including startup, 64 PIDs, offline read-only containers, a fresh 64 MiB temporary directory, a 2 GiB image, and 1 MiB limits for request, response, memory, and diagnostics. The official submission guide currently states 18 October 2026, 23:59 IST. Current commit, corrections, tests and container evidence were verified.

## Reconciled official sources and original evidence

Current official commit: `a8e26b35118cfa8e886a02f93984923e43ab64f6`, checked through the GitHub API on 17 October. All eight audited local official documents/validators match upstream bytes. [Official correction #1](https://github.com/RomeoJulietLove/The-Sequential-Matching-Problem/issues/1) has no comments and retains the final deadline. No newer correction was found in the current changelog or issue index. Evidence: `results/hardening/official_sources.json`.

The original [CI run 38919907335](https://github.com/GokulJayandan/jarvis/actions/runs/38919907335) is completed/success for `98c5440`. All six downloaded execution-log hashes match their metadata and all six commands exited zero. The original container and local action digests agree. The baseline image was Linux amd64, 123,653,457 bytes, entrypoint `["python","policy.py"]`, user `65534:65534`. Its scope is one seed-101 development episode; no original per-call Linux peak-RAM telemetry exists. Evidence: `results/hardening/baseline_ci_verified.json`, `docs/CI_VALIDATION.md`.

## Expanded Linux release verification

[CI run 39042745485](https://github.com/GokulJayandan/jarvis/actions/runs/39042745485) completed successfully on hardening commit `66874ac68ea8ab030a92e0a5b1f3542cffc1a411`. `scripts/verify_hardening_ci.py` downloaded and checked 39 artifact files, every command exit code and log hash, all actions/outcomes, telemetry limits and image metadata. Machine-readable evidence: `results/hardening/linux_ci_verified.json`.

| Measurement | Observed | Official limit / interpretation |
| --- | ---: | --- |
| Full tests on Linux/Python 3.14.8 | 93/93 pass | Interface and research tests |
| Official container episodes | 6/6 valid; 0 invalid | Seed 101 in all six scenario families |
| Timed container invocations | 744; 0 timeouts | Includes 720 episode calls and 24 valid boundary probes |
| All-phase latency | median 0.415 s; P95 0.502 s; P99 0.509 s; max 2.577 s | 10 s per invocation including startup |
| Ask latency | median 0.396 s; P95 0.407 s; P99 0.422 s; max 0.441 s | Empirical tested calls |
| Match latency | median 0.495 s; P95 0.504 s; P99 0.551 s; max 2.577 s | Empirical tested calls |
| Instrumented Linux policy time | median 0.190 s; max 2.411 s | `getrusage` wrapper; ten boundary states |
| Instrumented Linux wall time | median 0.412 s; max 2.627 s | Same ten states under official Docker flags |
| Linux process peak RSS | 69,001,216 bytes (65.805 MiB) | Process high-water RSS, not cgroup-wide peak; below 1 GiB |
| Image | 123,653,732 bytes (117.925 MiB), Linux amd64 | 2 GiB limit |
| Maximum request / response / memory / diagnostics | 1,048,576 / 27,064 / 2 / 0 bytes | Each limit 1,048,576 bytes |

The local and container runs produced identical actions and outcomes for all six scenario episodes. The image has `/app` as working directory, `["python","policy.py"]` as entrypoint and `65534:65534` as user. The official runner applied network isolation, two CPUs, 1 GiB RAM/swap, 64 PIDs, read-only root, dropped capabilities, `no-new-privileges`, nonroot execution and a fresh 64 MiB `tmpfs`. The no-cache build used the digest-pinned Python 3.12.7 base and an empty Docker configuration path; inference downloaded nothing.

`scripts/hardening_preflight.py` independently checks the preserved claims:

- Original 63-test suite rerun successfully before edits. Final full suite: **93 tests, 0 failures, 0 skips** on Python 3.14.6 (`results/hardening/final_tests/`).
- Historical Python 3.12 recovery log: **55 tests**, rather than the earlier 53-test record. Final expanded Python 3.12.7 compatibility run: **90 run, 88 passed, 2 skipped** because NumPy training is absent. Two calibration tests and the external NetworkX comparison are explicitly excluded from that standard-library run; they pass in the full suite.
- **71 data checksums** pass, with original manifests and data unchanged.
- Historical **318 validation episodes** = 11 screening configurations x 18 + 4 confirmation configurations x 30. Stored summaries recompute exactly. These are dependent comparisons over shared seeds, not 318 independent worlds.
- Historical **54 resource probes** = 42 resource calls + 6 adversarial + 6 corrected process-tree payload calls. Earlier launcher-only measurements are not full-process RSS.
- All four mandatory 18-episode benchmark files recompute under the official summarizer. Selected greedy and supplied greedy have identical actions/outcomes. The untouched result remains **3 versus 16** qualifying outcomes, selected versus protected RAVEN, over 18 episodes per arm.
- **540 small-instance pruning comparisons** replay exactly in portfolios, values, and regrets, excluding timings/allocations. They cover 36 underlying states with repeated budgets/shortlists. Zero regret in some small cases gives no guarantee about arbitrary states or actual MSMI.
- Training/validation row seeds match their declarations, are disjoint from each other and all reporting/test seeds, and have pre-action day <60 and matured day 100. Original model and selected configuration bytes are unchanged.

## Defects found and fixed

| Defect | Before | Fix | Regression evidence | Deployed decision effect |
| --- | --- | --- | --- | --- |
| Duplicate undirected research edges | Last duplicate could replace weight 10 with 2, selecting total 6 instead of 10 | Preserve maximum integer weight | `HardeningMatching.test_reversed_duplicate_weights` | None: V1 uses official greedy |
| Research pruning stale requirements | Shortlist could invent an absent question | Ignore requirement groups not contained in candidate set | `HardeningPortfolio.test_shortlist_never_invents_candidates` | None: V1 does not prune |
| Zero-example research training | Empty 1-D design matrix raised IndexError | Recover declared feature width and neutral smoothed prior | `HardeningProbabilities.test_fitting_empty_single_class_and_imbalance` | None: no retraining/assets changed |

The first new suite had these three genuine defects and one incorrect test expectation (two unused members were legitimately still available). `results/hardening/initial_regressions.json` retains the distinction. An audit replay comparison initially compared Python tuples with JSON lists; JSON normalization corrected the harness, not the research results. Local RSS sampling was also corrected to include child interpreters; original `local/` RSS values measure only the launcher and must not be used as full inference memory. Use `local_resources/` for corrected process-tree probes.

## Independent contract trace

Source abbreviations below point to the verified official commit: [PI: policy interface](https://github.com/RomeoJulietLove/The-Sequential-Matching-Problem/blob/a8e26b35118cfa8e886a02f93984923e43ab64f6/docs/POLICY_INTERFACE.md), [DC: data contract](https://github.com/RomeoJulietLove/The-Sequential-Matching-Problem/blob/a8e26b35118cfa8e886a02f93984923e43ab64f6/docs/DATA_CONTRACT.md), [K: simulator/validator](https://github.com/RomeoJulietLove/The-Sequential-Matching-Problem/blob/a8e26b35118cfa8e886a02f93984923e43ab64f6/kit.py), [E: process/container harness](https://github.com/RomeoJulietLove/The-Sequential-Matching-Problem/blob/a8e26b35118cfa8e886a02f93984923e43ab64f6/evaluate.py).

Test abbreviations: HC = `tests/test_hardening_contract.py`; HP = `tests/test_hardening_protocol.py`; HR = `tests/test_hardening_research.py`. Final test execution evidence is `results/hardening/{final_tests,final_python312}/tests.{json,log}`.

| ID | Official source/requirement | Implementation | Test reference | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| A | PI/E.invoke: one UTF-8 JSON request <=1 MiB | `raven.protocol.main` reads bounded bytes and rejects nonfinite constants | HP empty, exact_input_byte_limit, defensive_malformed | PASS | Actual bytes, exactly 1,048,576-byte requests |
| B | PI request schema; DC complete member fields | `decide(request)` consumes public state/phase; no private state object | HC pool_sizes, hidden_world_changes | PASS | Fixtures derive from `Simulator.observe`; schema-invalid cases labelled defensive |
| C | PI ask output exactly asks,memory | `decide` -> `official_policy.decide` -> `sanitize` | HC budget, seeded_properties | PASS | Official `resolve_asks` accepts emitted batches |
| D | PI match output exactly pairs,memory | Same dispatch to supplied greedy | HC seeded_properties; HP processes | PASS | Official `advance` accepts emitted batches |
| E | DC fields/status; decline remains unknown | `constraints.eligibility`, authoritative available flag | HC unknown_declined, boundaries | PASS | No soft imputation crosses hard gate; no invented mandatory-field defaults |
| F | DC/K.eligibility: reciprocal hard rules, blockers first | Independent `constraints.eligibility` | HC each_hard_rule; existing 4096 mask and 7800 pair differential checks | PASS | Compared to official oracle, valid gender arrays |
| G | PI/K.resolve_asks: 12 daily units, hard=3 soft=1 | `validation.sanitize` | HC budget, guard_rejects | PASS | Every budget 0..12; exact/over-budget candidates |
| H | K.advance: available/new/disjoint/feasible pairs | `sanitize`; official greedy allocation | HC guard, seeded_properties; HR graph oracles | PASS | No assertion of global optimality for deployed greedy |
| I | PI finite JSON memory, reset per episode | Memory ignored; emitted `{}` | HP near_max_memory, memory_roundtrips | PASS | 2-byte memory; arbitrary old finite schemas ignored |
| J | E.validate_response, K action validation | Independent final sanitizer | HC assert_action plus official methods | PASS | IDs, budget, overlap, history independently checked |
| K | PI exact single JSON, no NaN/Infinity | `json.dumps(allow_nan=False)` + newline | All HP byte tests | PASS | stdout only one parsed object, one trailing newline |
| L | PI zero exit, fresh process, stderr diagnostics | `main` catches failures into legal empty action; strict debug mode available | HP injected solver/portfolio failures, process loops | PASS | RuntimeError/TimeoutError/MemoryError yield valid empty action |
| M | PI no entrypoint arguments, assets present | Digest-pinned Dockerfile; `/app`; nonroot | Original CI plus expanded workflow | PASS | Expanded image built cleanly; all six families completed |
| N | E.docker_command: no network, read-only, tmpfs, no mount | Official evaluator unchanged; no inference downloads | Expanded Linux CI | PASS | 744 successful offline invocations; no host mount or runtime download |
| O | PI resource limits and 2 GiB image | Official Docker flags/timeout; bounded stdin/stdout/memory | Expanded Linux CI and instrumented probes | PASS (tested scope) | Max 2.627 s wall, 65.805 MiB process RSS, 117.925 MiB image; empirical tests are not a universal bound |

No additional schema validation is required for malformed requests by the official contract. Valid observations include all mandatory fields. Unicode is exercised in opaque zone/pool labels; official member IDs are restricted to `syn_` plus 32 hexadecimal characters. They are never synthesized by the policy. Historical asks may legally be repeated across batches or asked after being answered/declined; only duplicate member/field requests within a batch are forbidden. Availability already includes busy/pause status. Follow-up days are advanced without policy invocations by the official harness.

## Adversarial coverage index

The item IDs below refer to the numbered cases in the task. PASS means the stated implemented scope has executed successfully. NOT TESTED identifies an unavailable guarantee or a concept absent from this implementation. The fixture builder uses the real public generator and `observe()`, with coherent field/status/day updates for constructed states. Seeded enumeration is reproducible property testing without a new Hypothesis dependency.

| Requested cases | Test/evidence | Result and qualification |
| --- | --- | --- |
| 3A.1-7 | HC pool_sizes_and_graph_extremes | PASS: zero/one/two/multiple, unknown/disconnected/complete |
| 3A.8,14,18 | HP exact_input_byte_limit; near_max_memory; HC boundaries | PASS: exactly 1 MiB, dense and all-unknown members, age bounds |
| 3A.9-12 | HP long_real_feedback_history; HC boundaries; simulator states | PASS: absent optional missing_reason, null fields/member_id/propensity, empty and >100-event history |
| 3A.13,15-16 | HP memory_roundtrips, near_max_memory | PASS: fresh processes and carried/reset JSON |
| 3A.17 | HC boundaries_and_unknown_soft | PASS for Unicode labels; Unicode member IDs are outside the documented schema |
| 3A.19-26 | All HP invokes | PASS: raw UTF-8, strict parsing, exact keys, zero actions, finite/bounded output, exit 0 |
| 3A.27-30 | HP invoke uses absolute entrypoint, fresh empty cwd, minimal environment; Docker allowlist and `/app` metadata | PASS locally and on Linux; no Windows paths, absent optional environment dependency or writable persistence |
| 3B.1-14 | HC each_hard_rule, unknown_declined, boundaries; existing Constraints | PASS: both directions, all eleven hard fields, blocker priority and combinations |
| 3B.15-20 | HC unknown_declined, guard_rejects, seeded_properties | PASS: disclose unlock/block, no unknown/incompatible/repeat/busy introduction |
| 3C.1-7,12-17 | HC budget, guard_rejects; HR Portfolio | PASS: official budget/type checks and research portfolios |
| 3C.8-11 | HC budget_and_official_repeat_semantics | PASS: official repeat semantics distinguished from planner avoidance |
| 3C.18-19,22 | Existing Graphs joint_vs_singleton; HR complementary | PASS: complementarity, ties, zero improvement |
| 3C.20-21 | HR complementary low values; probability extremes | PASS for finite surrogate/probabilities; no stochastic answer-distribution optimizer exists |
| 3C.23-24 | HP near_max_memory; HR shortlist; research feature tests | PASS: stale memory ignored; missing estimates have trained defaults |
| 3C.25 | HP research_failures | PASS: forced optimizer failure returns official legal empty ask action |
| 3D.1-18 | HR Matching graph families, brute-force, finite weights; HC graph extremes | PASS: integer-weight exact research oracle; greedy behavior checked separately |
| 3D.19-20 | HR reversed_duplicate_weights | PASS after research fix |
| 3D.21-24 | HC guard_rejects, high_predictions, seeded_properties | PASS: history/availability/eligibility enforced independently of scores |
| 3D.25 | HP exact_input_byte_limit; HR oversize fallback | PASS for payload-fitting dense observations; no fixed member-count maximum exists |
| 3D.26-28 | HP research_failures; HR oversize fallback | PASS: injected timeout exception/failure and oversized greedy fallback; no claim of preempting a hung solver in-process |
| 3E.1-5,7-17,23-26 | HC seeded_properties (18 episodes x 120 decisions), public_feedback_lifecycle_fixtures, hidden_world_changes; HP long history | PASS for observed simulator trajectories and coherent public timelines (pending, one/both yes, both no, missing response, late date, pending second response, pause) |
| 3E.6 | HC guard_rejects advances 40 days before checking history | PASS for supported availability changes; no assumption all members return |
| 3E.18-22 | HP near_max_memory and roundtrips; defensive malformed | PASS: memory empty/old/stale/large; invalid JSON explicitly defensive |
| 3F.1-5,10 | HR fitting_empty_single_class_and_imbalance | PASS in full suite; training dependency absent in portable 3.12 run |
| 3F.6-9,14-18 | HR cold_start, immutable_model | PASS: missing/declined/unseen, extreme logits, finite clipped probabilities |
| 3F.11-13,19-21 | HR directional_joint_labels_and_pre_action_features; existing temporal tests | PASS: recorded-event directional/joint targets, late/censored/absent events not converted to preference labels; no unobserved-pair calibration claim |
| 3F.22 | hardening_preflight split_audit | PASS: declared pool/seed separation; files unchanged; no held-out refit |
| 3G.1-17,20-23 | HR Portfolio independent_subset_oracle and complementary tests | PASS: finite utility, exact affordable subsets, deterministic ties, cap, nonnegative regret |
| 3G.18 | HR shortlist_never_invents_candidates | PASS after stale-requirement fix |
| 3G.19,24 | Replayed 540 rows; original experiment/report | PASS: exhaustive only on tractable candidates; explicit surrogate versus actual MSMI |
| 3H.1-24 | Expanded workflow, hardening_run and Linux resource wrapper | PASS for tested scope: clean credential-free build, offline limits, all assets, six families, dense/near-limit states, determinism, image/time/process-RSS limits |
| 3H.25 | HP exact bytes; local and container invocation records | PASS: 1 MiB request, 27,064-byte maximum response, 2-byte memory, zero diagnostics |

Exact matching optimizes rounded integer edge weights (scale 1e9), and uses greedy beyond 220 nodes or 6000 edges. It does not promise exact real-valued optimality below quantization resolution or for oversized graphs. The fallback tests inject exceptions; only the external official timeout handles a genuinely hung process. Output validity after an actual 10-second process timeout is not claimed.

## Invariants and limits of proof

| Invariant | Result | Basis |
| --- | --- | --- |
| P1 valid JSON | PASS | Raw byte parsing and finite serialization |
| P2 hard eligible | PASS | Official eligibility oracle on every tested introduction |
| P3 disjoint members | PASS | Independent used-ID check and official atomic validator |
| P4 budget | PASS | Cost sum and official resolve_asks |
| P5 supported field | PASS | Official named-field whitelist |
| P6 no repeated pair | PASS | Unordered history comparison and official advance |
| P7 availability | PASS | Current observed flags; no hidden availability inference |
| P8 unknown blocks | PASS | Exhaustive missingness masks and decline tests |
| P9 no hidden/future inputs | PASS | Process boundary, observed fixtures, hidden-world perturbation, pre-action feature audit |
| P10 memory bound | PASS | Always `{}`, independently measured as 2 bytes |
| P11 deterministic | PASS | Repeated processes, controlled hash seeds, equal action hashes |
| P12 all private valid states within resources | NOT TESTED | Universal private-state guarantee cannot be proved by finite public testing. All tested local and Docker states pass. |

## Reproduction

From repository root (commands write new output directories; choose a new suffix for repeats):

```sh
python -m pip install -r requirements-dev.txt
python scripts/hardening_run.py --output results/hardening/replay
python scripts/hardening_run.py --output results/hardening/compatibility --stdlib --tests-only
docker build --no-cache --pull -t sequential-policy:submission .
python scripts/hardening_run.py --output results/hardening/docker_replay --image sequential-policy:submission --skip-tests
python scripts/hardening_container_resources.py sequential-policy:submission results/hardening/docker_resources_replay.json
python scripts/compare_runs.py results/hardening/replay/episodes.json results/hardening/docker_replay/episodes.json
```

Inference has no pip dependencies, network access, GPU, external asset retrieval or build credentials. The full development requirements are for tests/research only. Docker's allowlist copies policy sources, trained assets and licences; public dataset/world files, experiments, reports and local caches are excluded. The base image is pinned by digest. The expanded workflow used an empty Docker credential configuration. No forced push, repository replacement, selected-policy tuning, hidden-world access or official submission message occurred in this audit.
