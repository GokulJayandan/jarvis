### Team name and size

Team Jarvis — four participants. Project: RAVEN-Match.

### Public source URL and immutable version

Repository: https://github.com/GokulJayandan/jarvis

Full assessed-source commit SHA: `9480e8893c496672fee93dc5e5d69c61e54f6a32`

Immutable source: https://github.com/GokulJayandan/jarvis/tree/9480e8893c496672fee93dc5e5d69c61e54f6a32/

The deployed policy is **V1_greedy**: the supplied greedy clarification and soft-agreement greedy matching decisions, followed by independent hard-eligibility, availability, budget and duplicate-action guards. Learned probabilities, portfolio search, exact weighted matching and future-value models are research alternatives, not active deployed decision components. Final hardening repaired three standalone research edge cases without changing the selected configuration, model assets or deployed decisions.

### Report and results URLs

- Technical report: https://github.com/GokulJayandan/jarvis/blob/9480e8893c496672fee93dc5e5d69c61e54f6a32/report/TECHNICAL_REPORT.md
- Mandatory benchmark, selected policy: https://github.com/GokulJayandan/jarvis/blob/9480e8893c496672fee93dc5e5d69c61e54f6a32/results/recovery/final.json
- Baselines: [greedy](https://github.com/GokulJayandan/jarvis/blob/9480e8893c496672fee93dc5e5d69c61e54f6a32/results/recovery/greedy.json), [no clarification](https://github.com/GokulJayandan/jarvis/blob/9480e8893c496672fee93dc5e5d69c61e54f6a32/results/recovery/no_asks.json), [random feasible](https://github.com/GokulJayandan/jarvis/blob/9480e8893c496672fee93dc5e5d69c61e54f6a32/results/recovery/random.json)
- All research comparisons and ablations: https://github.com/GokulJayandan/jarvis/tree/9480e8893c496672fee93dc5e5d69c61e54f6a32/results/recovery
- Contract, adversarial, reproducibility and deployment audit: https://github.com/GokulJayandan/jarvis/blob/9480e8893c496672fee93dc5e5d69c61e54f6a32/docs/FINAL_HARDENING_AUDIT.md
- Machine-readable hardening evidence: https://github.com/GokulJayandan/jarvis/tree/9480e8893c496672fee93dc5e5d69c61e54f6a32/results/hardening

All these files and inference assets are included in the pinned assessed-source version.

### Build and evaluation commands

```sh
python -m pip install -r requirements-dev.txt
python -m unittest -v
python verify_data.py
python evaluate.py --seeds 101,102,103 --variants all --output results/submission_replay_final.json
python evaluate.py --policy official_policy.py --baseline greedy --seeds 101,102,103 --variants all --output results/submission_replay_greedy.json
python evaluate.py --policy official_policy.py --baseline no_asks --seeds 101,102,103 --variants all --output results/submission_replay_no_asks.json
python evaluate.py --policy official_policy.py --baseline random --seeds 101,102,103 --variants all --output results/submission_replay_random.json
docker build --no-cache --pull -t sequential-policy:submission .
python evaluate.py --image sequential-policy:submission --seeds 101 --variants all --output results/submission_replay_container.json
```

Offline CPU inference uses only the Python standard library and supplied files. No runtime dependency downloads, external services, credentials or GPU are required. The Python 3.12.7-slim base is digest-pinned in Dockerfile. Full research/test dependencies are separately pinned; development CI uses Python 3.14. The official runner enforces 2 CPUs, 1 GiB RAM, 10 seconds including startup, no network, 64 PIDs, read-only files, nonroot user and fresh 64 MiB tmpfs. Input, output, memory and diagnostics each have a 1 MiB limit; the image limit is 2 GiB.

### Assets, licences and tools

- Data: organisers' synthetic public kit, upstream `a8e26b35118cfa8e886a02f93984923e43ab64f6`; all 71 data checksums retained and verified. No private organiser worlds, external personal data or external pretrained model.
- Original code/docs retain the upstream MIT notice and synthetic-data terms in LICENSE and DATA_LICENSE.md. Research matching vendors NetworkX 3.6.1 blossom under BSD-3-Clause; the full notice and provenance are included. Python uses its PSF licence. Development-library notices are in docs/dependency_licenses and docs/LICENSES.md.
- The bundled research model was trained on the declared public training seeds only. Training and calibration records are separated from reporting/test seeds. See configs/seeds.json, configs/recovery.json, docs/UPSTREAM_PROVENANCE.md and the report. Training used CPU/NumPy; no hosted model or GPU is required for reproduction.
- Deployed greedy is deterministic and does not use a random inference seed. Research random-question variants use 17 + day; baseline random choices are declared in official_policy.py. No configuration or model was tuned on the untouched reporting sample.
- OpenAI Codex assisted code, tests, release audits and documentation. Automated self-review is not independent human endorsement.

### Validation and comparisons

- The mandatory comparison contains 18 valid episodes per policy (three matched seeds x all six scenario families) for selected, greedy, no-clarification and random-feasible policies. Selected and greedy both recorded 14 qualifying outcomes over 3,600 arrivals, score 0.388889 MSMI/100. This is a tie, not an improvement.
- Hypothesis-driven ablations, future-value and disclosure-calibration experiments are retained. All 540 tractable pruning comparisons were reproduced; they measure a surrogate, not actual MSMI regret or guarantees for large states.
- 93 Python 3.14 tests pass, including raw-byte JSON, independent official legality checks, matching brute-force oracles, deterministic seeded properties, failure injection and exactly 1 MiB boundary fixtures. Portable Python 3.12 compatibility and Linux Docker results are separately labelled in the audit.
- Successful Docker CI: https://github.com/GokulJayandan/jarvis/actions/runs/39049432462 (tested commit `9480e8893c496672fee93dc5e5d69c61e54f6a32`). The submitted commit has byte-identical complete Docker build inputs to this successful run; the preparation preflight verifies that equivalence and binds the extracted evidence to GitHub artifact `12107201719` / `sha256:32a2a9277037d6d20489b06f66be2d26bed51d50b236d873239ae35e2230e68c`. The expanded run checks all six families, local/container action and outcome equality, dense/near-limit probes, image size, per-phase latency and Linux process peak RSS. See the audit for measured values and precise limits.
- **Disclosed weakness:** the frozen untouched sample yielded only 3 qualifying outcomes for the selected policy versus 16 for protected research RAVEN, over 18 episodes each. This result remains unchanged and was not used to reselect or tune the algorithm. Few seed clusters and rare events limit statistical conclusions.
- Zero invalid episodes in the public checks do not prove that every private observation will meet all validity or resource limits. No private leaderboard or real-world effectiveness claim is made.
