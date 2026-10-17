# Team Jarvis — RAVEN-Match

Round 2 of [The Sequential Matching Problem](https://github.com/RomeoJulietLove/The-Sequential-Matching-Problem). All profiles and outcomes are synthetic.

Current release configuration: **V1_greedy**. Official greedy clarification and soft-agreement greedy matching, wrapped in RAVEN independent hard-eligibility, budget, duplicate and availability validation. Learned probabilities, portfolio search and future terms are not used by the selected policy. Advanced RAVEN modules are evaluated research alternatives, not decision components of the deployed V1_greedy policy. Exact settings are in `results/recovery/release_selection.json`.

**Docker and source-publication checks passed:** [GitHub Actions run 38919907335](https://github.com/GokulJayandan/jarvis/actions/runs/38919907335) successfully built and evaluated the policy container at public commit `98c5440dba6a2780f2ffd766c4f576fd796c4abb`. Final hardening status, expanded contract tests, release fixes, and current Docker evidence are recorded in `docs/FINAL_HARDENING_AUDIT.md`. The official submission issue is prepared separately and has not been posted.

The repeated official benchmark scores 0.3889 MSMI/100 (14 qualifying pairs / 3600 arrivals). Greedy scores 0.3889; this is not a claim of superiority. Selection used fresh validation; untouched post-freeze results and uncertainty are in the report.

**Negative generalization result:** on the untouched three-seed sample, the selected policy obtained 3 qualifying outcomes versus protected RAVEN's 16 (18 episodes each). The conservative selection rule did not choose the stronger policy on that sample. The configuration was not changed after seeing held-out outcomes.

## Run

Inference uses standard-library Python, no pip runtime dependencies, GPU, network or persistent filesystem state. The Dockerfile pins Python 3.12.7. Local research uses Python 3.14.6 and `requirements-dev.txt`.

```sh
python policy.py < observation.json
python -m unittest -v
python verify_data.py
python evaluate.py --seeds 101,102,103 --variants all --output results/recovery/final.json
python evaluate.py --policy official_policy.py --baseline greedy --seeds 101,102,103 --variants all --output results/recovery/greedy.json
python evaluate.py --policy official_policy.py --baseline no_asks --seeds 101,102,103 --variants all --output results/recovery/no_asks.json
python evaluate.py --policy official_policy.py --baseline random --seeds 101,102,103 --variants all --output results/recovery/random.json
docker build -t sequential-policy:submission .
python evaluate.py --image sequential-policy:submission --seeds 101 --output results/recovery/container_check.json
```

Use a new output path when repeating runs. The official evaluator always passes `--baseline greedy` to its default custom policy; `--policy official_policy.py` unambiguously selects the preserved official baselines. Official evaluator, simulator, data and hard-eligibility semantics are unchanged.

## Evidence and reproduction

- [Current technical report](report/TECHNICAL_REPORT.md), [recovery results](results/recovery/), [release evidence](docs/RECOVERY_RELEASE.md).
- [Root-cause investigation](docs/PERFORMANCE_ROOT_CAUSE.md), [recovery audit](docs/RECOVERY_AUDIT.md), [submission gates](docs/SUBMISSION_CHECKLIST.md).
- [Recovery commands](docs/RECOVERY_REPRODUCIBILITY.md), [original environment/provenance](docs/REPRODUCIBILITY.md), [declared recovery seeds](configs/recovery.json).
- [Historical protected-candidate report](report/TECHNICAL_REPORT_PRE_RECOVERY.md), [original research results](results/), [model card](docs/MODEL_CARD.md).

`results/final.json` and the original figures describe the protected pre-recovery soft policy. Current benchmark evidence is `results/recovery/final.json`; current figures are `figures/recovery/`. Original experiments are preserved, including negative findings. Model training and old selection scripts are historical research tools and must not be run as release-finalization steps.

```sh
python -m pip install -r requirements-dev.txt
python -m experiments.recovery_report
git apply docs/RELEASE_DOCUMENTATION.patch
```

The preserved report generator emits pre-CI release prose; the documentation-only patch above restores the verified CI/publication update without altering generated tables or figures. See [CI evidence and regeneration checks](docs/CI_VALIDATION.md). Run the historical recovery verifier only in a disposable audit copy because it rewrites pre-CI gate snapshots.

The original model uses 18 training seeds, six calibration seeds and two original policy-selection seeds. Recovery uses three new screening seeds, five new confirmation seeds and three untouched reporting seeds. Inference random seed is 17 where an experimental random policy is used. Selection and configuration details are fully recorded; no private organizer worlds were accessed.

[Successful CI run 38919907335](https://github.com/GokulJayandan/jarvis/actions/runs/38919907335) built the actual Dockerfile, completed official container evaluation, verified exact local/container equivalence, checked image size and uploaded diagnostic artifacts. The tested scope is one development episode, seed 101. [CI_VALIDATION.md](docs/CI_VALIDATION.md) records commands, limitations and log hashes. Source publication of the tested commit is verified; this documentation-only revision and official issue submission each require authorization.

## Attribution and team

Upstream release 1.0.0, commit `a8e26b35118cfa8e886a02f93984923e43ab64f6`. [MIT licence](LICENSE), [synthetic data conditions](DATA_LICENSE.md), [upstream provenance](docs/UPSTREAM_PROVENANCE.md), and [dependency notices](docs/LICENSES.md) are retained. The research matcher retains NetworkX BSD-3-Clause notices. No external pretrained models or real member data are used. OpenAI Codex assisted implementation and automated self-review.

Team Jarvis: GokulJayandan R S, Keerthana Janakiraman, Mridula B, Boomika L. No website was built. The original candidate is protected by tag `recovery/pre-competitive-recovery` at `a918583473afbb0bc70abe76f1266c39331bf97b`.
