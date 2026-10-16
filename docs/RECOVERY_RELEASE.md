# Recovery release evidence

Team Jarvis — RAVEN-Match. **Docker and source-publication checks passed:** [GitHub Actions run 38919907335](https://github.com/GokulJayandan/jarvis/actions/runs/38919907335) successfully built and evaluated the policy container at public commit `98c5440dba6a2780f2ffd766c4f576fd796c4abb`. The official submission issue has not been created; it requires separate authorization. This documentation revision also awaits authorization to push. This is an executed local recovery, not a claim of private performance.

**Important negative result:** the untouched post-freeze sample favored protected RAVEN over the selected conservative policy: 16 versus 3 qualifying outcomes over 18 episodes each. The selection rule did not identify the stronger policy on this sample. The choice remains frozen to avoid selecting on the held-out results; no claim of improved generalization or statistically optimal policy selection is made.

## Selected release algorithm

Selected configuration: **V1_greedy**. Official greedy clarification and soft-agreement greedy matching, wrapped in RAVEN independent hard-eligibility, budget, duplicate and availability validation. Learned probabilities, portfolio search and future terms are not used by the selected policy. Advanced RAVEN modules are evaluated research alternatives, not decision components of the deployed V1_greedy policy. Exact settings are in `results/recovery/release_selection.json`.

Selection used newly declared public validation seeds only: screening [22001, 22002, 22003]; confirmation [22101, 22102, 22103, 22104, 22105]. The predeclared rule requires a custom finalist's paired interval against greedy to exclude zero; otherwise select guarded greedy. V6 aliases V0 and V7 aliases V1 and were not counted as separate algorithms. These intervals use only five seed clusters, are descriptive, and are not multiplicity-adjusted. No superiority guarantee follows.

Original 101–103 reporting results were already known during recovery, so the repeated benchmark is a reproducibility comparison, not a newly untouched test. Seeds [22201, 22202, 22203] were untouched until selection and source freeze. No outcome from those seeds changed the configuration. Original training and model bytes were preserved. The original 13-policy study remains historical evidence.

## Mandatory official subprocess benchmark

Each row has 18 episodes, six families × three matched seeds, 60 decision days + 40 follow-up days. MSMI counts are qualifying pairs; arrivals are members. The score is the unchanged official equal-family average. Evidence: `results/recovery/{greedy,no_asks,random,final}.json`.

| Policy | Valid/episodes | MSMI | Arrivals | MSMI/100 | Meetings | Coverage | Ask units/episode |
| --- | --- | --- | --- | --- | --- | --- | --- |
| greedy | 18/18 | 14 | 3600 | 0.388889 | 155 | 0.371667 | 206.667 |
| no_asks | 18/18 | 5 | 3600 | 0.138889 | 48 | 0.142778 | 0 |
| random | 18/18 | 10 | 3600 | 0.277778 | 158 | 0.376667 | 206.667 |
| final | 18/18 | 14 | 3600 | 0.388889 | 155 | 0.371667 | 206.667 |

| Scenario | Episodes | Arrivals | MSMI | MSMI/100 | Meetings | Coverage | Ask units/episode |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cold_start | 3 | 600 | 1 | 0.166667 | 23 | 0.36 | 244 |
| delayed | 3 | 600 | 3 | 0.5 | 32 | 0.43 | 200 |
| development | 3 | 600 | 3 | 0.5 | 30 | 0.431667 | 200 |
| drift | 3 | 600 | 3 | 0.5 | 28 | 0.431667 | 200 |
| shift | 3 | 600 | 3 | 0.5 | 30 | 0.431667 | 200 |
| sparse | 3 | 600 | 1 | 0.166667 | 12 | 0.145 | 196 |

Zero MSMI means no qualifying observed event in that sample, not an estimated zero success probability. With rare events and three seed clusters, uncertainty is large. Paired differences and descriptive bootstrap intervals are in `results/recovery/report_tables.json`.

## Validation search and confirmation

Screening: 18 episodes per distinct configuration; no final-reporting outcomes used.

| Configuration | MSMI/100 | MSMI count | Coverage | Ask units/episode |
| --- | --- | --- | --- | --- |
| A_future | 0.527778 | 19 | 0.34 | 547.833 |
| A_greedy_weighted | 0.25 | 9 | 0.341111 | 543.611 |
| A_uncalibrated | 0.333333 | 12 | 0.340278 | 542.722 |
| V0_frozen | 0.361111 | 13 | 0.340278 | 542.722 |
| V1_greedy | 0.416667 | 15 | 0.337778 | 194 |
| V2_greedy_asks | 0.444444 | 16 | 0.338889 | 194 |
| V3_greedy_matches | 0.555556 | 20 | 0.338889 | 537.444 |
| V4_prior | 0.694444 | 25 | 0.341667 | 190.667 |
| V5_present | 0.611111 | 22 | 0.341944 | 190.333 |
| V8_endpoint | 0.611111 | 22 | 0.339444 | 192.167 |
| V9_reduced | 0.583333 | 21 | 0.340556 | 190.333 |

Confirmation: 30 episodes per finalist, five new seeds × six families.

| Configuration | MSMI/100 | MSMI count | Coverage | Ask units/episode |
| --- | --- | --- | --- | --- |
| V0_frozen | 0.433333 | 26 | 0.333167 | 565.567 |
| V1_greedy | 0.333333 | 20 | 0.331333 | 203.4 |
| V4_prior | 0.383333 | 23 | 0.335833 | 197.3 |
| V5_present | 0.433333 | 26 | 0.334 | 197.2 |

Selection evidence and paired intervals: `results/recovery/selection.json`. Configuration IDs, exact overrides, source/model hashes and seed declarations are in `configs/recovery.json`, `registered_plan.json`, each run JSON and `frozen_source.json`. In-process validation uses the official engine and action validation, but its runtime is not comparable to container/startup time.

## Untouched post-freeze reporting

| Configuration | Episodes | MSMI count | MSMI/100 | Coverage |
| --- | --- | --- | --- | --- |
| V0_frozen | 18 | 16 | 0.444444 | 0.298333 |
| V1_greedy | 18 | 3 | 0.0833333 | 0.2975 |

Evidence: `results/recovery/fresh/*.json`. These are official-engine in-process episodes, not container evaluation. This small sample does not establish private or real-world generalization.

Selected versus greedy on these untouched seeds: {'n_episodes': 18, 'n_seed_clusters': 3, 'mean_difference': 0.0, 'ci95': [0.0, 0.0], 'method': 'paired seed-cluster percentile bootstrap; six equally weighted families; descriptive with few clusters'}.

Protected RAVEN minus selected release on untouched seeds: {'n_episodes': 18, 'n_seed_clusters': 3, 'mean_difference': 0.3611111111111111, 'ci95': [0.25, 0.5833333333333334], 'method': 'paired seed-cluster percentile bootstrap; six equally weighted families; descriptive with few clusters'}. This is an adverse result for the recovery selection, not evidence to hide behind the repeated 101–103 benchmark. A different selection decision would require a separately declared validation process and another untouched evaluation; no such retuning was performed here.

## Waiting, coverage and feedback

The selected policy served 1338 of 3600 arrivals; 2262 remained unserved. Among served members only, mean first-introduction wait was 6.448 days and median 4.0 days. Unserved members are excluded from this conditional wait statistic and remain in coverage denominators. Missing feedback count was 819; pending records were not labelled as preference failures.

For the original candidate versus greedy, the observation-only diagnostic replays seed 101 in each family. It records every day before and after asks. Feedback delays exclude records with no occurrence day and count those separately.

| Policy | Episodes | Hard asks | Soft asks | New feasible edges summed/day | Unallocated disjoint edges | Predicted MSMI sum | Realized MSMI | Mean feedback delay days | No occurrence date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| greedy | 6 | 410 | 0 | 178 | 0 | 5.71738 | 6 | 0 | 277 |
| frozen | 6 | 399 | 2169 | 191 | 0 | 5.85541 | 6 | 0 | 270 |

Source: `results/recovery/observation_diagnostics.json`. Feasible-edge sums count repeated opportunities on different days and are not distinct people or outcomes. These diagnostic trajectories differ after the first differing action; they do not isolate causal effects.

## Reviewer investigations

Future value: the historical protected soft-policy comparison was +0.3333 MSMI/100, descriptive interval [0, 0.5], over three fresh seed clusters. New screening compares A_future against V0 with all other settings fixed: {'n_episodes': 18, 'n_seed_clusters': 3, 'mean_difference': 0.16666666666666666, 'ci95': [0.0, 0.25], 'method': 'paired seed-cluster percentile bootstrap; six equally weighted families; descriptive with few clusters'}. This replication is validation evidence, not a new held-out claim. Neither coefficient nor policy is chosen from the old reporting seeds. Future-aware value remains a heuristic based on training arrival frequencies, never observed future people. These are research RAVEN ablations; the deployed guarded greedy policy does not use a future term.

| Future-on minus off study | Metric / unit | Mean difference | 95% descriptive interval | Episodes |
| --- | --- | --- | --- | --- |
| historical_soft | msmi_per_100_arrived_members | 0.333333 | [0.0, 0.5] | 18 |
| historical_soft | dates | 1.55556 | [0.3333333333333333, 2.8333333333333335] | 18 |
| historical_soft | coverage | 0.000555556 | [0.0, 0.001666666666666668] | 18 |
| historical_soft | mean_wait_days | 0.102722 | [0.01677047129622104, 0.1781742329742125] | 18 |
| historical_soft | ask_cost | 5.94444 | [-0.6666666666666666, 14.833333333333334] | 18 |
| historical_soft | inference_seconds | -2.37393 | [-2.727483699680306, -1.8530419829767197] | 18 |
| recovery_screen | msmi_per_100_arrived_members | 0.166667 | [0.0, 0.25] | 18 |
| recovery_screen | dates | 1.11111 | [-0.16666666666666666, 1.8333333333333333] | 18 |
| recovery_screen | coverage | -0.000277778 | [-0.001666666666666668, 0.0008333333333333434] | 18 |
| recovery_screen | mean_wait_days | 0.217365 | [-0.11553773024361262, 0.4654424886697903] | 18 |
| recovery_screen | ask_cost | 5.11111 | [2.8333333333333335, 6.833333333333333] | 18 |
| recovery_screen | inference_seconds | -2.98883 | [-4.316596616602813, -2.079330332848864] | 18 |

Mean waiting is conditional on served members and is first computed per episode. Coverage is a fraction; ask cost is units per episode; dates are completed pairs per episode. Runtime is in-process inference seconds per episode under concurrent load. Scenario-specific effects remain available in each paired result file and are not assumed uniform.

| Study | Scenario | Episodes/arm | MSMI/100 delta | Dates/episode delta | Coverage delta | Wait days delta | Ask units delta |
| --- | --- | --- | --- | --- | --- | --- | --- |
| historical_soft | cold_start | 3 | 0.5 | -0.333333 | 0 | 0.613777 | -1 |
| historical_soft | delayed | 3 | 0 | 0.333333 | -0.00166667 | -0.415286 | 12 |
| historical_soft | development | 3 | 0.5 | 4 | 0.00166667 | 0.0632832 | 3.33333 |
| historical_soft | drift | 3 | 0.5 | 3.66667 | 0.00166667 | 0.0632832 | 3.33333 |
| historical_soft | shift | 3 | 0.5 | 1.33333 | 0.00166667 | 0.214858 | 9.66667 |
| historical_soft | sparse | 3 | 0 | 0.333333 | 0 | 0.0764163 | 8.33333 |
| recovery_screen | cold_start | 3 | 0 | 1.33333 | -0.00166667 | 0.39598 | -6.33333 |
| recovery_screen | delayed | 3 | 0.166667 | 1.66667 | 0.00166667 | 0.234476 | 1 |
| recovery_screen | development | 3 | 0.166667 | 1 | 0 | 0.223996 | 2 |
| recovery_screen | drift | 3 | 0.333333 | 1.66667 | 0 | 0.223996 | 2 |
| recovery_screen | shift | 3 | 0.166667 | 1.33333 | 0 | 0.390366 | 6 |
| recovery_screen | sparse | 3 | 0.166667 | -0.333333 | -0.00166667 | -0.164623 | 26 |

Pruning: all 540 stored comparisons were audited for exhaustive combination counts, identical budgets and regret arithmetic. At limit 12, all 108 comparisons had zero measured surrogate regret across 36 underlying small states, but **only 3 of those 108 comparisons actually removed candidates**. This substantially limits the evidence for the production limit. This is neither 540 independent states nor proof of zero actual MSMI loss. Production-observation exact probes: 17, of which 5 removed candidates; these only cover encountered states with at most 16 useful questions. Detailed regret, selected portfolios and runtimes are retained; larger candidate states are not claimed exact.

All 540 cases were also rerun: every portfolio, utility and regret matched exactly (`recovery_pruning_replay.log`). Exclusion of one chosen optimum can leave another tied optimum, so exclusion and positive regret differ. Relative regret is stored per case and undefined when oracle utility is zero. Python allocation peaks are recorded, not total process memory. Runtime averages below use the original study and are not a container speed claim.

| Limit | Comparisons | Positive regret | Chosen optimum excluded | Mean regret | 95th percentile | Max regret | Oracle seconds | Pruned seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 108 | 32 | 32 | 0.000206083 | 0.00133948 | 0.00346374 | 0.00119041 | 2.39324e-05 |
| 4 | 108 | 12 | 12 | 8.20129e-05 | 7.25468e-05 | 0.0018269 | 0.00119041 | 4.63685e-05 |
| 6 | 108 | 3 | 3 | 2.14964e-05 | 0 | 0.00182663 | 0.00119041 | 0.000106667 |
| 8 | 108 | 1 | 1 | 2.66615e-06 | 0 | 0.000287944 | 0.00119041 | 0.000186696 |
| 12 | 108 | 0 | 0 | 0 | 0 | 0 | 0.00119041 | 0.000399806 |

Calibration: all pooled and model scores, including disclosure strata, were recomputed from the saved 960 selected-introduction records. Qualifying MSMI has only six positives; pooled Brier is slightly better than the calibrated model. Better acceptance calibration is not evidence of better MSMI ranking. All-pair calibration and randomized counterfactual ranking remain unmeasured. Disclosure is deterministic under this version's observed status semantics; its zero Brier is a contract check, not learned prediction skill.

| Target | Predictor | Selected pairs | Positives | Brier | Log loss |
| --- | --- | --- | --- | --- | --- |
| directional | prior | 960 | 356 | 0.233523 | 0.659847 |
| directional | logistic | 960 | 356 | 0.22428 | 0.640457 |
| directional | logistic calibrated | 960 | 356 | 0.224381 | 0.640661 |
| joint | prior | 960 | 147 | 0.129766 | 0.428445 |
| joint | logistic | 960 | 147 | 0.125762 | 0.413935 |
| joint | logistic calibrated | 960 | 147 | 0.12555 | 0.413382 |
| date | prior | 960 | 109 | 0.10065 | 0.353857 |
| date | logistic | 960 | 109 | 0.0999812 | 0.350083 |
| date | logistic calibrated | 960 | 109 | 0.100028 | 0.350086 |
| msmi | prior | 960 | 6 | 0.00624029 | 0.0394813 |
| msmi | logistic | 960 | 6 | 0.00626545 | 0.0396558 |
| msmi | logistic calibrated | 960 | 6 | 0.00624641 | 0.0390514 |

| MSMI disclosure stratum | Predictor | Selected pairs | Positives | Brier | ECE |
| --- | --- | --- | --- | --- | --- |
| fully_observed_soft | prior | 183 | 0 | 0.000136137 | 0.0116678 |
| declined_soft | prior | 338 | 3 | 0.00880476 | 0.00279205 |
| not_asked_soft | prior | 439 | 3 | 0.00681038 | 0.00483408 |
| fully_observed_soft | logistic | 183 | 0 | 0.000265166 | 0.0135519 |
| declined_soft | logistic | 338 | 3 | 0.00879955 | 0.0168484 |
| not_asked_soft | logistic | 439 | 3 | 0.00681563 | 0.0154748 |
| fully_observed_soft | logistic calibrated | 183 | 0 | 0.000198684 | 0.0117218 |
| declined_soft | logistic calibrated | 338 | 3 | 0.00879745 | 0.0157631 |
| not_asked_soft | logistic calibrated | 439 | 3 | 0.00680333 | 0.0142999 |

Source: `results/calibration/metrics.json`; predictions were fitted only on training and validation worlds. These selected-introduction records are biased toward the historical policies, with no known propensity correction. Mature recorded-event targets differ from latent preference labels. Pending/missing second-meeting responses are not labelled as negative preferences. Reliability figures retain bin sample sizes and descriptive Wilson intervals that do not account for within-world dependence.

The directional model's gain over the pooled prior must not be attributed solely to calibration: the uncalibrated model has slightly lower directional Brier than the calibrated one. Likewise, the pooled MSMI prior is better on Brier while the calibrated predictor is better on log loss in this sample. Six positives do not establish a uniformly better probability estimator.

## Reliability and resources

Final unit tests and official data verification passed; see `results/execution/recovery_final_tests.*` and `recovery_final_data.*`. The protected soft configuration and unchanged model were replayed for 18 episodes through the recovery dispatcher; every action hash and outcome matches the original file. Separately, `recovery_protected_commit` extracts the protected commit's exact source bytes and executes a matching official subprocess smoke episode; `protected_source_audit.json` records the byte hashes. Baseline replays are compared against original files. New phase-backend and full-episode guarded-baseline equivalence tests exercise the only inference code changes.

There are 54 final subprocess resource probes, including six constructed cases near the 1 MiB request limit. Maximum observed invocation: 2.6728 seconds; sampled RSS: 54.629 MiB; request: 1047909 bytes; response: 25065 bytes. These Windows measurements are sampled, may miss peaks, and do not verify enforced container CPU/RAM limits. Stress episodes and adversarial dense/unresolved/declined observations use legal-action checks. Each resource invocation rejects unexpected stderr rather than allowing an exception fallback to hide a failure.

The earlier local Docker attempts failed because Docker was absent; those failure records remain unchanged. They are superseded for the current policy by [successful CI run 38919907335](https://github.com/GokulJayandan/jarvis/actions/runs/38919907335) on public commit `98c5440dba6a2780f2ffd766c4f576fd796c4abb`. The actual Docker build and official container evaluator both exited 0. The development episode with seed 101 was valid (0 invalid episodes out of 1), and its actions and outcomes exactly matched subprocess evaluation. The Linux amd64 image measured 123,653,457 bytes (117.925 MiB), below the 2 GiB limit. The official evaluator applied network-disabled execution, 2 CPUs, 1 GiB RAM, a read-only filesystem and the 10-second per-invocation timeout; no resource-limit failure occurred. This is one container episode, not a six-scenario container benchmark or a private-validity guarantee. Separate peak-RAM telemetry was not collected in CI. Full commands, log hashes, image identity and evidence links are in `docs/CI_VALIDATION.md`. No website work or official issue submission was performed.

Recovery found and corrected a memory-measurement defect: Windows virtual-environment Python uses a launcher and child interpreter, while the historical sampler measured only the launcher PID. The original RSS claims can therefore underestimate total memory. All current release resource measurements sum the launcher and recursive descendants, which may double-count shared pages. The preliminary launcher-only near-limit file is retained as `max_payload.json`; the corrected file is `max_payload_process_tree.json`. Inference code was not changed by this measurement correction.

## Reproduction and provenance

Use Python 3.14 with `requirements-dev.txt` for research, or the pinned Python 3.12.7 Docker image for inference. Inference has no pip dependencies, network, GPU or persistent filesystem state. Official MIT source and synthetic-data notices, vendored BSD matching notices and all model provenance remain included. OpenAI Codex assisted implementation and automated review; no human independent review is claimed.

Use the report-generation instructions in `docs/CI_VALIDATION.md` and the evaluation commands in `docs/RECOVERY_REPRODUCIBILITY.md`. The preserved generators describe pre-CI status; apply the documented release prose patch after regeneration. The historical verifier writes pre-CI gate snapshots and should only be rerun in a disposable audit copy. New run scripts refuse to overwrite search evidence. To repeat the full search, use a clean checkout with a different result root. The protected original candidate is tagged `recovery/pre-competitive-recovery` at `a918583473afbb0bc70abe76f1266c39331bf97b`.
