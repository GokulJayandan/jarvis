# Predeclared experiment protocol

`configs/seeds.json` is the seed registry. Six manifest training pools plus twelve
fresh training seeds are used across all six public families. Features are saved
before actions and labels only after 60 decision + 40 follow-up days. Six validation
seeds calibrate model intercepts; the two manifest validation seeds select among
predeclared policy variants. The final 101–103 seeds, 13001–13005 fresh tests and
two manifest test pools are not used for fitting or selection.

The same seed across variants shares population structure, so uncertainty resamples
seed clusters jointly across all families. With two or three clusters, intervals
are descriptive and coarse; low event counts and selection among thirteen policies
limit power. No significance or superiority claim is inferred from a point estimate.

P0 official greedy, P1 random valid bundles, P2 potential-edge endpoints, P3 singleton
VOI, P4 joint portfolios, P5 pruned portfolios, P6 future-aware portfolios are
implemented via configuration. Full-episode unpruned search has a deterministic cap;
only tractable small-state portfolio searches are called exact. Primary outcome is
the unmodified official `evaluate.summarise` score, not the planning surrogate.

Validation ablations use `evaluate.episode` with an explicitly labelled in-process
adapter that preserves strict JSON response validation and simulator validation.
This reduces process-start overhead for research; it is not Docker validation.
Mandatory baseline and final commands use the actual official subprocess runner.
Runtime across these modes is not directly comparable. Jobs may overlap on this
development machine; final resource figures identify their measurement method.

Hypotheses: future value improves fresh-pool outcomes; pruning saves compute with
limited surrogate regret; calibrated probabilities improve held-out calibration;
joint questions recover complementary endpoints better than singleton VOI; exact
matching improves global allocation; soft questions may improve pair choice at a
budget cost. Negative results are retained. Configuration is frozen before final
and fresh test reporting. Final metrics do not trigger retuning.
The fresh future-value comparison holds every selected final-policy component
fixed and overrides only its future coefficient (0 versus 0.5). Overrides are
recorded in the in-process experiment metadata; inference source is not changed.
An earlier joint-only future comparison is retained in `results/future_joint_reference`.
The selected-policy comparison was added to isolate the coefficient on the actual
selected soft-question policy. Neither comparison is used to reselect or retune.

The pruning study crosses seeds, 12/24/36-member states, three disclosure/geography
families, budgets 3/6/12, and candidate limits 2/4/6/8/12. Cases with no useful
questions remain in results, with undefined relative regret represented by null.
These measurements concern the explicit surrogate, not actual downstream MSMI.
