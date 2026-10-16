"""Generate recovery conclusions, tables and figures from executed evidence only."""
import json
import statistics as st
import subprocess
from pathlib import Path
from experiments.common import ROOT,write,paired_ci

B=ROOT/'results/recovery'
def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
def rows(stage,name):return read(f'results/recovery/{stage}/{name}.json')['episodes']
def fmt(x):return f'{x:.6g}' if isinstance(x,float) else str(x)
def table(headers,records):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(fmt,r))+' |' for r in records])
def total(data):
    r=data['episodes'];waits=[v for e in r for v in e['first_introduction_wait_days']]
    return dict(episodes=len(r),valid=sum(e['valid'] for e in r),score=data['summary']['primary_score'],
        **{k:sum(e[k] for e in r) for k in ('arrived_members','assignments','mutual_acceptances','dates','mutual_second_meeting_intention','served_members','unserved_members','ask_cost','missing_feedback')},
        coverage=st.mean(e['coverage'] for e in r),wait_mean=st.mean(waits) if waits else None,wait_median=st.median(waits) if waits else None,
        seconds=st.mean(e['inference_seconds'] for e in r))

def main():
    assert read('results/recovery/release_checks_complete.json')['valid']
    selection=read('results/recovery/selection.json');plan=read('configs/recovery.json')
    data={n:read(f'results/recovery/{n}.json') for n in ('greedy','no_asks','random','final')}
    totals={n:total(d) for n,d in data.items()}
    old=read('results/recovery/matched_diagnostics.json');diag=read('results/recovery/observation_diagnostics.json')
    screen={p.stem:read(str(p.relative_to(ROOT))) for p in (B/'screen').glob('*.json')}
    screenrows=[[n,d['summary']['primary_score'],sum(r['mutual_second_meeting_intention'] for r in d['episodes']),d['summary']['overall']['coverage'],d['summary']['overall']['ask_cost']] for n,d in sorted(screen.items())]
    confirm={p.stem:read(str(p.relative_to(ROOT))) for p in (B/'confirm').glob('*.json')}
    confirmrows=[[n,d['summary']['primary_score'],sum(r['mutual_second_meeting_intention'] for r in d['episodes']),d['summary']['overall']['coverage'],d['summary']['overall']['ask_cost']] for n,d in sorted(confirm.items())]
    scenarios=[]
    for variant in data['final']['summary']['scenario_means']:
        subset=[r for r in data['final']['episodes'] if r['variant']==variant]
        scenarios.append([variant,len(subset),sum(r['arrived_members'] for r in subset),sum(r['mutual_second_meeting_intention'] for r in subset),
            st.mean(r['msmi_per_100_arrived_members'] for r in subset),sum(r['dates'] for r in subset),st.mean(r['coverage'] for r in subset),st.mean(r['ask_cost'] for r in subset)])
    comparisons={n:paired_ci(d['episodes'],data['greedy']['episodes']) for n,d in data.items() if n!='greedy'}
    ablations={n:paired_ci(d['episodes'],screen['V0_frozen']['episodes']) for n,d in screen.items() if n!='V0_frozen'}
    future_effects={};future_scenarios=[]
    for label,present,future in [('historical_soft',read('results/future/present.json'),read('results/future/future.json')),
                                 ('recovery_screen',screen['V0_frozen'],screen['A_future'])]:
        a=[dict(r,mean_wait_days=st.mean(r['first_introduction_wait_days'])) for r in future['episodes'] if r['first_introduction_wait_days']]
        b=[dict(r,mean_wait_days=st.mean(r['first_introduction_wait_days'])) for r in present['episodes'] if r['first_introduction_wait_days']]
        future_effects[label]={key:paired_ci(a,b,key) for key in ('msmi_per_100_arrived_members','dates','coverage','mean_wait_days','ask_cost','inference_seconds')}
        for variant in sorted({r['variant'] for r in a}):
            aa=[r for r in a if r['variant']==variant];bb=[r for r in b if r['variant']==variant]
            future_scenarios.append([label,variant,len(aa),*[st.mean(r[key] for r in aa)-st.mean(r[key] for r in bb) for key in ('msmi_per_100_arrived_members','dates','coverage','mean_wait_days','ask_cost')]])
    resources=read('results/recovery/robustness/resources.json');adversarial=read('results/recovery/robustness/adversarial.json')
    max_payload=read('results/recovery/robustness/max_payload_process_tree.json')
    probes=resources['calls']+adversarial['calls']+max_payload['calls']
    probe_summary=dict(calls=len(probes),max_seconds=max(r['seconds'] for r in probes),max_rss_mib=max(r['peak_sampled_rss_bytes'] for r in probes)/1024**2,
        max_request_bytes=max(r['request_bytes'] for r in probes),max_response_bytes=max(r['response_bytes'] for r in probes))
    observed=[]
    for mode in ('greedy','frozen'):
        es=[e for e in diag['episodes'] if e['policy']==mode];ds=[d for e in es for d in e['days']];ps=[p for e in es for p in e['predictions']]
        delays=[d for e in es for d in e['feedback_delays']]
        observed.append([mode,len(es),sum(d['hard_asks'] for d in ds),sum(d['soft_asks'] for d in ds),
            sum(d['confirmed_after']-d['confirmed_before'] for d in ds),sum(d['unallocated_disjoint_edges'] for d in ds),
            sum(p['p'] for p in ps),sum(p['msmi'] for p in ps),st.mean(delays) if delays else 0,
            sum(e['feedback_without_occurrence_day'] for e in es)])
    fresh={p.stem:read(str(p.relative_to(ROOT))) for p in (B/'fresh').glob('*.json')}
    fresh_comparison=paired_ci(fresh[selection['selected']]['episodes'],fresh['V1_greedy']['episodes'])
    fresh_reference=paired_ci(fresh['V0_frozen']['episodes'],fresh[selection['selected']]['episodes'])
    write('results/recovery/report_tables.json',dict(selected=selection['selected'],totals=totals,scenarios=scenarios,screen=screenrows,confirm=confirmrows,
        comparisons=comparisons,screening_ablations=ablations,future_effects=future_effects,future_scenarios=future_scenarios,resources=probe_summary,observation_diagnostics=observed,fresh={n:total(d) for n,d in fresh.items()},fresh_selected_vs_greedy=fresh_comparison,fresh_protected_minus_selected=fresh_reference))
    final=totals['final'];chosen=selection['selected']
    calibration=read('results/calibration/metrics.json')
    calrows=[[r['target'],r['model']+(' calibrated' if r['calibrated'] else ''),r['n'],r['positives'],r['brier'],r['log_loss']] for r in calibration['targets'] if r['stratum']=='all']
    strata=[[r['stratum'],r['model']+(' calibrated' if r['calibrated'] else ''),r['n'],r['positives'],r['brier'],r['ece']] for r in calibration['targets'] if r['target']=='msmi' and r['stratum']!='all']
    pruning=read('results/pruning/regret.json')['rows'];pruning_rows=[]
    for limit in (2,4,6,8,12):
        rs=[r for r in pruning if r['candidate_limit']==limit];regrets=sorted(r['absolute_regret'] for r in rs)
        pruning_rows.append([limit,len(rs),sum(r['absolute_regret']>1e-12 for r in rs),sum(r['best_portfolio_excluded'] for r in rs),st.mean(regrets),regrets[int(.95*(len(rs)-1))],max(regrets),st.mean(r['oracle_seconds'] for r in rs),st.mean(r['pruned_seconds'] for r in rs)])
    methods={
      'V1_greedy':'Official greedy clarification and soft-agreement greedy matching, wrapped in RAVEN independent hard-eligibility, budget, duplicate and availability validation. Learned probabilities, portfolio search and future terms are not used by the selected policy.',
      'V0_frozen':'Joint clarification over up to 12 candidate hard bundles, optional leftover-budget soft questions, calibrated direct-MSMI edge weights and exact blossom matching with bounded fallback. Future and waiting weights are zero.',
      'V4_prior':'Joint hard-bundle clarification over up to 12 candidates, using the pooled MSMI prior and learned observed-data feasibility cells for its surrogate; no soft questions. Confirmed edges have the same positive pooled outcome weight, so exact weighted matching selects maximum cardinality with deterministic tie resolution. Future and waiting weights are zero.',
      'V5_present':'Joint hard-bundle clarification over up to 12 candidates, calibrated direct-MSMI edge weights, and exact blossom matching with bounded fallback. Soft questions, future value and waiting penalties are disabled.'}
    method=methods[chosen]+' Exact settings are in `results/recovery/release_selection.json`.'
    text=f'''# Recovery release evidence

Team Jarvis — RAVEN-Match. **NO-GO for submission:** Docker execution and public immutable publication remain blocked. This is an executed local recovery, not a claim of private performance.

**Important negative result:** the untouched post-freeze sample favored protected RAVEN over the selected conservative policy: {total(fresh['V0_frozen'])['mutual_second_meeting_intention']} versus {total(fresh[selection['selected']])['mutual_second_meeting_intention']} qualifying outcomes over 18 episodes each. The selection rule did not identify the stronger policy on this sample. The choice remains frozen to avoid selecting on the held-out results; no claim of improved generalization or statistically optimal policy selection is made.

## Selected release algorithm

Selected configuration: **{chosen}**. {method}

Selection used newly declared public validation seeds only: screening {plan['screening_validation_seeds']}; confirmation {plan['confirmation_validation_seeds']}. The predeclared rule requires a custom finalist's paired interval against greedy to exclude zero; otherwise select guarded greedy. V6 aliases V0 and V7 aliases V1 and were not counted as separate algorithms. These intervals use only five seed clusters, are descriptive, and are not multiplicity-adjusted. No superiority guarantee follows.

Original 101–103 reporting results were already known during recovery, so the repeated benchmark is a reproducibility comparison, not a newly untouched test. Seeds {plan['untouched_reporting_seeds']} were untouched until selection and source freeze. No outcome from those seeds changed the configuration. Original training and model bytes were preserved. The original 13-policy study remains historical evidence.

## Mandatory official subprocess benchmark

Each row has 18 episodes, six families × three matched seeds, 60 decision days + 40 follow-up days. MSMI counts are qualifying pairs; arrivals are members. The score is the unchanged official equal-family average. Evidence: `results/recovery/{{greedy,no_asks,random,final}}.json`.

{table(['Policy','Valid/episodes','MSMI','Arrivals','MSMI/100','Meetings','Coverage','Ask units/episode'],[[n,f"{t['valid']}/{t['episodes']}",t['mutual_second_meeting_intention'],t['arrived_members'],t['score'],t['dates'],t['coverage'],t['ask_cost']/t['episodes']] for n,t in totals.items()])}

{table(['Scenario','Episodes','Arrivals','MSMI','MSMI/100','Meetings','Coverage','Ask units/episode'],scenarios)}

Zero MSMI means no qualifying observed event in that sample, not an estimated zero success probability. With rare events and three seed clusters, uncertainty is large. Paired differences and descriptive bootstrap intervals are in `results/recovery/report_tables.json`.

## Validation search and confirmation

Screening: 18 episodes per distinct configuration; no final-reporting outcomes used.

{table(['Configuration','MSMI/100','MSMI count','Coverage','Ask units/episode'],screenrows)}

Confirmation: 30 episodes per finalist, five new seeds × six families.

{table(['Configuration','MSMI/100','MSMI count','Coverage','Ask units/episode'],confirmrows)}

Selection evidence and paired intervals: `results/recovery/selection.json`. Configuration IDs, exact overrides, source/model hashes and seed declarations are in `configs/recovery.json`, `registered_plan.json`, each run JSON and `frozen_source.json`. In-process validation uses the official engine and action validation, but its runtime is not comparable to container/startup time.

## Untouched post-freeze reporting

{table(['Configuration','Episodes','MSMI count','MSMI/100','Coverage'],[[n,t['episodes'],t['mutual_second_meeting_intention'],t['score'],t['coverage']] for n,d in fresh.items() for t in [total(d)]])}

Evidence: `results/recovery/fresh/*.json`. These are official-engine in-process episodes, not container evaluation. This small sample does not establish private or real-world generalization.

Selected versus greedy on these untouched seeds: {fresh_comparison}.

Protected RAVEN minus selected release on untouched seeds: {fresh_reference}. This is an adverse result for the recovery selection, not evidence to hide behind the repeated 101–103 benchmark. A different selection decision would require a separately declared validation process and another untouched evaluation; no such retuning was performed here.

## Waiting, coverage and feedback

The selected policy served {final['served_members']} of {final['arrived_members']} arrivals; {final['unserved_members']} remained unserved. Among served members only, mean first-introduction wait was {final['wait_mean']:.3f} days and median {final['wait_median']} days. Unserved members are excluded from this conditional wait statistic and remain in coverage denominators. Missing feedback count was {final['missing_feedback']}; pending records were not labelled as preference failures.

For the original candidate versus greedy, the observation-only diagnostic replays seed 101 in each family. It records every day before and after asks. Feedback delays exclude records with no occurrence day and count those separately.

{table(['Policy','Episodes','Hard asks','Soft asks','New feasible edges summed/day','Unallocated disjoint edges','Predicted MSMI sum','Realized MSMI','Mean feedback delay days','No occurrence date'],observed)}

Source: `results/recovery/observation_diagnostics.json`. Feasible-edge sums count repeated opportunities on different days and are not distinct people or outcomes. These diagnostic trajectories differ after the first differing action; they do not isolate causal effects.

## Reviewer investigations

Future value: the historical protected soft-policy comparison was +0.3333 MSMI/100, descriptive interval [0, 0.5], over three fresh seed clusters. New screening compares A_future against V0 with all other settings fixed: {ablations['A_future']}. This replication is validation evidence, not a new held-out claim. Neither coefficient nor policy is chosen from the old reporting seeds. Future-aware value remains a heuristic based on training arrival frequencies, never observed future people. These are research RAVEN ablations; the deployed guarded greedy policy does not use a future term.

{table(['Future-on minus off study','Metric / unit','Mean difference','95% descriptive interval','Episodes'],[[label,key,v['mean_difference'],str(v['ci95']),v['n_episodes']] for label,effects in future_effects.items() for key,v in effects.items()])}

Mean waiting is conditional on served members and is first computed per episode. Coverage is a fraction; ask cost is units per episode; dates are completed pairs per episode. Runtime is in-process inference seconds per episode under concurrent load. Scenario-specific effects remain available in each paired result file and are not assumed uniform.

{table(['Study','Scenario','Episodes/arm','MSMI/100 delta','Dates/episode delta','Coverage delta','Wait days delta','Ask units delta'],future_scenarios)}

Pruning: all 540 stored comparisons were audited for exhaustive combination counts, identical budgets and regret arithmetic. At limit 12, all 108 comparisons had zero measured surrogate regret across 36 underlying small states, but **only {sum(r['original_candidates']>r['pruned_candidates'] for r in pruning if r['candidate_limit']==12)} of those 108 comparisons actually removed candidates**. This substantially limits the evidence for the production limit. This is neither 540 independent states nor proof of zero actual MSMI loss. Production-observation exact probes: {len(diag['production_state_oracles'])}, of which {sum(r['candidates']>r['kept'] for r in diag['production_state_oracles'])} removed candidates; these only cover encountered states with at most 16 useful questions. Detailed regret, selected portfolios and runtimes are retained; larger candidate states are not claimed exact.

All 540 cases were also rerun: every portfolio, utility and regret matched exactly (`recovery_pruning_replay.log`). Exclusion of one chosen optimum can leave another tied optimum, so exclusion and positive regret differ. Relative regret is stored per case and undefined when oracle utility is zero. Python allocation peaks are recorded, not total process memory. Runtime averages below use the original study and are not a container speed claim.

{table(['Limit','Comparisons','Positive regret','Chosen optimum excluded','Mean regret','95th percentile','Max regret','Oracle seconds','Pruned seconds'],pruning_rows)}

Calibration: all pooled and model scores, including disclosure strata, were recomputed from the saved 960 selected-introduction records. Qualifying MSMI has only six positives; pooled Brier is slightly better than the calibrated model. Better acceptance calibration is not evidence of better MSMI ranking. All-pair calibration and randomized counterfactual ranking remain unmeasured. Disclosure is deterministic under this version's observed status semantics; its zero Brier is a contract check, not learned prediction skill.

{table(['Target','Predictor','Selected pairs','Positives','Brier','Log loss'],calrows)}

{table(['MSMI disclosure stratum','Predictor','Selected pairs','Positives','Brier','ECE'],strata)}

Source: `results/calibration/metrics.json`; predictions were fitted only on training and validation worlds. These selected-introduction records are biased toward the historical policies, with no known propensity correction. Mature recorded-event targets differ from latent preference labels. Pending/missing second-meeting responses are not labelled as negative preferences. Reliability figures retain bin sample sizes and descriptive Wilson intervals that do not account for within-world dependence.

The directional model's gain over the pooled prior must not be attributed solely to calibration: the uncalibrated model has slightly lower directional Brier than the calibrated one. Likewise, the pooled MSMI prior is better on Brier while the calibrated predictor is better on log loss in this sample. Six positives do not establish a uniformly better probability estimator.

## Reliability and resources

Final unit tests and official data verification passed; see `results/execution/recovery_final_tests.*` and `recovery_final_data.*`. The protected soft configuration and unchanged model were replayed for 18 episodes through the recovery dispatcher; every action hash and outcome matches the original file. Separately, `recovery_protected_commit` extracts the protected commit's exact source bytes and executes a matching official subprocess smoke episode; `protected_source_audit.json` records the byte hashes. Baseline replays are compared against original files. New phase-backend and full-episode guarded-baseline equivalence tests exercise the only inference code changes.

There are {probe_summary['calls']} final subprocess resource probes, including six constructed cases near the 1 MiB request limit. Maximum observed invocation: {probe_summary['max_seconds']:.4f} seconds; sampled RSS: {probe_summary['max_rss_mib']:.3f} MiB; request: {probe_summary['max_request_bytes']} bytes; response: {probe_summary['max_response_bytes']} bytes. These Windows measurements are sampled, may miss peaks, and do not verify enforced container CPU/RAM limits. Stress episodes and adversarial dense/unresolved/declined observations use legal-action checks. Each resource invocation rejects unexpected stderr rather than allowing an exception fallback to hide a failure.

Docker build failed to launch because the executable is absent, and official container evaluation exited 2. CI uses Ubuntu, the actual Dockerfile, the official evaluator, exact local/container action comparison and uploaded exit-code/log artifacts. CI has not been run. Public source and issue publication have not been authorized. No website work was started.

Recovery found and corrected a memory-measurement defect: Windows virtual-environment Python uses a launcher and child interpreter, while the historical sampler measured only the launcher PID. The original RSS claims can therefore underestimate total memory. All current release resource measurements sum the launcher and recursive descendants, which may double-count shared pages. The preliminary launcher-only near-limit file is retained as `max_payload.json`; the corrected file is `max_payload_process_tree.json`. Inference code was not changed by this measurement correction.

## Reproduction and provenance

Use Python 3.14 with `requirements-dev.txt` for research, or the pinned Python 3.12.7 Docker image for inference. Inference has no pip dependencies, network, GPU or persistent filesystem state. Official MIT source and synthetic-data notices, vendored BSD matching notices and all model provenance remain included. OpenAI Codex assisted implementation and automated review; no human independent review is claimed.

Run `python -m scripts.verify_recovery`, `python -m experiments.recovery_report`, and the commands in `docs/RECOVERY_REPRODUCIBILITY.md`. New run scripts refuse to overwrite search evidence. To repeat the full search, use a clean checkout with a different result root. The protected original candidate is tagged `recovery/pre-competitive-recovery` at `a918583473afbb0bc70abe76f1266c39331bf97b`.
'''
    (ROOT/'docs/RECOVERY_RELEASE.md').write_text(text,encoding='utf-8')
    historical=ROOT/'report/TECHNICAL_REPORT_PRE_RECOVERY.md'
    if not historical.exists():
        historical.write_bytes(subprocess.check_output(['git','show','a918583473afbb0bc70abe76f1266c39331bf97b:report/TECHNICAL_REPORT.md'],cwd=ROOT))
    report=text+'\n\n---\n\n# Historical RAVEN research study (protected pre-recovery candidate)\n\nAll references to the selected or frozen soft policy in the following historical sections describe the protected original candidate, not the current release configuration above. Original results and figures are preserved unchanged.\n\n'+historical.read_text(encoding='utf-8')
    (ROOT/'report/TECHNICAL_REPORT.md').write_text(report,encoding='utf-8')
    readme=f'''# Team Jarvis — RAVEN-Match

Round 2 of [The Sequential Matching Problem](https://github.com/RomeoJulietLove/The-Sequential-Matching-Problem). All profiles and outcomes are synthetic.

Current release configuration: **{chosen}**. {method}

**NO-GO for submission:** Docker is unavailable locally, CI has not executed, and no source or issue has been published. The local implementation and experiments are tested; container eligibility is not established.

The repeated official benchmark scores {final['score']:.4f} MSMI/100 ({final['mutual_second_meeting_intention']} qualifying pairs / {final['arrived_members']} arrivals). Greedy scores {totals['greedy']['score']:.4f}; this is not a claim of superiority. Selection used fresh validation; untouched post-freeze results and uncertainty are in the report.

**Negative generalization result:** on the untouched three-seed sample, the selected policy obtained {total(fresh[selection['selected']])['mutual_second_meeting_intention']} qualifying outcomes versus protected RAVEN's {total(fresh['V0_frozen'])['mutual_second_meeting_intention']} (18 episodes each). The conservative selection rule did not choose the stronger policy on that sample. The configuration was not changed after seeing held-out outcomes.

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
python -m scripts.verify_recovery
```

The original model uses 18 training seeds, six calibration seeds and two original policy-selection seeds. Recovery uses three new screening seeds, five new confirmation seeds and three untouched reporting seeds. Inference random seed is 17 where an experimental random policy is used. Selection and configuration details are fully recorded; no private organizer worlds were accessed.

CI builds the actual Dockerfile and retains command logs, exit codes, local/container comparisons and image inspection as artifacts. A workflow file is not evidence of a successful container run. Authorization is still required to push and later submit the official issue.

## Attribution and team

Upstream release 1.0.0, commit `a8e26b35118cfa8e886a02f93984923e43ab64f6`. [MIT licence](LICENSE), [synthetic data conditions](DATA_LICENSE.md), [upstream provenance](docs/UPSTREAM_PROVENANCE.md), and [dependency notices](docs/LICENSES.md) are retained. The research matcher retains NetworkX BSD-3-Clause notices. No external pretrained models or real member data are used. OpenAI Codex assisted implementation and automated self-review.

Team Jarvis: GokulJayandan R S, Keerthana Janakiraman, Mridula B, Boomika L. No website was built. The original candidate is protected by tag `recovery/pre-competitive-recovery` at `a918583473afbb0bc70abe76f1266c39331bf97b`.
'''
    (ROOT/'README.md').write_text(readme,encoding='utf-8')
    diagnostic_report(old,diag,ablations,observed)
    figures(data,screen,confirm,observed)

def diagnostic_report(old,diag,ablations,observed):
    paired=old['paired']
    lines=['# Performance gap: measured diagnosis','',
      'The original difference is one qualifying pair across 18 episodes. '+str(paired),
      'This sample cannot identify a single causal root cause. The following assessments separate directly supported observations from hypotheses.','',
      table(['Hypothesis','Diagnostic and evidence','Conclusion'],[
        ['H1: wasted questions','Original ask units: 10,368 versus 3,720; observation replay separates hard/soft asks; V5 removes soft asks on new validation.','Supported for excess cost; causal MSMI harm inconclusive.'],
        ['H2: optimistic portfolio utility','Daily predicted surrogate gains and realized feasible-edge changes are recorded in observation_diagnostics.json. They are different quantities and cannot be equated.','Inconclusive: no unbiased counterfactual portfolio outcome oracle.'],
        ['H3: pruning loses useful opportunities',f"540 exact small comparisons; only 3/108 at limit 12 remove candidates; production probes n={len(diag['production_state_oracles'])}; V9 changes screening on full validation episodes.",'Inconclusive for full-state MSMI attribution; small-state surrogate loss measured.'],
        ['H4: poor outcome ranking','V4 pooled prior versus V5 calibrated no-soft; V2/V3 isolate official question/match components. See screen JSON.','Inconclusive. Calibration alone cannot establish ranking quality; sparse controlled outcome evidence reported.'],
        ['H5: acceptance versus MSMI mismatch','Directional Brier improves; MSMI pooled prior has slightly better held-out Brier, only six positives.','Supported as calibration limitation; not proof of score-gap causation.'],
        ['H6: future/wait deferral','Protected selected config has future_weight=0 and waiting_weight=0.','Unsupported for the reported score gap.'],
        ['H7: exact matching with weak weights','A_greedy_weighted changes only matching algorithm; V3 changes weights and algorithm to official baseline.','Inconclusive; paired validation does not justify a blanket claim that exact optimization is worse.'],
        ['H8: insufficient introductions','Original RAVEN: 1,444 introductions/1,351 served; greedy: 1,437/1,338.','Unsupported as an aggregate coverage deficit.'],
        ['H9: proxy not primary outcome','All selections and reporting use official MSMI; planning surrogate lacks proven relationship to realized MSMI.','Inconclusive: proxy mismatch remains a risk, not demonstrated causality.'],
        ['H10: rare-event variation',f"Original paired difference {paired['mean_difference']:.5f}; descriptive CI {paired['ci95']}.",'Compatible with variation; neither superiority nor inferiority established.']]),'',
      '## Per-seed matched table','',table(['Scenario','Seed','Greedy MSMI','RAVEN MSMI','Delta','Greedy dates','RAVEN dates','Date delta','Greedy ask cost','RAVEN ask cost','Coverage delta','Wait delta days'],[
        [r['scenario'],r['seed'],r['greedy_mutual_second_meeting_intention'],r['raven_mutual_second_meeting_intention'],r['delta_mutual_second_meeting_intention'],r['greedy_dates'],r['raven_dates'],r['delta_dates'],r['greedy_ask_cost'],r['raven_ask_cost'],r['delta_coverage'],r['delta_mean_first_introduction_wait_days']] for r in old['rows']]),'',
      '## Original observed outcome funnel','',table(['Policy','Introductions','Mutual acceptances','Dates','MSMI','Dates / mutual acceptances','MSMI / dates'],[[n,t['assignments'],t['mutual_acceptances'],t['dates'],t['mutual_second_meeting_intention'],t['dates']/t['mutual_acceptances'],t['mutual_second_meeting_intention']/t['dates']] for n,t in old['totals'].items() if n in ('greedy','final')]),'',
      'These ratios are conditional on different selected pairs and cannot isolate a stage-specific causal mechanism. RAVEN has more recorded mutual acceptances but fewer completed meetings; an acceptance model alone does not optimize the final target.','',
      '## Controlled screening differences against frozen RAVEN','',table(['Variant','MSMI/100 delta','95% descriptive interval','Seed clusters'],[[n,v['mean_difference'],str(v['ci95']),v['n_seed_clusters']] for n,v in ablations.items()]),'',
      'Waiting is conditional on receiving an introduction. All timings are descriptive under concurrent execution. No latent preference, future arrival or hidden propensity was provided to a policy. Missing feedback occurrence dates are excluded from delay means, with counts retained.']
    (ROOT/'docs/PERFORMANCE_ROOT_CAUSE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

def figures(data,screen,confirm,observed):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    out=ROOT/'figures/recovery';out.mkdir(parents=True,exist_ok=True);catalog=[]
    def save(name,source):
        plt.tight_layout();plt.savefig(out/(name+'.png'),dpi=160);plt.close();catalog.append({'file':f'figures/recovery/{name}.png','source':source})
    names=list(data)
    plt.figure(figsize=(7,4));plt.bar(names,[d['summary']['primary_score'] for d in data.values()]);plt.ylabel('Qualifying MSMI / 100 arrivals');plt.title('Official subprocess benchmark: 18 episodes per policy');save('01_baselines','results/recovery/{greedy,no_asks,random,final}.json')
    variants=list(data['final']['summary']['scenario_means']);xs=list(range(6))
    plt.figure(figsize=(9,4))
    for index,name in enumerate(names):plt.bar([x+(index-1.5)*.2 for x in xs],[data[name]['summary']['scenario_means'][v]['msmi_per_100_arrived_members'] for v in variants],width=.2,label=name)
    plt.xticks(xs,variants);plt.ylabel('MSMI / 100 arrivals');plt.title('Three episodes per policy and scenario');plt.legend();save('02_scenarios','results/recovery/*.json')
    plt.figure(figsize=(7,4))
    for name,d in data.items():
        t=total(d);plt.scatter(t['dates'],t['mutual_second_meeting_intention'],label=name)
        plt.annotate(name,(t['dates'],t['mutual_second_meeting_intention']),xytext=(5,-14 if name=='final' else 6),textcoords='offset points')
    plt.margins(x=.18,y=.2)
    plt.xlabel('Completed meetings (18 episodes)');plt.ylabel('Qualifying MSMI pairs');save('03_meetings','results/recovery/*.json')
    plt.figure(figsize=(9,4))
    for name in ('greedy','final'):plt.plot(variants,[data[name]['summary']['scenario_means'][v]['coverage'] for v in variants],marker='o',label=name)
    plt.ylabel('Fraction of arrived members served');plt.title('Coverage: three episodes per scenario');plt.legend();save('04_coverage','results/recovery/{greedy,final}.json')
    plt.figure(figsize=(7,4))
    for name in ('greedy','final'):
        waits=[w for r in data[name]['episodes'] for w in r['first_introduction_wait_days']];plt.hist(waits,bins=range(0,65,5),histtype='step',linestyle='--' if name=='final' else '-',label=f'{name}: n={len(waits)}')
    plt.xlabel('Days until first introduction');plt.ylabel('Served members');plt.title('Conditional waiting; unserved members excluded');plt.legend();save('05_waiting','results/recovery/{greedy,final}.json')
    plt.figure(figsize=(7,4));labels=['V0_frozen','A_future'];plt.bar(labels,[screen[n]['summary']['primary_score'] for n in labels]);plt.ylabel('MSMI / 100 arrivals');plt.title('Future term: 18 screening validation episodes per arm');save('06_future','results/recovery/screen/{V0_frozen,A_future}.json')
    plt.figure(figsize=(7,4));plt.bar(names,[d['summary']['overall']['ask_cost'] for d in data.values()]);plt.ylabel('Clarification units / episode');plt.title('Official subprocess benchmark: n=18 per policy');save('11_clarification','results/recovery/*.json')
    plt.figure(figsize=(7,4))
    for name in ('greedy','final'):plt.hist([r['inference_seconds'] for r in data[name]['episodes']],histtype='step',label=name,bins=10)
    plt.xlabel('Inference seconds per complete episode');plt.ylabel('Episodes');plt.title('Host subprocess timing, concurrent runs; n=18 per policy');plt.legend();save('12_runtime','results/recovery/{greedy,final}.json')
    write('figures/recovery/catalog.json',catalog)
    (out/'README.md').write_text('Generated with `python -m experiments.recovery_report`. Sources and captions are embedded in catalog.json and each plot. These figures describe the recovery release. Historical pruning, calibration and disclosure figures 07–10 remain unchanged because their underlying data and model did not change. No chart implies statistical significance.\n',encoding='utf-8')

if __name__=='__main__':main()
