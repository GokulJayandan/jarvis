# Model card — synthetic outcomes only

Recovery note: this card describes the preserved research predictor. Whether the
deployed policy uses it is specified in `results/recovery/release_selection.json`.
The model itself is not refitted during recovery. Current inference checksums are
in `results/recovery/frozen_source.json`; older provenance is historical.

Purpose: rank currently legal synthetic introductions and score clarification
opportunities. Never a real-member compatibility, clinical, or social predictor.

Assets: `raven/assets/model.json`, `raven/assets/final_config.json`. Exact checksums
are recorded in `results/provenance.json` and each experiment's source fingerprint.
No downloaded pretrained model or external dataset. Training is CPU only.

Training: `python -m experiments.train`; declared training seeds in
`configs/seeds.json`. All six scenario families; greedy/random baseline actions.
Only pre-action JSON-observable features are attached to each selected introduction.
Labels are observed after day 100, with the official qualifying-window definition.
Day-30 static profiles are not attached retrospectively to earlier introductions.

Targets: directional recorded Yes; joint recorded Yes; completed date; qualifying
mutual second-meeting intention. These are recorded events, not latent preference
labels. Direct pair models avoid multiplying dependent directional probabilities.
Thirty-five features encode soft agreement/disagreement, endpoint missingness,
declined/not-asked fractions, current day and age difference. Ridge strength 20;
validation-only intercept calibration regularized with strength 20. The empirical
prior ablation uses Jeffreys smoothing. Features exclude IDs, world seeds, future
arrivals, latent traits and simulator random-state reconstruction.

Gate model: empirical-Bayes conditional eligibility rates from real legal ask
transitions, shrinkage 20. Disclosure itself follows exact deterministic official
semantics. Gate predictions can guide asks only; they cannot authorize a match.

Selection and calibration populations are distinct from final and fresh tests.
Across variants, common seeds may share identities and must stay in the same split.
Held-out calibration uses baseline-selected introductions, with counts and missing
strata explicitly reported. No inverse-propensity claim is made: propensities are
unknown. Rare MSMI events give substantial uncertainty even with many assignments.

Online feedback is not used to refit weights. This keeps inference small and avoids
right-censoring mistakes, at the cost of adaptation. Models are JSON, read-only,
finite and bundled in the image. Inference writes no files and makes no network calls.
