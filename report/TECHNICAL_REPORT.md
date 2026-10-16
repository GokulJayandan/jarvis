# RAVEN-Match — Recoverability-Aware Vertex Elicitation and Sequential Allocation

Team Jarvis: GokulJayandan R S, Keerthana Janakiraman, Mridula B, Boomika L.
Round 2, synthetic Sequential Matching Problem. Generated from stored experiment files.

## 1. Abstract

The frozen selected configuration is **soft**. Its official public score is **0.3611 MSMI per 100 arrived members**. Official greedy scored 0.3889; the frozen policy does not demonstrate an improvement on the mandatory test sample. We investigate joint clarification, candidate pruning and persistent future information value. Hard eligibility is enforced independently of estimates. Results concern invented simulator outcomes only. Docker execution is blocked on this host; this build must not be represented as submission-ready until that gate passes.

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

See `docs/FAILURE_ANALYSIS.md`. Sparse supply, hard refusals, occupied members, overlapping opportunities and late feedback can prevent qualifying outcomes. Expected-edge-weight clarification ignores joint answer dependence. Learned probabilities have selective feedback, rare-event uncertainty and shift risk. Container validation is an actual unresolved blocker. Unit-test success does not prove private validity.

## 23. Limitations

This is synthetic evaluation, not social or clinical validation. Few independent seeds limit uncertainty estimates. Model selection reuses validation for calibration/configuration choice and compares several candidates. No held-out retuning is allowed. The future term is pooled and heuristic; the pruning oracle concerns small states and an approximate objective. Memory is intentionally empty because histories are cumulative; models do not adapt to evaluation feedback. The optional website was not started because mandatory Docker verification remains blocked.

## 24. Reproducibility

See `README.md`, `docs/REPRODUCIBILITY.md`, `configs/seeds.json`, pinned experiment dependencies, source fingerprints and execution logs. Generate figures with `python -m experiments.generate_figures` and this report with `python -m experiments.generate_report`. Inference is standard-library Python with a vendored solver and read-only JSON assets. There are no runtime APIs, GPUs or persistent files. The local measured interpreter is Python 3.14.6; the Dockerfile specifies Python 3.12.7, which requires actual container verification.

## 25. Software, data, model and AI provenance

Official MIT source and synthetic-data conditions are preserved. Vendored NetworkX retains BSD notices. Exact file and asset hashes: `results/provenance.json`. See `docs/{UPSTREAM_PROVENANCE,LICENSES,MODEL_CARD}.md`. New Team Jarvis work remains owned by its authors. OpenAI Codex assisted implementation and automated review. No human independent-review claim is made. Other teams’ source code was not used. No private organiser seeds or hidden state enter inference.

## 26. Conclusion

The selected public-validation configuration is soft; measured final score is 0.3611 MSMI/100. The report preserves both positive and negative evidence. Local implementation and public evaluation must be distinguished from submission completion. A working offline Docker run and authorized publication of an immutable commit remain necessary before official submission.
