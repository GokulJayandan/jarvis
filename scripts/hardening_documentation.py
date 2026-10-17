"""Idempotent prose-only overlay after historical report regeneration/CI overlay."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def replace_file(name,old,new):
    path=ROOT/name
    if not path.exists():return
    path.write_text(path.read_text(encoding='utf-8').replace(old,new),encoding='utf-8')

def main():
    old='The official submission issue has not been created; it requires separate authorization. This documentation revision also awaits authorization to push.'
    interim='Final hardening status, expanded contract tests, release fixes, and current Docker evidence are recorded in `docs/FINAL_HARDENING_AUDIT.md`. Form-complete issue preparation tooling is ready; the immutable final-SHA package has not been posted.'
    baseline='**Docker and source-publication checks passed:** [GitHub Actions run 38919907335](https://github.com/GokulJayandan/jarvis/actions/runs/38919907335) successfully built and evaluated the policy container at public commit `98c5440dba6a2780f2ffd766c4f576fd796c4abb`.'
    final='**Final hardening and Docker checks passed:** [GitHub Actions run 39042745485](https://github.com/GokulJayandan/jarvis/actions/runs/39042745485) passed 93 tests, a clean image build, all six container scenarios, local/container action-and-outcome equality, and Linux boundary/resource probes at public commit `66874ac68ea8ab030a92e0a5b1f3542cffc1a411`. The original run 38919907335 remains baseline evidence. Full scope and limits are recorded in `docs/FINAL_HARDENING_AUDIT.md`. Form-complete issue preparation tooling is ready; the immutable final-SHA package has not been posted.'
    readme_old='[Successful CI run 38919907335](https://github.com/GokulJayandan/jarvis/actions/runs/38919907335) built the actual Dockerfile, completed official container evaluation, verified exact local/container equivalence, checked image size and uploaded diagnostic artifacts. The tested scope is one development episode, seed 101. [CI_VALIDATION.md](docs/CI_VALIDATION.md) records commands, limitations and log hashes. Source publication of the tested commit is verified; this documentation-only revision and official issue submission each require authorization.'
    readme_new='[Expanded CI run 39042745485](https://github.com/GokulJayandan/jarvis/actions/runs/39042745485) built the actual Dockerfile, passed all six scenario families with zero invalid episodes, verified exact local/container actions and outcomes, and recorded image, latency and Linux process-memory evidence. [FINAL_HARDENING_AUDIT.md](docs/FINAL_HARDENING_AUDIT.md) records commands, measurements and limits. The tested commit is public; form-complete issue preparation tooling is ready and the immutable final-SHA package is unposted.'
    history_old='The earlier local Docker attempts failed because Docker was absent; those failure records remain unchanged. They are superseded for the current policy by [successful CI run 38919907335](https://github.com/GokulJayandan/jarvis/actions/runs/38919907335) on public commit `98c5440dba6a2780f2ffd766c4f576fd796c4abb`. The actual Docker build and official container evaluator both exited 0. The development episode with seed 101 was valid (0 invalid episodes out of 1), and its actions and outcomes exactly matched subprocess evaluation. The Linux amd64 image measured 123,653,457 bytes (117.925 MiB), below the 2 GiB limit. The official evaluator applied network-disabled execution, 2 CPUs, 1 GiB RAM, a read-only filesystem and the 10-second per-invocation timeout; no resource-limit failure occurred. This is one container episode, not a six-scenario container benchmark or a private-validity guarantee. Separate peak-RAM telemetry was not collected in CI. Full commands, log hashes, image identity and evidence links are in `docs/CI_VALIDATION.md`. No website work or official issue submission was performed.'
    history_new='The earlier local Docker attempts failed because Docker was absent; those failure records remain unchanged as historical evidence. The original CI run 38919907335 later cleared the build gate for one development episode. Expanded [CI run 39042745485](https://github.com/GokulJayandan/jarvis/actions/runs/39042745485) then passed all six seed-101 scenario families with zero invalid episodes and exact local/container actions and outcomes. Across 744 calls there were no timeouts; the maximum observed wall time was 2.577 seconds. Instrumented Linux boundary probes measured a 65.805 MiB process high-water RSS, and the Linux amd64 image was 117.925 MiB. These public tests do not guarantee every private state. Full commands, hashes, measurements and qualifications are in `docs/FINAL_HARDENING_AUDIT.md`. No website work or official issue submission was performed.'
    seeds_old='- [Recovery commands](docs/RECOVERY_REPRODUCIBILITY.md), [original environment/provenance](docs/REPRODUCIBILITY.md), [declared recovery seeds](configs/recovery.json).'
    seeds_new='- [Recovery commands](docs/RECOVERY_REPRODUCIBILITY.md), [original environment/provenance](docs/REPRODUCIBILITY.md), [complete seed registry](configs/seeds.json), [declared recovery seeds](configs/recovery.json).'
    seed_text_old='The original model uses 18 training seeds, six calibration seeds and two original policy-selection seeds. Recovery uses three new screening seeds, five new confirmation seeds and three untouched reporting seeds. Inference random seed is 17 where an experimental random policy is used. Selection and configuration details are fully recorded; no private organizer worlds were accessed.'
    seed_text_new='The original model training seeds are `20261000`–`20261005` and `11001`–`11012`; validation/calibration seeds are `20261006`, `20261007` and `12001`–`12004`. The immutable [seed registry](configs/seeds.json) also declares reporting, fresh-test, pruning and stress seeds. Recovery uses three new screening seeds, five new confirmation seeds and three untouched reporting seeds. Inference random seed is 17 where an experimental random policy is used. Selection and configuration details are fully recorded; no private organizer worlds were accessed.'
    for name in ('README.md','report/TECHNICAL_REPORT.md','docs/RECOVERY_RELEASE.md'):
        path=ROOT/name;text=path.read_text(encoding='utf-8').replace(old,interim)
        text=text.replace(baseline+' '+interim,final).replace(baseline+' '+old,final)
        text=text.replace(readme_old,readme_new).replace(history_old,history_new)
        text=text.replace(seeds_old,seeds_new).replace(seed_text_old,seed_text_new)
        text=text.replace('git apply docs/RELEASE_DOCUMENTATION.patch\n```','git apply docs/RELEASE_DOCUMENTATION.patch\npython scripts/hardening_documentation.py\n```')
        text=text.replace('The preserved report generator emits pre-CI release prose; the documentation-only patch above restores the verified CI/publication update without altering generated tables or figures.',
            'The preserved report generator emits pre-CI release prose; the baseline patch and hardening overlay restore verified release evidence without altering generated tables or figures.')
        text=text.replace('Docker execution is blocked on this host; this build must not be represented as submission-ready until that gate passes.',
            'At the original study date Docker was absent on the Windows host. That historical blocker was subsequently cleared for the released V1_greedy by verified Linux CI; see the current release audit above.')
        text=text.replace('The optional website was not started because mandatory Docker verification remains blocked.',
            'No website is part of this submission. Historical Docker failures are superseded by the verified Linux CI evidence in the current release audit.')
        text=text.replace('Container validation is an actual unresolved blocker. Unit-test success does not prove private validity.',
            'At the original study checkpoint, container validation was unresolved. Expanded Linux CI subsequently passed for the released policy; finite public tests still do not prove private validity.')
        text=text.replace('the Dockerfile specifies Python 3.12.7, which requires actual container verification.',
            'the Dockerfile specifies Python 3.12.7, which expanded Linux CI verified for the released container.')
        text=text.replace('The selected public-validation configuration is soft; measured final score is 0.3611 MSMI/100. The report preserves both positive and negative evidence. Local implementation and public evaluation must be distinguished from submission completion. A working offline Docker run and authorized publication of an immutable commit remain necessary before official submission.',
            'The historical public-validation configuration was soft and measured 0.3611 MSMI/100. The released V1_greedy policy and its 0.3889 MSMI/100 mandatory comparison are documented in the recovery sections above, together with the negative untouched result. Offline Docker verification and immutable source publication have passed; the official issue remains unposted.')
        text=text.replace('The official submission issue package is prepared separately and has not been posted.',
            'Form-complete issue preparation tooling is ready; the immutable final-SHA package has not been posted.')
        text=text.replace('the immutable issue package is prepared and unposted.',
            'form-complete issue preparation tooling is ready and the immutable final-SHA package is unposted.')
        path.write_text(text,encoding='utf-8')

    replace_file('docs/RECOVERY_REPRODUCIBILITY.md',
        'For report-only regeneration, run `python -m experiments.recovery_report` followed\nby `git apply docs/RELEASE_DOCUMENTATION.patch`. The unmodified generator\nreconstructs measured tables/figures and the historical report; the prose-only\npatch restores the post-CI documentation. Use a disposable copy for verification',
        'For report-only regeneration, run `python -m experiments.recovery_report`,\n`git apply docs/RELEASE_DOCUMENTATION.patch`, then\n`python scripts/hardening_documentation.py`. The unmodified generator\nreconstructs measured tables/figures and the historical report; the two prose-only\noverlays restore the baseline and expanded post-CI documentation. Use a disposable copy for verification')
    replace_file('docs/RECOVERY_REPRODUCIBILITY.md',
        'The issue submission package is\nprepared separately.',
        'Form-complete issue preparation tooling is ready; the immutable final-SHA package\nis generated after publication.')
    replace_file('docs/RECOVERY_AUDIT.md',
        '`FINAL_HARDENING_AUDIT.md`; the official issue package is prepared but unposted.',
        '`FINAL_HARDENING_AUDIT.md`; form-complete issue preparation tooling is ready, and the immutable final-SHA package remains unposted.')
    replace_file('docs/FINAL_HARDENING_AUDIT.md',
        'Test execution evidence is `results/hardening/{local,python312}/tests.{json,log}`.',
        'Final test execution evidence is `results/hardening/{final_tests,final_python312}/tests.{json,log}`.')
    replace_file('docs/FINAL_RELEASE_VERIFICATION.md',
        'The final issue package is prepared and remains unposted.',
        'Form-complete preparation tooling is ready; the immutable final-SHA package is generated only after the commit and CI evidence are public.')
    replace_file('docs/FINAL_RELEASE_VERIFICATION.md',
        '| Public immutable links | Raw files match Git object bytes without authentication | PASS after final package generation |',
        '| Public immutable links | Raw files must match Git object bytes without authentication | FINAL PACKAGE GATE |')
    replace_file('docs/FINAL_RELEASE_VERIFICATION.md',
        '| Official issue | Prepared package, unposted | READY |',
        '| Official issue | Form-complete generator ready; final-SHA package unposted | READY AFTER PUBLICATION |')
    replace_file('docs/RECOVERY_INDEPENDENT_REVIEW.md',
        '| F: publication | Ready | Hardening commit `66874ac68ea8ab030a92e0a5b1f3542cffc1a411` is public and its SHA-pinned report/results match Git bytes | Current-template issue package and immutable source archive prepared after final CI | Official issue has not been posted |',
        '| F: publication | Ready after final publication gate | Hardening commit `66874ac68ea8ab030a92e0a5b1f3542cffc1a411` is public and its SHA-pinned report/results match Git bytes | Generate the current-template issue package and immutable source archive only after the final commit and CI artifact are public | Official issue has not been posted |')
    replace_file('docs/RECOVERY_INDEPENDENT_REVIEW.md',
        'one container episode does not guarantee private validity',
        'finite public container episodes do not guarantee private validity')
    replace_file('docs/SUBMISSION_CHECKLIST.md',
        '| 19 | Immutable public commit available | PASS | Public `66874ac68ea8ab030a92e0a5b1f3542cffc1a411`, verified report/results and expanded CI evidence |',
        '| 19 | Immutable public commit available | PASS (tested source) | Public `66874ac68ea8ab030a92e0a5b1f3542cffc1a411`; final documentation SHA is checked by the package generator after publication |')
    replace_file('docs/SUBMISSION_CHECKLIST.md',
        '| 20 | Official submission | READY / NOT POSTED | Immutable issue package is prepared after hardening and public-link verification |',
        '| 20 | Official submission | READY AFTER PUBLICATION / NOT POSTED | Form-complete generator is ready; immutable issue package is created only after final-SHA CI and public-link verification |')

if __name__=='__main__':main()
