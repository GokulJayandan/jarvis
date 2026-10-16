# Structured automated recovery review

This is a coding-agent self-review, not an independent human review. The
machine-readable `results/recovery/quality_gates.json` is the preserved pre-CI
snapshot. Current documented status is in `SUBMISSION_CHECKLIST.md` and
`CI_VALIDATION.md`; experimental evidence files are unchanged.

| Review | Severity | Evidence and issue | Action | Remaining risk |
| --- | --- | --- | --- | --- |
| A: official contract | High | Upstream main and public rules unchanged; policy baseline dispatch previously bypassed the independent guard | All backend outputs now pass the existing sanitizer; full-episode guarded-baseline equivalence test added | Public tests cannot prove private validity |
| B: algorithms | High | Question and matching effects were confounded in the original aggregate comparison | Added official-question/RAVEN-match and RAVEN-question/official-match switches; all introductions remain confirmed feasible | Trajectories diverge; no causal counterfactual label for unchosen pairs |
| B: pruning | Medium | 540 comparisons could be mistaken for 540 independent states; only 3/108 at limit 12 remove candidates | Replayed all 540; verified exact counts and identical results; disclosed 36 states and conditional production probes | Zero-regret evidence at the production limit is weak; surrogate regret is not MSMI regret; large states not solved exhaustively |
| C: statistics | High | Original selection used two seeds and 13 policies, with rare events | Predeclared new screening, five-seed confirmation, untouched reporting and conservative selection rule | Low power, search selection and unadjusted intervals remain; no superiority guarantee |
| C: labels | High | Feedback may have no occurrence date; selective introduction labels | Fixed diagnostic delay extraction to count missing dates separately; recomputed all calibration strata and historical paired effects | Calibration covers selected pairs, not all opportunities; Wilson bins ignore world dependence |
| D: generalization | High | One-pair old score gap is weak evidence | Matched six-family screening/confirmation and post-freeze fresh populations; original files preserved | Private worlds and real relationship outcomes remain untested |
| D: selection failure on untouched sample | High | Selected guarded greedy obtained 3 MSMI versus protected RAVEN's 16 over 18 episodes each | Report the negative result prominently; preserve predeclared freeze and all candidate evidence | The conservative selection rule did not identify the strongest policy on this sample; no claim of improved generalization |
| E: engineering | High | Existing evidence must survive recovery unchanged | Local recovery tag; versioned result paths; original action/outcome replay; final source and staged-byte hashes | Linux CI now passed at the published tested commit; one container episode does not guarantee private validity |
| E: RAM measurement | High | Historical sampler omitted the child interpreter spawned by the Windows venv launcher | Verified launcher/child process tree; corrected sampling to sum recursive descendant RSS and reran final probes | Sampling can miss peaks and double-count shared pages; old launcher-only RAM claims are underestimates |
| E: container | Resolved for tested scope | CI run 38919907335 built the actual Dockerfile and completed official image evaluation, exit 0 | Downloaded and hash-verified logs; exact subprocess/container equivalence; 117.925 MiB image; network/resource restrictions applied | One development episode only; no separate peak-memory telemetry or private-world guarantee |
| F: publication | Pending authorization | Tested commit `98c5440dba6a2780f2ffd766c4f576fd796c4abb` is public; SHA-pinned report/results match Git bytes | Prepare documentation-only revision and current-template issue draft | New documentation commit awaits authorized push; official issue requires separate approval |

The inference changes are deliberately narrow: two experimental backend switches
and routing the existing official baseline branch through the sanitizer. The
selected configuration changes only after validation completes. Official
`kit.py`, `evaluate.py`, data, validators and baseline implementation remain
byte-identical to the protected candidate. No final reporting observation is used
to alter coefficients or configuration.

The first recovery diagnostic crashed when subtracting a missing occurrence day.
It was an analysis-script failure, not a policy failure. Its log remains in
`results/execution/recovery_diagnostics.*`; the corrected replay is separately
logged as `recovery_diagnostics_retry.*`. This distinction is retained in the
release evidence rather than suppressing the failure.
