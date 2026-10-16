# Performance gap: measured diagnosis

The original difference is one qualifying pair across 18 episodes. {'n_episodes': 18, 'n_seed_clusters': 3, 'mean_difference': -0.027777777777777776, 'ci95': [-0.16666666666666666, 0.08333333333333333], 'method': 'paired seed-cluster percentile bootstrap; six equally weighted families; descriptive with few clusters'}
This sample cannot identify a single causal root cause. The following assessments separate directly supported observations from hypotheses.

| Hypothesis | Diagnostic and evidence | Conclusion |
| --- | --- | --- |
| H1: wasted questions | Original ask units: 10,368 versus 3,720; observation replay separates hard/soft asks; V5 removes soft asks on new validation. | Supported for excess cost; causal MSMI harm inconclusive. |
| H2: optimistic portfolio utility | Daily predicted surrogate gains and realized feasible-edge changes are recorded in observation_diagnostics.json. They are different quantities and cannot be equated. | Inconclusive: no unbiased counterfactual portfolio outcome oracle. |
| H3: pruning loses useful opportunities | 540 exact small comparisons; only 3/108 at limit 12 remove candidates; production probes n=17; V9 changes screening on full validation episodes. | Inconclusive for full-state MSMI attribution; small-state surrogate loss measured. |
| H4: poor outcome ranking | V4 pooled prior versus V5 calibrated no-soft; V2/V3 isolate official question/match components. See screen JSON. | Inconclusive. Calibration alone cannot establish ranking quality; sparse controlled outcome evidence reported. |
| H5: acceptance versus MSMI mismatch | Directional Brier improves; MSMI pooled prior has slightly better held-out Brier, only six positives. | Supported as calibration limitation; not proof of score-gap causation. |
| H6: future/wait deferral | Protected selected config has future_weight=0 and waiting_weight=0. | Unsupported for the reported score gap. |
| H7: exact matching with weak weights | A_greedy_weighted changes only matching algorithm; V3 changes weights and algorithm to official baseline. | Inconclusive; paired validation does not justify a blanket claim that exact optimization is worse. |
| H8: insufficient introductions | Original RAVEN: 1,444 introductions/1,351 served; greedy: 1,437/1,338. | Unsupported as an aggregate coverage deficit. |
| H9: proxy not primary outcome | All selections and reporting use official MSMI; planning surrogate lacks proven relationship to realized MSMI. | Inconclusive: proxy mismatch remains a risk, not demonstrated causality. |
| H10: rare-event variation | Original paired difference -0.02778; descriptive CI [-0.16666666666666666, 0.08333333333333333]. | Compatible with variation; neither superiority nor inferiority established. |

## Per-seed matched table

| Scenario | Seed | Greedy MSMI | RAVEN MSMI | Delta | Greedy dates | RAVEN dates | Date delta | Greedy ask cost | RAVEN ask cost | Coverage delta | Wait delta days |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| development | 101 | 1 | 1 | 0 | 15 | 12 | -3 | 198 | 547 | 0.005 | -0.346774 |
| development | 102 | 1 | 1 | 0 | 9 | 10 | 1 | 195 | 538 | 0.005 | -0.117736 |
| development | 103 | 1 | 0 | -1 | 6 | 5 | -1 | 207 | 610 | 0 | -0.872093 |
| sparse | 101 | 0 | 0 | 0 | 3 | 4 | 1 | 192 | 534 | 0 | -2.71429 |
| sparse | 102 | 1 | 0 | -1 | 8 | 3 | -5 | 189 | 525 | 0 | -1.97297 |
| sparse | 103 | 0 | 0 | 0 | 1 | 1 | 0 | 207 | 574 | 0 | -1.2 |
| cold_start | 101 | 1 | 1 | 0 | 14 | 13 | -1 | 246 | 642 | 0.025 | 0.132434 |
| cold_start | 102 | 0 | 0 | 0 | 5 | 3 | -2 | 249 | 687 | 0.015 | 1.13925 |
| cold_start | 103 | 0 | 1 | 1 | 4 | 5 | 1 | 237 | 661 | -0.005 | -1.95198 |
| delayed | 101 | 2 | 2 | 0 | 16 | 15 | -1 | 198 | 546 | 0 | -0.67033 |
| delayed | 102 | 0 | 2 | 2 | 9 | 17 | 8 | 195 | 502 | -0.005 | -1.11894 |
| delayed | 103 | 1 | 1 | 0 | 7 | 6 | -1 | 207 | 603 | 0.005 | -0.87606 |
| shift | 101 | 1 | 1 | 0 | 17 | 13 | -4 | 198 | 550 | 0.005 | -0.580879 |
| shift | 102 | 1 | 1 | 0 | 7 | 15 | 8 | 195 | 544 | 0.005 | 0.249473 |
| shift | 103 | 1 | 0 | -1 | 6 | 3 | -3 | 207 | 610 | 0 | -0.337209 |
| drift | 101 | 1 | 1 | 0 | 13 | 9 | -4 | 198 | 547 | 0.005 | -0.454301 |
| drift | 102 | 1 | 1 | 0 | 9 | 9 | 0 | 195 | 538 | 0.005 | -0.117736 |
| drift | 103 | 1 | 0 | -1 | 6 | 5 | -1 | 207 | 610 | 0 | -0.872093 |

## Original observed outcome funnel

| Policy | Introductions | Mutual acceptances | Dates | MSMI | Dates / mutual acceptances | MSMI / dates |
| --- | --- | --- | --- | --- | --- | --- |
| greedy | 1437 | 198 | 155 | 14 | 0.782828 | 0.0903226 |
| final | 1444 | 204 | 148 | 13 | 0.72549 | 0.0878378 |

These ratios are conditional on different selected pairs and cannot isolate a stage-specific causal mechanism. RAVEN has more recorded mutual acceptances but fewer completed meetings; an acceptance model alone does not optimize the final target.

## Controlled screening differences against frozen RAVEN

| Variant | MSMI/100 delta | 95% descriptive interval | Seed clusters |
| --- | --- | --- | --- |
| A_future | 0.166667 | [0.0, 0.25] | 3 |
| A_greedy_weighted | -0.111111 | [-0.3333333333333333, 0.0] | 3 |
| A_uncalibrated | -0.0277778 | [-0.08333333333333333, 0.0] | 3 |
| V1_greedy | 0.0555556 | [-0.16666666666666666, 0.4166666666666667] | 3 |
| V2_greedy_asks | 0.0833333 | [-0.4166666666666667, 0.3333333333333333] | 3 |
| V3_greedy_matches | 0.194444 | [-0.08333333333333333, 0.4166666666666667] | 3 |
| V4_prior | 0.333333 | [0.08333333333333333, 0.5833333333333334] | 3 |
| V5_present | 0.25 | [-0.08333333333333333, 0.4166666666666667] | 3 |
| V8_endpoint | 0.25 | [-0.08333333333333333, 0.6666666666666666] | 3 |
| V9_reduced | 0.222222 | [-0.08333333333333333, 0.4166666666666667] | 3 |

Waiting is conditional on receiving an introduction. All timings are descriptive under concurrent execution. No latent preference, future arrival or hidden propensity was provided to a policy. Missing feedback occurrence dates are excluded from delay means, with counts retained.
