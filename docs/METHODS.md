# Methods

RAVEN constructs confirmed legal edges and recoverable potential edges from the
current observation. A known blocker excludes an edge. Any missing hard field
excludes it from allocation. Permanently declined hard fields exclude it from
the recoverable planning graph. Pair history and current availability are checked
before scoring and again by a separate output guard.

Four ridge-logistic predictors estimate recorded directional Yes by deadline,
joint Yes, a completed meeting, and qualifying MSMI directly. Pair predictors are
symmetrized. No directional-independence product is used. Missing soft values have
explicit indicators; declined and not-asked fractions are separate. Features use
neither IDs nor world seeds nor future observations. Training duplicates symmetric
pair examples, but splits are by independent world seed, never by row.

Inference reads small JSON coefficients; numpy is used only for training. Model
calibration is a validation-only regularized intercept update. Pooled Jeffreys
priors and uncalibrated logits are ablations. All assignment labels mature through
day 100. A zero recorded-event target does not mean a negative preference. There
is no attempt to estimate second-meeting preferences for pairs without dates.

The gate model is an empirical-Bayes table of confirmed eligibility after legally
asked hard bundles, conditioned on same-zone status, unresolved endpoints and age
gap. It uses observed pre-ask and post-ask profiles, not hidden truths. Sparse cells
shrink toward the pooled training rate with strength 20. It is only a planning
estimate. It never fills in a hard field or authorizes an introduction.

For portfolio Q, define a deterministic surrogate

`U(Q) = greedy_matching_value(confirmed + unlocked_expected_edges(Q)) + future(Q)`.

Each potential edge is unlocked only if **all** its missing endpoint bundles are
in Q. Its weight is predicted MSMI times predicted hard-feasibility probability.
This is an allocation using expected edge weights; it is **not** an unbiased
estimate of expected optimal matching after random answers. Dependence and
alternative matching paths are approximated. We make no approximation guarantee.
Cost is a hard budget constraint; equal-utility ties prefer fewer questions.

Candidate screening retains complete high-value endpoint groups and candidates
with large total incident opportunity. Exhaustive combinations up to four hard
bundles are evaluated within the screened set and a deterministic work cap.
The unpruned full-episode variant also has a work cap and is explicitly approximate.
The separate small-state oracle has no cap and is exact for this surrogate.
It enumerates all undominated hard-bundle questions. Soft questions, already
answered bundles and permanently unrecoverable bundles have zero gain under this
particular surrogate and positive cost, so omission weakly dominates them. This
is not an oracle for a richer objective that values soft-information updates.

Future value uses training-observed arrival counts after the current day, observed
zone frequencies, pooled reciprocal feasibility, pooled MSMI and bounded survival
discount. It is a heuristic for persistent information, not a prediction of actual
future individuals. Its coefficient is tested at 0, 0.5 and 2. No future lists enter
inference. The empirical arrival schedule makes this term zero after the final
training-supported arrival day. It does not assume a private arrival schedule.

Allocation uses BSD-licensed NetworkX blossom with a minimal graph adapter.
Weights are scaled to integers (1e9) for numerical reliability. The algorithm body
is unchanged. Small graphs are checked against enumeration, larger graphs against
installed NetworkX. Greedy allocation is an ablation and oversized-graph safeguard.
The deterministic safeguard uses greedy above 6,000 edges or 220 endpoints. A
19,900-edge development probe took over four seconds for blossom alone, motivating
this conservative reserve for graph construction and process startup.

The policy deliberately keeps empty explicit memory: cumulative feedback, question
history and assignments already arrive in each state. Models are frozen, not
silently updated from censored evaluation outcomes. No persistent files are written.
This is a limitation on adaptation, but avoids feedback-label and cross-episode
state leakage. Observations above 220 members use a deterministic bounded subset;
the official population size is 200. The final policy may instead select the
official greedy baseline if validation favors it; see the selection record.
