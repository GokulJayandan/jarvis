# Recovery release evidence

Team Jarvis — RAVEN-Match. **Final hardening and Docker checks passed:** [GitHub Actions run 39042745485](https://github.com/GokulJayandan/jarvis/actions/runs/39042745485) passed 93 tests, a clean image build, all six container scenarios, local/container action-and-outcome equality, and Linux boundary/resource probes at public commit `66874ac68ea8ab030a92e0a5b1f3542cffc1a411`. The original run 38919907335 remains baseline evidence. Full scope and limits are recorded in `docs/FINAL_HARDENING_AUDIT.md`. Form-complete issue preparation tooling is ready; the immutable final-SHA package has not been posted. This is an executed local recovery, not a claim of private performance.

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

The earlier local Docker attempts failed because Docker was absent; those failure records remain unchanged as historical evidence. The original CI run 38919907335 later cleared the build gate for one development episode. Expanded [CI run 39042745485](https://github.com/GokulJayandan/jarvis/actions/runs/39042745485) then passed all six seed-101 scenario families with zero invalid episodes and exact local/container actions and outcomes. Across 744 calls there were no timeouts; the maximum observed wall time was 2.577 seconds. Instrumented Linux boundary probes measured a 65.805 MiB process high-water RSS, and the Linux amd64 image was 117.925 MiB. These public tests do not guarantee every private state. Full commands, hashes, measurements and qualifications are in `docs/FINAL_HARDENING_AUDIT.md`. No website work or official issue submission was performed.

Recovery found and corrected a memory-measurement defect: Windows virtual-environment Python uses a launcher and child interpreter, while the historical sampler measured only the launcher PID. The original RSS claims can therefore underestimate total memory. All current release resource measurements sum the launcher and recursive descendants, which may double-count shared pages. The preliminary launcher-only near-limit file is retained as `max_payload.json`; the corrected file is `max_payload_process_tree.json`. Inference code was not changed by this measurement correction.

## Reproduction and provenance

Use Python 3.14 with `requirements-dev.txt` for research, or the pinned Python 3.12.7 Docker image for inference. Inference has no pip dependencies, network, GPU or persistent filesystem state. Official MIT source and synthetic-data notices, vendored BSD matching notices and all model provenance remain included. OpenAI Codex assisted implementation and automated review; no human independent review is claimed.

Use the report-generation instructions in `docs/CI_VALIDATION.md` and the evaluation commands in `docs/RECOVERY_REPRODUCIBILITY.md`. The preserved generators describe pre-CI status; apply the documented release prose patch after regeneration. The historical verifier writes pre-CI gate snapshots and should only be rerun in a disposable audit copy. New run scripts refuse to overwrite search evidence. To repeat the full search, use a clean checkout with a different result root. The protected original candidate is tagged `recovery/pre-competitive-recovery` at `a918583473afbb0bc70abe76f1266c39331bf97b`.


---

# Historical RAVEN research study (protected pre-recovery candidate)

All references to the selected or frozen soft policy in the following historical sections describe the protected original candidate, not the current release configuration above. Original results and figures are preserved unchanged. Docker/publication blockers mentioned in the historical text below describe the original pre-CI review, not current status; they are superseded by the successful CI and publication evidence above.

# RAVEN-Match — Recoverability-Aware Vertex Elicitation and Sequential Allocation

Team Jarvis: GokulJayandan R S, Keerthana Janakiraman, Mridula B, Boomika L.
Round 2, synthetic Sequential Matching Problem. Generated from stored experiment files.

## 1. Abstract

The frozen selected configuration is **soft**. Its official public score is **0.3611 MSMI per 100 arrived members**. Official greedy scored 0.3889; the frozen policy does not demonstrate an improvement on the mandatory test sample. We investigate joint clarification, candidate pruning and persistent future information value. Hard eligibility is enforced independently of estimates. Results concern invented simulator outcomes only. At the original study date Docker was absent on the Windows host. That historical blocker was subsequently cleared for the released V1_greedy by verified Linux CI; see the current release audit above.

## 2. Problem definition

At each day the policy selects immediate clarifications within 12 units, then allocates available confirmed-feasible pairs. A qualifying outcome requires a date within 30 days and two Yes second-meeting reports within three days of that date. The primary outcome is pair-level MSMI / arrived members × 100. Sixty decision days are followed by forty days with no introductions. Unserved and departed members remain in the denominator.

## 3. Research questions

Does joint elicitation recover complementary opportunities? Does a training-derived future-arrival term improve fresh episodes? How much surrogate utility does screening discard? Do calibrated observable-feature predictions outperform pooled frequencies on held-out selected pairs?

## 4. Related work and references

Global allocation uses Edmonds-style blossom/primal-dual matching via NetworkX 3.6.1 (BSD-3-Clause). See [NetworkX matching source](https://github.com/networkx/networkx/blob/networkx-3.6.1/networkx/algorithms/matching.py) and its reference to Galil (1986). Our portfolio objective is a bounded heuristic, with no submodularity or approximation guarantee. The authoritative benchmark is [official release source](https://github.com/RomeoJulietLove/The-Sequential-Matching-Problem/tree/a8e26b35118cfa8e886a02f93984923e43ab64f6).

## 5. Official data and evaluation setup

Upstream commit: `a8e26b35118cfa8e886a02f93984923e43ab64f6`, release 1.0.0. Training rollouts: 108 episodes, 8163 selected introductions. Calibration-validation rollouts: 36 episodes, 2662 introductions. Sources: `results/training/{observations,validation_observations}.json`; seed registry: `configs/seeds.json`. Six manifest training pools, two validation and two development-test pools remain separate. Static day-30 fields are never used as day-zero features. Official evaluator and simulator source are unchanged. Private worlds were not accessed or generated.

## 6. Feasibility and hard constraints

The independent checker enforces reciprocal age, explicit gender preferences, zone, smoking and existing-children restrictions; relationship structures must agree, explicit yes/no children-plan conflicts fail, and schedules must overlap. All hard values must be known. Known failure takes priority over missingness. Same member, cross-pool and underage pairs fail. Availability and prior introductions are separate filters. Tests exhaust all 2^11 missing-field masks at each endpoint and compare thousands of randomized public profiles with `kit.eligibility`.

## 7. Two-graph architecture

Confirmed edges alone reach `allocate`. Potential edges represent pairs with unresolved recoverable hard constraints. Declined hard fields are excluded from the recoverable planning subgraph. Explicit edge types and an output sanitizer prevent potential-edge allocation. The official simulator performs the final independent atomic action validation.

## 8. Probability and disclosure modelling

Four regularized logistic targets estimate recorded directional Yes, joint Yes, a completed date and qualifying MSMI directly. Pair predictions are symmetric; directional probabilities are not multiplied. Pooled Jeffreys estimates are a real ablation. The 35 features include soft agreement, disagreement, separate endpoint missingness, refusal/not-asked fractions, current day and age gap. Validation-only intercept calibration is regularized. Labels are collected after day 100. Missing responses are zero only for explicitly recorded-event targets; they are never labelled as negative personal preferences. Selection bias remains because only introduced pairs have outcomes. Disclosure follows exact official status semantics: non-declined requests disclose immediately; declined values remain unavailable.

## 9. Joint clarification objective

For question set Q, `U(Q) = V_greedy(C ∪ P_unlocked(Q)) + λ Σ L_i(t)`. Potential edge weight is predicted MSMI times empirical-Bayes feasibility after revelation. An edge becomes available to this surrogate only when every required endpoint bundle is selected. Cost is a hard constraint (3 per bundle, daily budget 12); ties prefer fewer questions. This allocates expected edge weights and is not exact expected post-answer matching utility. No unknown or sampled edge is ever introduced.

## 10. Portfolio search and pruning

Production screens candidates by incident opportunity and preserves high-value complementary endpoint groups, then enumerates up to four bundles within a fixed work cap. The full-episode unpruned comparator has a 2,000-portfolio cap and is approximate. The separate small-state oracle is exhaustive and exact for the declared surrogate. P1 random valid bundles, P2 endpoint, P3 singleton VOI and joint portfolios are genuinely different implementations.

## 11. Persistent future-arrival value

The future term uses training-observed arrival counts after day t, zone frequencies, pooled reciprocal feasibility and MSMI priors, a bounded survival discount and remaining horizon. It sees no actual future members. Coefficients 0, 0.5 and 2 are evaluated on validation seeds. The approximation omits detailed future competition and individual dropout risk. It becomes zero after the latest training-supported arrival day.

## 12. Matching optimization

Confirmed weights are predicted qualifying-event probabilities, optionally plus a waiting term. Exact general-graph matching uses the vendored NetworkX blossom body with integer-scaled weights. A minimal adapter avoids importing NetworkX at inference. Brute-force small-graph checks, odd cycles and larger NetworkX differential tests validate the adapter. Greedy matching is a configuration ablation. No exponential matching routine is used on full states.

## 13. Official baselines

| Policy | Valid episodes | MSMI pairs | Arrived members | Official score | Mean coverage |
| --- | --- | --- | --- | --- | --- |
| greedy | 18 | 14 | 3600 | 0.3889 | 0.3717 |
| no_asks | 18 | 5 | 3600 | 0.1389 | 0.1428 |
| random | 18 | 10 | 3600 | 0.2778 | 0.3767 |
| final | 18 | 13 | 3600 | 0.3611 | 0.3753 |

Sources: `results/{greedy,no_asks,random,final}.json`. Every required arm uses seeds 101,102,103 across all six families. Baselines were executed before replacing the starter entrypoint; `official_policy.py` reproduces them afterward. Scores average family means equally, not pooled family denominators.

## 14. Experimental protocol

See `docs/EXPERIMENT_PROTOCOL.md`. Models are fit on training data, intercepts calibrated on validation, and configurations selected on the two manifest validation seeds. The configuration is frozen in `raven/assets/final_config.json` before final reporting. Validation and research use the unchanged `evaluate.episode` with a labelled in-process JSON adapter; mandatory final/baseline runs use actual subprocesses. In-process runtime is not comparable to container or subprocess runtime. Multiple candidate selection and few independent seeds require caution. All attempted runs and negative results remain available.

## 15. Overall and scenario-level results

| Policy | Family | n | Arrived | Introductions | Mutual Yes | Dates | MSMI | MSMI/100 | Coverage | Ask units | Missing feedback |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| greedy | development | 3 | 600 | 299 | 39 | 30 | 3 | 0.5000 | 0.4317 | 600 | 180 |
| greedy | sparse | 3 | 600 | 53 | 14 | 12 | 1 | 0.1667 | 0.1450 | 588 | 25 |
| greedy | cold_start | 3 | 600 | 195 | 28 | 23 | 1 | 0.1667 | 0.3600 | 732 | 91 |
| greedy | delayed | 3 | 600 | 289 | 41 | 32 | 3 | 0.5000 | 0.4300 | 600 | 166 |
| greedy | shift | 3 | 600 | 299 | 39 | 30 | 3 | 0.5000 | 0.4317 | 600 | 176 |
| greedy | drift | 3 | 600 | 302 | 37 | 28 | 3 | 0.5000 | 0.4317 | 600 | 181 |
| no_asks | development | 3 | 600 | 97 | 13 | 10 | 1 | 0.1667 | 0.1833 | 0 | 54 |
| no_asks | sparse | 3 | 600 | 16 | 3 | 3 | 0 | 0.0000 | 0.0433 | 0 | 6 |
| no_asks | cold_start | 3 | 600 | 33 | 7 | 5 | 0 | 0.0000 | 0.0800 | 0 | 14 |
| no_asks | delayed | 3 | 600 | 97 | 15 | 10 | 2 | 0.3333 | 0.1833 | 0 | 57 |
| no_asks | shift | 3 | 600 | 98 | 12 | 10 | 1 | 0.1667 | 0.1833 | 0 | 55 |
| no_asks | drift | 3 | 600 | 97 | 13 | 10 | 1 | 0.1667 | 0.1833 | 0 | 54 |
| random | development | 3 | 600 | 303 | 39 | 33 | 2 | 0.3333 | 0.4400 | 600 | 164 |
| random | sparse | 3 | 600 | 53 | 13 | 11 | 1 | 0.1667 | 0.1450 | 588 | 25 |
| random | cold_start | 3 | 600 | 195 | 27 | 25 | 1 | 0.1667 | 0.3633 | 732 | 95 |
| random | delayed | 3 | 600 | 294 | 41 | 31 | 1 | 0.1667 | 0.4383 | 600 | 150 |
| random | shift | 3 | 600 | 301 | 35 | 27 | 3 | 0.5000 | 0.4333 | 600 | 156 |
| random | drift | 3 | 600 | 303 | 37 | 31 | 2 | 0.3333 | 0.4400 | 600 | 164 |
| final | development | 3 | 600 | 302 | 43 | 27 | 2 | 0.3333 | 0.4350 | 1695 | 157 |
| final | sparse | 3 | 600 | 53 | 9 | 8 | 0 | 0.0000 | 0.1450 | 1633 | 24 |
| final | cold_start | 3 | 600 | 206 | 27 | 21 | 2 | 0.3333 | 0.3717 | 1990 | 92 |
| final | delayed | 3 | 600 | 276 | 46 | 38 | 5 | 0.8333 | 0.4300 | 1651 | 145 |
| final | shift | 3 | 600 | 297 | 40 | 31 | 2 | 0.3333 | 0.4350 | 1704 | 161 |
| final | drift | 3 | 600 | 310 | 39 | 23 | 2 | 0.3333 | 0.4350 | 1695 | 158 |

Counts are summed within each row; coverage and MSMI/100 are episode means. Source files are the same as Section 13. A zero MSMI count is a measured zero in a rare-event pipeline and does not establish policy equivalence.

Paired final-minus-baseline differences (MSMI/100; seed-cluster percentile bootstrap):

| Baseline | Episodes | Seed clusters | Difference | 95% interval |
| --- | --- | --- | --- | --- |
| greedy | 18 | 3 | -0.0278 | [-0.1667, 0.0833] |
| no_asks | 18 | 3 | 0.2222 | [0.0833, 0.4167] |
| random | 18 | 3 | 0.0833 | [-0.0833, 0.25] |

Three clusters give coarse, descriptive intervals; no private-leaderboard inference is justified.

Additional frozen-policy test runs (official engine, in-process adapter):

| Source | Episodes | All valid | MSMI/100 |
| --- | --- | --- | --- |
| results/raven/manifest_test.json | 12 | True | 0.2083 |
| results/raven/fresh_test.json | 12 | True | 0.3750 |

## 16. Future-value ablation

Fresh-seed future-minus-present result: {"n_episodes": 18, "n_seed_clusters": 3, "mean_difference": 0.3333333333333333, "ci95": [0.0, 0.5], "method": "paired seed-cluster percentile bootstrap; six equally weighted families; descriptive with few clusters"}

Coverage effect: {"n_episodes": 18, "n_seed_clusters": 3, "mean_difference": 0.0005555555555555561, "ci95": [0.0, 0.001666666666666668], "method": "paired seed-cluster percentile bootstrap; six equally weighted families; descriptive with few clusters"}; clarification-cost effect: {"n_episodes": 18, "n_seed_clusters": 3, "mean_difference": 5.944444444444445, "ci95": [-0.6666666666666666, 14.833333333333334], "method": "paired seed-cluster percentile bootstrap; six equally weighted families; descriptive with few clusters"}. Sources: `results/future/{present,future,paired}.json`. The interval includes zero; these runs do not establish a stable improvement.

The earlier joint-only policy comparison is retained separately at `results/future_joint_reference/`: {"n_episodes": 18, "n_seed_clusters": 3, "mean_difference": 0.2222222222222222, "ci95": [-0.08333333333333333, 0.4166666666666667], "method": "paired seed-cluster percentile bootstrap; six equally weighted families; descriptive with few clusters"}. The main comparison above holds the selected soft-question configuration fixed and changes only the future coefficient. Neither fresh comparison changes the frozen choice.

## 17. Pruning regret

| Limit | Cases | Mean regret | Max regret | P(utility loss) | P(tied chosen optimum excluded) | Mean ms |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 108 | 0.0002 | 0.0035 | 0.2963 | 0.2963 | 0.0239 |
| 4 | 108 | 0.0001 | 0.0018 | 0.1111 | 0.1111 | 0.0464 |
| 6 | 108 | 0.0000 | 0.0018 | 0.0278 | 0.0278 | 0.1067 |
| 8 | 108 | 0.0000 | 0.0003 | 0.0093 | 0.0093 | 0.1867 |
| 12 | 108 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.3998 |

Source: `results/pruning/regret.json`. All 540 comparisons use exact enumeration of the declared surrogate. Repeated candidate limits/budgets on one state are dependent. Excluding a particular tied optimum need not lose utility; both events are reported. Relative regret is null when the optimum is zero. This is not measured MSMI regret.

## 18. Calibration by disclosure strata

| Target | Model | Disclosure stratum | n | Events | Brier | Log loss | ECE |
| --- | --- | --- | --- | --- | --- | --- | --- |
| directional | prior | all | 960 | 356 | 0.2335 | 0.6598 | 0.0144 |
| directional | prior | fully_observed_soft | 183 | 65 | 0.2290 | 0.6506 | 0.0012 |
| directional | prior | declined_soft | 338 | 95 | 0.2077 | 0.6068 | 0.0754 |
| directional | prior | not_asked_soft | 439 | 196 | 0.2552 | 0.7045 | 0.0900 |
| directional | logistic | all | 960 | 356 | 0.2243 | 0.6405 | 0.0785 |
| directional | logistic | fully_observed_soft | 183 | 65 | 0.2022 | 0.5946 | 0.1220 |
| directional | logistic | declined_soft | 338 | 95 | 0.2066 | 0.6042 | 0.1308 |
| directional | logistic | not_asked_soft | 439 | 196 | 0.2471 | 0.6874 | 0.1424 |
| directional | logistic calibrated | all | 960 | 356 | 0.2244 | 0.6407 | 0.0785 |
| directional | logistic calibrated | fully_observed_soft | 183 | 65 | 0.2022 | 0.5947 | 0.1226 |
| directional | logistic calibrated | declined_soft | 338 | 95 | 0.2062 | 0.6032 | 0.1307 |
| directional | logistic calibrated | not_asked_soft | 439 | 196 | 0.2477 | 0.6887 | 0.1438 |
| joint | prior | all | 960 | 147 | 0.1298 | 0.4284 | 0.0094 |
| joint | prior | fully_observed_soft | 183 | 27 | 0.1258 | 0.4185 | 0.0038 |
| joint | prior | declined_soft | 338 | 31 | 0.0860 | 0.3188 | 0.0520 |
| joint | prior | not_asked_soft | 439 | 89 | 0.1651 | 0.5170 | 0.0590 |
| joint | logistic | all | 960 | 147 | 0.1258 | 0.4139 | 0.0501 |
| joint | logistic | fully_observed_soft | 183 | 27 | 0.1127 | 0.3668 | 0.1079 |
| joint | logistic | declined_soft | 338 | 31 | 0.0860 | 0.3184 | 0.0666 |
| joint | logistic | not_asked_soft | 439 | 89 | 0.1618 | 0.5071 | 0.1043 |
| joint | logistic calibrated | all | 960 | 147 | 0.1256 | 0.4134 | 0.0480 |
| joint | logistic calibrated | fully_observed_soft | 183 | 27 | 0.1125 | 0.3669 | 0.1098 |
| joint | logistic calibrated | declined_soft | 338 | 31 | 0.0868 | 0.3213 | 0.0676 |
| joint | logistic calibrated | not_asked_soft | 439 | 89 | 0.1608 | 0.5036 | 0.1012 |
| date | prior | all | 960 | 109 | 0.1007 | 0.3539 | 0.0003 |
| date | prior | fully_observed_soft | 183 | 17 | 0.0847 | 0.3114 | 0.0203 |
| date | prior | declined_soft | 338 | 21 | 0.0609 | 0.2480 | 0.0511 |
| date | prior | not_asked_soft | 439 | 71 | 0.1379 | 0.4530 | 0.0485 |
| date | logistic | all | 960 | 109 | 0.1000 | 0.3501 | 0.0407 |
| date | logistic | fully_observed_soft | 183 | 17 | 0.0838 | 0.3015 | 0.0868 |
| date | logistic | declined_soft | 338 | 21 | 0.0603 | 0.2448 | 0.0469 |
| date | logistic | not_asked_soft | 439 | 71 | 0.1373 | 0.4514 | 0.0862 |
| date | logistic calibrated | all | 960 | 109 | 0.1000 | 0.3501 | 0.0414 |
| date | logistic calibrated | fully_observed_soft | 183 | 17 | 0.0845 | 0.3040 | 0.0931 |
| date | logistic calibrated | declined_soft | 338 | 21 | 0.0612 | 0.2489 | 0.0521 |
| date | logistic calibrated | not_asked_soft | 439 | 71 | 0.1364 | 0.4472 | 0.0841 |
| msmi | prior | all | 960 | 6 | 0.0062 | 0.0395 | 0.0054 |
| msmi | prior | fully_observed_soft | 183 | 0 | 0.0001 | 0.0117 | 0.0117 |
| msmi | prior | declined_soft | 338 | 3 | 0.0088 | 0.0511 | 0.0028 |
| msmi | prior | not_asked_soft | 439 | 3 | 0.0068 | 0.0421 | 0.0048 |
| msmi | logistic | all | 960 | 6 | 0.0063 | 0.0397 | 0.0153 |
| msmi | logistic | fully_observed_soft | 183 | 0 | 0.0003 | 0.0137 | 0.0136 |
| msmi | logistic | declined_soft | 338 | 3 | 0.0088 | 0.0508 | 0.0168 |
| msmi | logistic | not_asked_soft | 439 | 3 | 0.0068 | 0.0419 | 0.0155 |
| msmi | logistic calibrated | all | 960 | 6 | 0.0062 | 0.0391 | 0.0140 |
| msmi | logistic calibrated | fully_observed_soft | 183 | 0 | 0.0002 | 0.0118 | 0.0117 |
| msmi | logistic calibrated | declined_soft | 338 | 3 | 0.0088 | 0.0507 | 0.0158 |
| msmi | logistic calibrated | not_asked_soft | 439 | 3 | 0.0068 | 0.0414 | 0.0143 |

Source: `results/calibration/metrics.json`, fresh seeds 13001–13002. Calibration is evaluated after fitting and frozen selection; this diagnostic does not retune the model. Reliability uses equal-frequency bins. Wilson bin intervals ignore within-world dependence and are descriptive. No unselected-pair calibration claim is made. Deterministic disclosure strata: {"observed": {"n": 57, "brier": 0.0}, "not_asked": {"n": 195, "brier": 0.0}, "declined": {"n": 12, "brier": 0.0}}. Gate-feasibility calibration: {"n": 3852, "brier": 0.09165583073457843, "log_loss": 0.3116802038378811, "ece": 0.00951409437033929}. Directional calibrated Brier is 0.22438 versus pooled 0.23352. MSMI calibrated Brier is 0.00625 versus pooled 0.00624, based on only 6 events. Calibration does not improve every target or metric; the table retains negative evidence. No parameters were changed after these held-out diagnostics.

## 19. Coverage and waiting

| Policy | Served person-episodes | Unserved person-episodes | Mean wait days | Median wait days | Max wait days |
| --- | --- | --- | --- | --- | --- |
| greedy | 1338 | 2262 | 6.4477 | 4.0 | 51 |
| no_asks | 514 | 3086 | 4.1732 | 0.0 | 53 |
| random | 1356 | 2244 | 6.5361 | 5.0 | 58 |
| final | 1351 | 2249 | 5.8919 | 4 | 59 |

Waiting is conditional on receiving an introduction, so low mean wait can coexist with poor coverage. Unserved members have no observed first-introduction time. Sources: the four official result JSONs. No demographic fairness claim is made.

## 20. Runtime and reliability

Final test command exit code: 0. Source: `results/execution/final_tests.{json,log}`. 48 measured subprocess calls, including dense adversarial fixtures; maximum 4.1848 s, maximum sampled RSS 30.48 MiB; maximum request 569876 bytes, response 8025 bytes. Sources: `results/robustness/{resources,adversarial}.json`. RSS is sampled, not a guaranteed peak. These Windows measurements do not establish Docker-enforced limits. Docker build could not launch (executable missing), and official container evaluation exited 2. `results/container_check.json` is a failed check, not a successful benchmark. A portable Windows Python 3.12.7 run passed 53 standard-library compatibility tests (`results/execution/python312_compat.log`); this is not Linux/container verification. No runtime exceptions may be hidden during final evaluation: `RAVEN_STRICT=1` turns development fallback errors into failing subprocesses. Production fallback emits diagnostics to stderr and legal empty actions.

## 21. Additional ablations

| Configuration | MSMI/100 | Coverage | Ask units/episode | In-process seconds/episode |
| --- | --- | --- | --- | --- |
| official_greedy | 0.3750 | 0.2921 | 195.0000 | 6.9989 |
| joint | 0.5000 | 0.2971 | 187.5000 | 5.1712 |
| future | 0.3750 | 0.2954 | 194.7500 | 2.9963 |
| future_high | 0.3333 | 0.2954 | 194.7500 | 2.9095 |
| prior | 0.5833 | 0.2942 | 187.5000 | 3.5399 |
| uncalibrated | 0.5000 | 0.2971 | 187.5000 | 3.5432 |
| greedy_match | 0.4167 | 0.2950 | 187.5000 | 3.3819 |
| singleton | 0.5000 | 0.2954 | 180.0000 | 3.0789 |
| endpoint | 0.0833 | 0.2975 | 188.5000 | 2.9846 |
| random_questions | 0.0833 | 0.2971 | 195.0000 | 1.1903 |
| soft | 0.6667 | 0.2946 | 535.4167 | 3.6894 |
| unpruned | 0.2500 | 0.2971 | 188.2500 | 4.7787 |
| waiting | 0.5000 | 0.2975 | 187.5000 | 4.1000 |

Each configuration uses the same two validation seeds across all six families (12 episodes). Sources: `results/ablations/*.json`, selection record `results/selection.json`. Future changes λ only; calibration and prior variants change prediction; singleton/endpoint/random change clarification; greedy_match changes allocation; soft enables soft questions; waiting adds waiting utility. The unpruned arm removes screening but retains a work cap, so its reference is approximate. Multiple-testing risk applies to choosing the largest score.

## 22. Failure cases

See `docs/FAILURE_ANALYSIS.md`. Sparse supply, hard refusals, occupied members, overlapping opportunities and late feedback can prevent qualifying outcomes. Expected-edge-weight clarification ignores joint answer dependence. Learned probabilities have selective feedback, rare-event uncertainty and shift risk. At the original study checkpoint, container validation was unresolved. Expanded Linux CI subsequently passed for the released policy; finite public tests still do not prove private validity.

## 23. Limitations

This is synthetic evaluation, not social or clinical validation. Few independent seeds limit uncertainty estimates. Model selection reuses validation for calibration/configuration choice and compares several candidates. No held-out retuning is allowed. The future term is pooled and heuristic; the pruning oracle concerns small states and an approximate objective. Memory is intentionally empty because histories are cumulative; models do not adapt to evaluation feedback. No website is part of this submission. Historical Docker failures are superseded by the verified Linux CI evidence in the current release audit.

## 24. Reproducibility

See `README.md`, `docs/REPRODUCIBILITY.md`, `configs/seeds.json`, pinned experiment dependencies, source fingerprints and execution logs. Generate figures with `python -m experiments.generate_figures` and this report with `python -m experiments.generate_report`. Inference is standard-library Python with a vendored solver and read-only JSON assets. There are no runtime APIs, GPUs or persistent files. The local measured interpreter is Python 3.14.6; the Dockerfile specifies Python 3.12.7, which expanded Linux CI verified for the released container.

## 25. Software, data, model and AI provenance

Official MIT source and synthetic-data conditions are preserved. Vendored NetworkX retains BSD notices. Exact file and asset hashes: `results/provenance.json`. See `docs/{UPSTREAM_PROVENANCE,LICENSES,MODEL_CARD}.md`. New Team Jarvis work remains owned by its authors. OpenAI Codex assisted implementation and automated review. No human independent-review claim is made. Other teams’ source code was not used. No private organiser seeds or hidden state enter inference.

## 26. Conclusion

The historical public-validation configuration was soft and measured 0.3611 MSMI/100. The released V1_greedy policy and its 0.3889 MSMI/100 mandatory comparison are documented in the recovery sections above, together with the negative untouched result. Offline Docker verification and immutable source publication have passed; the official issue remains unposted.
