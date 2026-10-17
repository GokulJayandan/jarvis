# Final release verification

## Starting state

Recorded on 17 October 2026 (Asia/Calcutta) before the final release-lockdown pass.

| Check | Observed value | Status |
|---|---|---|
| Repository | `GokulJayandan/jarvis` | PASS |
| Origin fetch/push URL | `https://github.com/GokulJayandan/jarvis.git` | PASS |
| Branch | `main` | PASS |
| Local HEAD | `66874ac68ea8ab030a92e0a5b1f3542cffc1a411` | PASS |
| Remote `origin/main` | `66874ac68ea8ab030a92e0a5b1f3542cffc1a411` | PASS |
| Protected recovery commit | `98c5440dba6a2780f2ffd766c4f576fd796c4abb` | PASS — retained in history |
| Previous successful Docker workflow | `https://github.com/GokulJayandan/jarvis/actions/runs/38919907335` | PASS — preserved as historical evidence |

The tracked worktree was clean. Five untracked hardening artifacts were present and preserved for review: two document-reproduction JSON files, one Python 3.12 evidence directory, and two release helper scripts. No reset, checkout, clean, or history-rewriting operation was performed.

The live organiser specification, submission guide, data contract, changelog, and final-submission issue template were checked against the vendored copies. The public deadline remains 18 October 2026 at 23:59 IST, and the required Round 2 route remains the repository's Final submission issue form. Form-complete preparation tooling is ready; the immutable final-SHA package is generated only after the commit and CI evidence are public.

## Final state

Completed on 17 October 2026.

| Check | Evidence | Status |
|---|---|---|
| Full local suite | 93 tests on Python 3.14.6 | PASS |
| Portable runtime suite | 90 run on Python 3.12.7; 88 pass, 2 training-only skips | PASS |
| Official data | 71/71 checksums | PASS |
| Historical research evidence | 318 validation episodes, 540 pruning replays, 54 historical resource probes | PASS |
| Report/figure reproduction | 14 files reproduced in an isolated Git archive copy | PASS |
| Publication screening | 529 staged files; no matched credential/key patterns | PASS within documented pattern-scan limits |
| Expanded Docker CI | [Run 39042745485](https://github.com/GokulJayandan/jarvis/actions/runs/39042745485), commit `66874ac68ea8ab030a92e0a5b1f3542cffc1a411` | PASS |
| Container scenarios | Six families, seed 101; 6/6 valid, 0 invalid | PASS |
| Local/container equivalence | All actions and outcomes equal | PASS |
| Container resource probes | 744 calls, 0 timeouts; max 2.577 s; process peak 65.805 MiB; image 117.925 MiB | PASS for tested scope |
| Public immutable links | Raw files must match Git object bytes without authentication | FINAL PACKAGE GATE |
| Official issue | Form-complete generator ready; final-SHA package unposted | READY AFTER PUBLICATION |

The deployed V1_greedy configuration and model assets remain unchanged from the
freeze. Three defects fixed during hardening are confined to standalone research
matching, pruning and empty-dataset training paths. The untouched negative result
remains disclosed: selected V1_greedy recorded 3 qualifying outcomes versus 16
for protected research RAVEN across 18 episodes per arm. No held-out result was
used to change the selected policy.
