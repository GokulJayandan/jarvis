# Team Jarvis — RAVEN-Match

Recoverability-Aware Vertex Elicitation and Sequential Allocation, for Round 2 of
[The Sequential Matching Problem](https://github.com/RomeoJulietLove/The-Sequential-Matching-Problem).
All profiles and outcomes are synthetic, not real-world relationship validation.

The implementation combines strict reciprocal feasibility, separate confirmed and
recoverable potential graphs, outcome prediction, complementary clarification
portfolios and general-graph matching. Public validation selects the final policy;
the simpler official baseline remains eligible for selection.

**Container verification is blocked because Docker is absent on this host.**
Check the actual gates before calling this submission-ready. Nothing has been
published to GitHub or submitted to the organizers by this build process.

## Run

Python 3.10+ for inference; local experiments use 3.14.6. No pip runtime dependencies.

```text
python policy.py < observation.json
python -m unittest -v
python verify_data.py
python evaluate.py --seeds 101,102,103 --variants all --output results/final.json
```

The executable reads one JSON request and writes one JSON action. It is offline,
CPU-only and uses current input, frozen assets and explicit memory (empty here).
Diagnostics go to stderr. No private world or inferred hidden constraint authorizes
a match. Official evaluator, simulator, tests, data and validators are unchanged.

Reproduce the original baselines after installing our adapter:

```text
python evaluate.py --policy official_policy.py --baseline greedy --seeds 101,102,103 --variants all --output results/greedy.json
python evaluate.py --policy official_policy.py --baseline no_asks --seeds 101,102,103 --variants all --output results/no_asks.json
python evaluate.py --policy official_policy.py --baseline random --seeds 101,102,103 --variants all --output results/random.json
```

The official evaluator always passes `--baseline greedy` to a custom default policy.
Use preserved `official_policy.py` for an unambiguous official greedy run.

## Evidence

* [Technical report](report/TECHNICAL_REPORT.md) and [machine-readable tables](results/report_tables.json).
* [Raw results](results/) and [reproducibility commands](docs/REPRODUCIBILITY.md).
* [Contract audit](docs/CONTRACT_AUDIT.md), [methods](docs/METHODS.md), [model card](docs/MODEL_CARD.md).
* [Automated self-review](docs/INDEPENDENT_REVIEW.md) and [submission gates](docs/SUBMISSION_CHECKLIST.md).
* [Experiment protocol](docs/EXPERIMENT_PROTOCOL.md) and [seed registry](configs/seeds.json).

Training uses eighteen independent public seeds across six families. Six separate
validation seeds calibrate models, and two select the configuration. Inference seed
17 applies to the random-question ablation; optimizers use stable deterministic
ordering. Held-out reporting seeds are not used for tuning.

```text
python -m pip install -r requirements-dev.txt
python -m experiments.train
python -m experiments.run_ablations
python -m experiments.run_pruning
python -m experiments.run_calibration
python -m experiments.run_future_value
python -m experiments.run_robustness
python -m experiments.generate_figures
python -m experiments.generate_report
```

## Container

```text
docker build -t sequential-policy:submission .
python evaluate.py --image sequential-policy:submission --seeds 101 --output results/container_check.json
```

These commands were attempted but could not pass without Docker installed. The
failed container result is retained. Its presence is not proof of success. The
Dockerfile packages all inference assets using the official Python 3.12.7 base;
offline execution, image size and enforced limits still need verification.

## Attribution and team

Upstream release 1.0.0, commit `a8e26b35118cfa8e886a02f93984923e43ab64f6`.
Notices remain in [LICENSE](LICENSE) and [DATA_LICENSE.md](DATA_LICENSE.md).
NetworkX blossom retains BSD-3-Clause notices. See [provenance](docs/UPSTREAM_PROVENANCE.md)
and [licences](docs/LICENSES.md). New Team Jarvis work remains owned by its authors;
participation does not itself grant a commercial licence. OpenAI Codex assisted
implementation and automated review.

GokulJayandan R S · Keerthana Janakiraman · Mridula B · Boomika L.

The optional website has not been started; mandatory evidence takes priority.
Publication and official issue submission require explicit authorization.
