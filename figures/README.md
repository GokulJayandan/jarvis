# Reproducible experiment figures

Generate with `python -m experiments.generate_figures`.

[01_baseline_comparison](01_baseline_comparison.png) — Equal weighting of six families; three matched seeds per family. Low event counts limit inference. Sources: `results/greedy.json`, `results/no_asks.json`, `results/random.json`, `results/final.json`.

[02_scenarios](02_scenarios.png) — Public families and matched seeds; zero MSMI is an observed zero, not evidence of equivalence. Sources: `results/greedy.json`, `results/no_asks.json`, `results/random.json`, `results/final.json`.

[03_outcome_funnel](03_outcome_funnel.png) — Each point is an official full episode; overlapping points are possible. Sources: `results/greedy.json`, `results/no_asks.json`, `results/random.json`, `results/final.json`.

[04_coverage](04_coverage.png) — Includes unserved members in the denominator; not a fairness certification. Sources: `results/greedy.json`, `results/no_asks.json`, `results/random.json`, `results/final.json`.

[05_waiting](05_waiting.png) — Conditional on being served. Unserved counts are reported separately in the report. Sources: `results/greedy.json`, `results/no_asks.json`, `results/random.json`, `results/final.json`.

[11_clarification](11_clarification.png) — Hard bundle costs 3; soft question costs 1. Maximum 720 units per episode. Sources: `results/greedy.json`, `results/no_asks.json`, `results/random.json`, `results/final.json`.

[06_future_effect](06_future_effect.png) — Paired full episodes; intervals and seed-cluster limitations appear in the report. Sources: `results/future/present.json`, `results/future/future.json`.

[07_pruning_regret](07_pruning_regret.png) — Regret is against exact portfolio enumeration of the same surrogate, not actual MSMI. Sources: `results/pruning/regret.json`.

[08_pruning_runtime](08_pruning_runtime.png) — Python wall-clock search only; oracle peak allocations and runtime are recorded in raw data. Sources: `results/pruning/regret.json`.

[09_reliability](09_reliability.png) — Held-out baseline-selected pairs; equal-frequency bins. Pair dependence and selection bias remain. Sources: `results/calibration/metrics.json`.

[10_disclosure_calibration](10_disclosure_calibration.png) — Strata concern observed soft-field status at decision time; lower Brier is better. Sources: `results/calibration/metrics.json`.

[12_runtime](12_runtime.png) — Includes startup, protocol IO and dense adversarial states. Not a container resource-enforcement result. Sources: `results/robustness/resources.json`, `results/robustness/adversarial.json`.
