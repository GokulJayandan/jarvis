"""Generate reviewer tables from measured JSON, never from manually typed scores."""
import collections
import json
from pathlib import Path
import statistics
from experiments.common import ROOT,write,paired_ci

def read(path):
    p=ROOT/path
    return json.loads(p.read_text()) if p.exists() else None

def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join('---' for _ in headers)+' |']+
                     ['| '+' | '.join(str(v) for v in row)+' |' for row in rows])

def fmt(x):return 'Not evaluated' if x is None else f'{x:.4f}'

def main():
    report=[]
    def section(title,body):report.append('## '+title+'\n\n'+body+'\n')
    report.append('# RAVEN-Match — Recoverability-Aware Vertex Elicitation and Sequential Allocation\n\n'
        'Team Jarvis: GokulJayandan R S, Keerthana Janakiraman, Mridula B, Boomika L.\n'
        'Round 2, synthetic Sequential Matching Problem. Generated from stored experiment files.\n')
    data={n:read('results/'+n+'.json') for n in ('greedy','no_asks','random','final')}
    selection=read('results/selection.json')
    final=data['final'];resources=read('results/robustness/resources.json');cal=read('results/calibration/metrics.json');regret=read('results/pruning/regret.json')
    chosen=selection['winner'] if selection else 'NOT SELECTED'
    score=final['summary'].get('primary_score') if final else None
    baseline_comparison=''
    if final and data['greedy']:
        baseline_comparison=f'Official greedy scored {data["greedy"]["summary"]["primary_score"]:.4f}; the frozen policy does not demonstrate an improvement on the mandatory test sample. '
    section('1. Abstract',f'The frozen selected configuration is **{chosen}**. Its official public score is **{fmt(score)} MSMI per 100 arrived members**. '
        +baseline_comparison+'We investigate joint clarification, candidate pruning and persistent future information value. Hard eligibility is enforced independently of estimates. '
        'Results concern invented simulator outcomes only. Docker execution is blocked on this host; this build must not be represented as submission-ready until that gate passes.')
    section('2. Problem definition','At each day the policy selects immediate clarifications within 12 units, then allocates available confirmed-feasible pairs. '
        'A qualifying outcome requires a date within 30 days and two Yes second-meeting reports within three days of that date. The primary outcome is pair-level MSMI / arrived members × 100. '
        'Sixty decision days are followed by forty days with no introductions. Unserved and departed members remain in the denominator.')
    section('3. Research questions','Does joint elicitation recover complementary opportunities? Does a training-derived future-arrival term improve fresh episodes? '
        'How much surrogate utility does screening discard? Do calibrated observable-feature predictions outperform pooled frequencies on held-out selected pairs?')
    section('4. Related work and references','Global allocation uses Edmonds-style blossom/primal-dual matching via NetworkX 3.6.1 (BSD-3-Clause). '
        'See [NetworkX matching source](https://github.com/networkx/networkx/blob/networkx-3.6.1/networkx/algorithms/matching.py) and its reference to Galil (1986). '
        'Our portfolio objective is a bounded heuristic, with no submodularity or approximation guarantee. '
        'The authoritative benchmark is [official release source](https://github.com/RomeoJulietLove/The-Sequential-Matching-Problem/tree/a8e26b35118cfa8e886a02f93984923e43ab64f6).')
    train=read('results/training/observations.json');val=read('results/training/validation_observations.json')
    section('5. Official data and evaluation setup',f'Upstream commit: `a8e26b35118cfa8e886a02f93984923e43ab64f6`, release 1.0.0. '
        f'Training rollouts: {train["episodes"] if train else "Not evaluated"} episodes, {len(train["rows"]) if train else "Not evaluated"} selected introductions. '
        f'Calibration-validation rollouts: {val["episodes"] if val else "Not evaluated"} episodes, {len(val["rows"]) if val else "Not evaluated"} introductions. '
        'Sources: `results/training/{observations,validation_observations}.json`; seed registry: `configs/seeds.json`. '
        'Six manifest training pools, two validation and two development-test pools remain separate. Static day-30 fields are never used as day-zero features. '
        'Official evaluator and simulator source are unchanged. Private worlds were not accessed or generated.')
    section('6. Feasibility and hard constraints','The independent checker enforces reciprocal age, explicit gender preferences, zone, smoking and existing-children restrictions; '
        'relationship structures must agree, explicit yes/no children-plan conflicts fail, and schedules must overlap. All hard values must be known. '
        'Known failure takes priority over missingness. Same member, cross-pool and underage pairs fail. Availability and prior introductions are separate filters. '
        'Tests exhaust all 2^11 missing-field masks at each endpoint and compare thousands of randomized public profiles with `kit.eligibility`.')
    section('7. Two-graph architecture','Confirmed edges alone reach `allocate`. Potential edges represent pairs with unresolved recoverable hard constraints. '
        'Declined hard fields are excluded from the recoverable planning subgraph. Explicit edge types and an output sanitizer prevent potential-edge allocation. '
        'The official simulator performs the final independent atomic action validation.')
    section('8. Probability and disclosure modelling','Four regularized logistic targets estimate recorded directional Yes, joint Yes, a completed date and qualifying MSMI directly. '
        'Pair predictions are symmetric; directional probabilities are not multiplied. Pooled Jeffreys estimates are a real ablation. '
        'The 35 features include soft agreement, disagreement, separate endpoint missingness, refusal/not-asked fractions, current day and age gap. '
        'Validation-only intercept calibration is regularized. Labels are collected after day 100. Missing responses are zero only for explicitly recorded-event targets; '
        'they are never labelled as negative personal preferences. Selection bias remains because only introduced pairs have outcomes. '
        'Disclosure follows exact official status semantics: non-declined requests disclose immediately; declined values remain unavailable.')
    section('9. Joint clarification objective','For question set Q, `U(Q) = V_greedy(C ∪ P_unlocked(Q)) + λ Σ L_i(t)`. '
        'Potential edge weight is predicted MSMI times empirical-Bayes feasibility after revelation. An edge becomes available to this surrogate only when every required endpoint bundle is selected. '
        'Cost is a hard constraint (3 per bundle, daily budget 12); ties prefer fewer questions. This allocates expected edge weights and is not exact expected post-answer matching utility. '
        'No unknown or sampled edge is ever introduced.')
    section('10. Portfolio search and pruning','Production screens candidates by incident opportunity and preserves high-value complementary endpoint groups, then enumerates up to four bundles within a fixed work cap. '
        'The full-episode unpruned comparator has a 2,000-portfolio cap and is approximate. The separate small-state oracle is exhaustive and exact for the declared surrogate. '
        'P1 random valid bundles, P2 endpoint, P3 singleton VOI and joint portfolios are genuinely different implementations.')
    section('11. Persistent future-arrival value','The future term uses training-observed arrival counts after day t, zone frequencies, pooled reciprocal feasibility and MSMI priors, '
        'a bounded survival discount and remaining horizon. It sees no actual future members. Coefficients 0, 0.5 and 2 are evaluated on validation seeds. '
        'The approximation omits detailed future competition and individual dropout risk. It becomes zero after the latest training-supported arrival day.')
    section('12. Matching optimization','Confirmed weights are predicted qualifying-event probabilities, optionally plus a waiting term. '
        'Exact general-graph matching uses the vendored NetworkX blossom body with integer-scaled weights. A minimal adapter avoids importing NetworkX at inference. '
        'Brute-force small-graph checks, odd cycles and larger NetworkX differential tests validate the adapter. Greedy matching is a configuration ablation. '
        'No exponential matching routine is used on full states.')
    summary_rows=[];scenario_rows=[]
    for name,obj in data.items():
        if not obj:continue
        rows=[r for r in obj['episodes'] if r.get('valid')]
        summary_rows.append([name,len(rows),sum(r['mutual_second_meeting_intention'] for r in rows),sum(r['arrived_members'] for r in rows),fmt(obj['summary'].get('primary_score')),fmt(obj['summary'].get('overall',{}).get('coverage'))])
        groups=collections.defaultdict(list)
        for r in rows:groups[r['variant']].append(r)
        for variant,rs in groups.items():
            scenario_rows.append([name,variant,len(rs),sum(r['arrived_members'] for r in rs),sum(r['assignments'] for r in rs),sum(r['mutual_acceptances'] for r in rs),sum(r['dates'] for r in rs),sum(r['mutual_second_meeting_intention'] for r in rs),fmt(statistics.mean(r['msmi_per_100_arrived_members'] for r in rs)),fmt(statistics.mean(r['coverage'] for r in rs)),sum(r['ask_cost'] for r in rs),sum(r['missing_feedback'] for r in rs)])
    section('13. Official baselines',table(['Policy','Valid episodes','MSMI pairs','Arrived members','Official score','Mean coverage'],summary_rows)+'\n\n'
        'Sources: `results/{greedy,no_asks,random,final}.json`. Every required arm uses seeds 101,102,103 across all six families. '
        'Baselines were executed before replacing the starter entrypoint; `official_policy.py` reproduces them afterward. Scores average family means equally, not pooled family denominators.')
    section('14. Experimental protocol','See `docs/EXPERIMENT_PROTOCOL.md`. Models are fit on training data, intercepts calibrated on validation, and configurations selected on the two manifest validation seeds. '
        'The configuration is frozen in `raven/assets/final_config.json` before final reporting. Validation and research use the unchanged `evaluate.episode` with a labelled in-process JSON adapter; '
        'mandatory final/baseline runs use actual subprocesses. In-process runtime is not comparable to container or subprocess runtime. '
        'Multiple candidate selection and few independent seeds require caution. All attempted runs and negative results remain available.')
    section('15. Overall and scenario-level results',table(['Policy','Family','n','Arrived','Introductions','Mutual Yes','Dates','MSMI','MSMI/100','Coverage','Ask units','Missing feedback'],scenario_rows)+'\n\n'
        'Counts are summed within each row; coverage and MSMI/100 are episode means. Source files are the same as Section 13. '
        'A zero MSMI count is a measured zero in a rare-event pipeline and does not establish policy equivalence.')
    comparisons={}
    if final:
        for n in ('greedy','no_asks','random'):
            if data[n]:comparisons[n]=paired_ci(final['episodes'],data[n]['episodes'])
    report.append('Paired final-minus-baseline differences (MSMI/100; seed-cluster percentile bootstrap):\n\n'+table(['Baseline','Episodes','Seed clusters','Difference','95% interval'],[[n,r['n_episodes'],r['n_seed_clusters'],fmt(r['mean_difference']),str([round(x,4) for x in r['ci95']])] for n,r in comparisons.items()])+'\n\nThree clusters give coarse, descriptive intervals; no private-leaderboard inference is justified.\n')
    extra=[]
    for path in ('results/raven/manifest_test.json','results/raven/fresh_test.json'):
        obj=read(path)
        if obj:extra.append([path,len(obj['episodes']),obj['summary']['eligible'],fmt(obj['summary'].get('primary_score'))])
    if extra:report.append('Additional frozen-policy test runs (official engine, in-process adapter):\n\n'+table(['Source','Episodes','All valid','MSMI/100'],extra)+'\n')
    future=read('results/future/paired.json')
    section('16. Future-value ablation',('Fresh-seed future-minus-present result: '+json.dumps(future['msmi'])+'\n\n'
        'Coverage effect: '+json.dumps(future['coverage'])+'; clarification-cost effect: '+json.dumps(future['ask_cost'])+'. '
        'Sources: `results/future/{present,future,paired}.json`. '+
        ('The interval includes zero; these runs do not establish a stable improvement.' if future['msmi']['ci95'][0]<=0<=future['msmi']['ci95'][1] else 'The measured interval excludes zero in this small public sample; generalization still requires caution.')) if future else 'Not evaluated.')
    joint_future=read('results/future_joint_reference/paired.json')
    if joint_future:report.append('The earlier joint-only policy comparison is retained separately at `results/future_joint_reference/`: '+json.dumps(joint_future['msmi'])+'. The main comparison above holds the selected soft-question configuration fixed and changes only the future coefficient. Neither fresh comparison changes the frozen choice.\n')
    if regret:
        groups=collections.defaultdict(list)
        for r in regret['rows']:groups[r['candidate_limit']].append(r)
        rows=[[limit,len(rs),fmt(statistics.mean(r['absolute_regret'] for r in rs)),fmt(max(r['absolute_regret'] for r in rs)),fmt(statistics.mean(r['absolute_regret']>1e-12 for r in rs)),fmt(statistics.mean(r['best_portfolio_excluded'] for r in rs)),fmt(1000*statistics.mean(r['pruned_seconds'] for r in rs))] for limit,rs in sorted(groups.items())]
        body=table(['Limit','Cases','Mean regret','Max regret','P(utility loss)','P(tied chosen optimum excluded)','Mean ms'],rows)+'\n\n'
        body+='Source: `results/pruning/regret.json`. All '+str(len(regret['rows']))+' comparisons use exact enumeration of the declared surrogate. Repeated candidate limits/budgets on one state are dependent. '
        body+='Excluding a particular tied optimum need not lose utility; both events are reported. Relative regret is null when the optimum is zero. This is not measured MSMI regret.'
    else:body='Not evaluated.'
    section('17. Pruning regret',body)
    if cal:
        rows=[[r['target'],r['model']+(' calibrated' if r['calibrated'] else ''),r['stratum'],r['n'],r['positives'],fmt(r['brier']),fmt(r['log_loss']),fmt(r['ece'])] for r in cal['targets']]
        body=table(['Target','Model','Disclosure stratum','n','Events','Brier','Log loss','ECE'],rows)+'\n\n'
        body+='Source: `results/calibration/metrics.json`, fresh seeds 13001–13002. Calibration is evaluated after fitting and frozen selection; this diagnostic does not retune the model. '
        body+='Reliability uses equal-frequency bins. Wilson bin intervals ignore within-world dependence and are descriptive. No unselected-pair calibration claim is made. '
        body+='Deterministic disclosure strata: '+json.dumps({k:{x:v[x] for x in ('n','brier') if x in v} for k,v in cal['disclosure_strata'].items()})+'. '
        body+='Gate-feasibility calibration: '+json.dumps({k:cal['gate'][k] for k in ('n','brier','log_loss','ece') if k in cal['gate']})+'.'
        aggregate={(r['target'],r['model'],r['calibrated']):r for r in cal['targets'] if r['stratum']=='all'}
        direction=aggregate['directional','logistic',True];prior_direction=aggregate['directional','prior',False]
        outcome=aggregate['msmi','logistic',True];prior_outcome=aggregate['msmi','prior',False]
        body+=f' Directional calibrated Brier is {direction["brier"]:.5f} versus pooled {prior_direction["brier"]:.5f}. '
        body+=f'MSMI calibrated Brier is {outcome["brier"]:.5f} versus pooled {prior_outcome["brier"]:.5f}, based on only {outcome["positives"]} events. '
        body+='Calibration does not improve every target or metric; the table retains negative evidence. No parameters were changed after these held-out diagnostics.'
    else:body='Not evaluated.'
    section('18. Calibration by disclosure strata',body)
    waits=[]
    for name,obj in data.items():
        if not obj:continue
        rows=[r for r in obj['episodes'] if r.get('valid')];ws=[w for r in rows for w in r['first_introduction_wait_days']]
        waits.append([name,len(ws),sum(r['unserved_members'] for r in rows),fmt(statistics.mean(ws)) if ws else 'undefined',statistics.median(ws) if ws else 'undefined',max(ws) if ws else 'undefined'])
    section('19. Coverage and waiting',table(['Policy','Served person-episodes','Unserved person-episodes','Mean wait days','Median wait days','Max wait days'],waits)+'\n\n'
        'Waiting is conditional on receiving an introduction, so low mean wait can coexist with poor coverage. Unserved members have no observed first-introduction time. '
        'Sources: the four official result JSONs. No demographic fairness claim is made.')
    tests=read('results/execution/final_tests.json')
    body='Final test command exit code: '+str(tests.get('exit_code') if tests else 'NOT TESTED')+'. Source: `results/execution/final_tests.{json,log}`. '
    if resources:
        adversarial=read('results/robustness/adversarial.json')
        calls=resources['calls']+(adversarial['calls'] if adversarial else []);body+=f'{len(calls)} measured subprocess calls, including dense adversarial fixtures; maximum {max(r["seconds"] for r in calls):.4f} s, maximum sampled RSS {max(r["peak_sampled_rss_bytes"] for r in calls)/1024**2:.2f} MiB; maximum request {max(r["request_bytes"] for r in calls)} bytes, response {max(r["response_bytes"] for r in calls)} bytes. '
        body+='Sources: `results/robustness/{resources,adversarial}.json`. RSS is sampled, not a guaranteed peak. These Windows measurements do not establish Docker-enforced limits. '
    body+='Docker build could not launch (executable missing), and official container evaluation exited 2. `results/container_check.json` is a failed check, not a successful benchmark. '
    body+='A portable Windows Python 3.12.7 run passed 53 standard-library compatibility tests (`results/execution/python312_compat.log`); this is not Linux/container verification. '
    body+='No runtime exceptions may be hidden during final evaluation: `RAVEN_STRICT=1` turns development fallback errors into failing subprocesses. Production fallback emits diagnostics to stderr and legal empty actions.'
    section('20. Runtime and reliability',body)
    ablations=[]
    if selection:
        for name,s in selection['all_candidates'].items():
            o=s['overall'];ablations.append([name,fmt(s['primary_score']),fmt(o['coverage']),fmt(o['ask_cost']),fmt(o['inference_seconds'])])
    section('21. Additional ablations',table(['Configuration','MSMI/100','Coverage','Ask units/episode','In-process seconds/episode'],ablations)+'\n\n'
        'Each configuration uses the same two validation seeds across all six families (12 episodes). '
        'Sources: `results/ablations/*.json`, selection record `results/selection.json`. Future changes λ only; calibration and prior variants change prediction; '
        'singleton/endpoint/random change clarification; greedy_match changes allocation; soft enables soft questions; waiting adds waiting utility. '
        'The unpruned arm removes screening but retains a work cap, so its reference is approximate. Multiple-testing risk applies to choosing the largest score.')
    section('22. Failure cases','See `docs/FAILURE_ANALYSIS.md`. Sparse supply, hard refusals, occupied members, overlapping opportunities and late feedback can prevent qualifying outcomes. '
        'Expected-edge-weight clarification ignores joint answer dependence. Learned probabilities have selective feedback, rare-event uncertainty and shift risk. '
        'Container validation is an actual unresolved blocker. Unit-test success does not prove private validity.')
    section('23. Limitations','This is synthetic evaluation, not social or clinical validation. Few independent seeds limit uncertainty estimates. '
        'Model selection reuses validation for calibration/configuration choice and compares several candidates. No held-out retuning is allowed. '
        'The future term is pooled and heuristic; the pruning oracle concerns small states and an approximate objective. '
        'Memory is intentionally empty because histories are cumulative; models do not adapt to evaluation feedback. '
        'The optional website was not started because mandatory Docker verification remains blocked.')
    section('24. Reproducibility','See `README.md`, `docs/REPRODUCIBILITY.md`, `configs/seeds.json`, pinned experiment dependencies, source fingerprints and execution logs. '
        'Generate figures with `python -m experiments.generate_figures` and this report with `python -m experiments.generate_report`. '
        'Inference is standard-library Python with a vendored solver and read-only JSON assets. There are no runtime APIs, GPUs or persistent files. '
        'The local measured interpreter is Python 3.14.6; the Dockerfile specifies Python 3.12.7, which requires actual container verification.')
    section('25. Software, data, model and AI provenance','Official MIT source and synthetic-data conditions are preserved. Vendored NetworkX retains BSD notices. '
        'Exact file and asset hashes: `results/provenance.json`. See `docs/{UPSTREAM_PROVENANCE,LICENSES,MODEL_CARD}.md`. '
        'New Team Jarvis work remains owned by its authors. OpenAI Codex assisted implementation and automated review. No human independent-review claim is made. '
        'Other teams’ source code was not used. No private organiser seeds or hidden state enter inference.')
    section('26. Conclusion',f'The selected public-validation configuration is {chosen}; measured final score is {fmt(score)} MSMI/100. '
        'The report preserves both positive and negative evidence. Local implementation and public evaluation must be distinguished from submission completion. '
        'A working offline Docker run and authorized publication of an immutable commit remain necessary before official submission.')
    target=ROOT/'report';target.mkdir(exist_ok=True)
    (target/'TECHNICAL_REPORT.md').write_text('\n'.join(report),encoding='utf-8')
    write('results/comparisons.json',comparisons)
    write('results/report_tables.json',dict(summary=summary_rows,scenario=scenario_rows,waiting=waits,ablations=ablations))

if __name__=='__main__':main()
