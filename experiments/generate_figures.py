"""Twelve reproducible evidence figures, exclusively from stored measured results."""
import collections
import json
from pathlib import Path
import statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from experiments.common import ROOT,write

def read(path):
    p=ROOT/path
    return json.loads(p.read_text()) if p.exists() else None

def main():
    if (ROOT/'results/recovery/release_checks_complete.json').exists():
        from experiments.recovery_report import main as recovery
        return recovery()
    folder=ROOT/'figures';folder.mkdir(exist_ok=True)
    plt.rcParams.update({'figure.dpi':140,'font.size':9,'axes.spines.top':False,'axes.spines.right':False})
    catalog=[]
    def save(name,caption,sources):
        plt.tight_layout();plt.savefig(folder/(name+'.png'));plt.close()
        catalog.append(dict(file='figures/'+name+'.png',caption=caption,sources=sources))
    sources={name:read('results/'+name+'.json') for name in ('greedy','no_asks','random','final')}
    available={k:v for k,v in sources.items() if v and v['summary'].get('eligible')}
    if available:
        names=list(available);fig,ax=plt.subplots(figsize=(7,4))
        ax.bar(names,[available[n]['summary']['primary_score'] for n in names],color=['#6686a3','#a7b8c5','#8477ad','#007f8b'][:len(names)])
        ax.set_ylabel('MSMI / 100 arrived members');ax.set_title('Official primary score · 18 episodes per policy')
        save('01_baseline_comparison','Equal weighting of six families; three matched seeds per family. Low event counts limit inference.',list('results/'+n+'.json' for n in names))
        variants=list(next(iter(available.values()))['summary']['scenario_means'])
        fig,ax=plt.subplots(figsize=(9,4))
        for n,data in available.items():ax.plot(variants,[data['summary']['scenario_means'][v]['msmi_per_100_arrived_members'] for v in variants],marker='o',label=n)
        ax.legend();ax.set_ylabel('MSMI / 100 arrived members');ax.set_title('Scenario outcomes · n=3 episodes per point')
        save('02_scenarios','Public families and matched seeds; zero MSMI is an observed zero, not evidence of equivalence.',list('results/'+n+'.json' for n in names))
        fig,ax=plt.subplots(figsize=(7,4))
        for n,data in available.items():
            ax.scatter([r['dates'] for r in data['episodes']],[r['mutual_second_meeting_intention'] for r in data['episodes']],label=n,alpha=.7)
        ax.legend();ax.set_xlabel('Completed meetings / episode');ax.set_ylabel('Qualifying MSMI pairs / episode')
        save('03_outcome_funnel','Each point is an official full episode; overlapping points are possible.',list('results/'+n+'.json' for n in names))
        fig,ax=plt.subplots(figsize=(9,4))
        for n,data in available.items():ax.plot(variants,[100*data['summary']['scenario_means'][v]['coverage'] for v in variants],marker='o',label=n)
        ax.legend();ax.set_ylabel('Arrived members introduced (%)');ax.set_title('Distinct-member coverage · n=3 episodes per point')
        save('04_coverage','Includes unserved members in the denominator; not a fairness certification.',list('results/'+n+'.json' for n in names))
        fig,ax=plt.subplots(figsize=(7,4))
        for n,data in available.items():
            waits=sorted(w for r in data['episodes'] for w in r['first_introduction_wait_days'])
            if waits:ax.step(waits,[(i+1)/len(waits) for i in range(len(waits))],where='post',label=f'{n} (served n={len(waits)})')
        ax.legend();ax.set_xlabel('Days from arrival to first introduction');ax.set_ylabel('Fraction of served members')
        save('05_waiting','Conditional on being served. Unserved counts are reported separately in the report.',list('results/'+n+'.json' for n in names))
        fig,ax=plt.subplots(figsize=(9,4))
        for n,data in available.items():ax.plot(variants,[data['summary']['scenario_means'][v]['ask_cost'] for v in variants],marker='o',label=n)
        ax.legend();ax.set_ylabel('Clarification units / episode');ax.set_title('Budget expenditure · n=3 episodes per point')
        save('11_clarification','Hard bundle costs 3; soft question costs 1. Maximum 720 units per episode.',list('results/'+n+'.json' for n in names))
    present=read('results/future/present.json');future=read('results/future/future.json')
    if present and future:
        a={(r['variant'],r['seed']):r for r in present['episodes']}
        groups=collections.defaultdict(list)
        for r in future['episodes']:groups[r['variant']].append(r['msmi_per_100_arrived_members']-a[r['variant'],r['seed']]['msmi_per_100_arrived_members'])
        fig,ax=plt.subplots(figsize=(9,4))
        ax.bar(list(groups),[statistics.mean(x) for x in groups.values()]);ax.axhline(0,color='black',lw=.8)
        ax.set_ylabel('Future − present MSMI / 100');ax.set_title('Fresh-seed paired effect · n='+str(len(next(iter(groups.values()))))+' per family')
        save('06_future_effect','Paired full episodes; intervals and seed-cluster limitations appear in the report.',['results/future/present.json','results/future/future.json'])
    regret=read('results/pruning/regret.json')
    if regret:
        groups=collections.defaultdict(list)
        for r in regret['rows']:groups[r['candidate_limit']].append(r)
        limits=sorted(groups)
        fig,ax=plt.subplots(figsize=(7,4));ax.plot(limits,[statistics.mean(r['absolute_regret'] for r in groups[l]) for l in limits],marker='o',label='Mean')
        ax.plot(limits,[max(r['absolute_regret'] for r in groups[l]) for l in limits],marker='s',label='Maximum')
        ax.legend();ax.set_xlabel('Candidate limit');ax.set_ylabel('Surrogate utility lost');ax.set_title(f'Exact small-state pruning study · {len(regret["rows"])} comparisons')
        save('07_pruning_regret','Regret is against exact portfolio enumeration of the same surrogate, not actual MSMI.',['results/pruning/regret.json'])
        fig,ax=plt.subplots(figsize=(7,4))
        for l in limits:ax.scatter(statistics.mean(r['pruned_seconds'] for r in groups[l])*1000,statistics.mean(r['absolute_regret'] for r in groups[l]),label=f'limit {l}')
        ax.legend();ax.set_xlabel('Mean search time (ms)');ax.set_ylabel('Mean surrogate regret')
        save('08_pruning_runtime','Python wall-clock search only; oracle peak allocations and runtime are recorded in raw data.',['results/pruning/regret.json'])
    calibration=read('results/calibration/metrics.json')
    if calibration:
        fig,axes=plt.subplots(1,2,figsize=(10,4))
        for ax,target in zip(axes,('directional','msmi')):
            for row in calibration['targets']:
                if row['target']==target and row['stratum']=='all':
                    bins=row['bins'];ax.plot([b['p'] for b in bins],[b['observed'] for b in bins],marker='o',label=row['model']+(' calibrated' if row['calibrated'] else ''))
                    if row['calibrated']:
                        ax.errorbar([b['p'] for b in bins],[b['observed'] for b in bins],yerr=[[b['observed']-b['ci95'][0] for b in bins],[b['ci95'][1]-b['observed'] for b in bins]],fmt='none',alpha=.3,capsize=2,color='green')
            ax.plot([0,1],[0,1],':',color='gray');ax.set_xlabel('Mean predicted event probability');ax.set_ylabel('Observed event frequency');ax.set_title(target);ax.legend(fontsize=7)
            aggregate=next(r for r in calibration['targets'] if r['target']==target and r['stratum']=='all')
            ax.set_title(target+f' · n={aggregate["n"]}, events={aggregate["positives"]}')
            if target=='msmi':ax.set_xlim(0,.15);ax.set_ylim(0,.15)
        save('09_reliability','Held-out baseline-selected pairs; equal-frequency bins. Pair dependence and selection bias remain.',['results/calibration/metrics.json'])
        rows=[r for r in calibration['targets'] if r['target']=='directional' and r['model']=='logistic' and r['calibrated'] and r['stratum']!='all']
        fig,ax=plt.subplots(figsize=(8,4));ax.bar([r['stratum']+'\nn='+str(r['n']) for r in rows],[r['brier'] for r in rows]);ax.set_ylabel('Directional recorded-Yes Brier score')
        save('10_disclosure_calibration','Strata concern observed soft-field status at decision time; lower Brier is better.',['results/calibration/metrics.json'])
    resources=read('results/robustness/resources.json')
    if resources:
        adversarial=read('results/robustness/adversarial.json');calls=resources['calls']+(adversarial['calls'] if adversarial else [])
        fig,ax=plt.subplots(figsize=(7,4));ax.hist([r['seconds'] for r in calls],bins=16);ax.axvline(10,color='red',linestyle='--',label='Official 10 s limit')
        ax.set_xlabel('Windows subprocess invocation seconds');ax.set_ylabel('Calls');ax.set_title(f'n={len(calls)} sampled invocations');ax.legend()
        save('12_runtime','Includes startup, protocol IO and dense adversarial states. Not a container resource-enforcement result.',['results/robustness/resources.json','results/robustness/adversarial.json'])
    write('figures/catalog.json',catalog)
    (folder/'README.md').write_text('# Reproducible experiment figures\n\nGenerate with `python -m experiments.generate_figures`.\n\n'+
        '\n\n'.join('['+Path(x['file']).stem+']('+Path(x['file']).name+') — '+x['caption']+' Sources: '+', '.join('`'+s+'`' for s in x['sources'])+'.' for x in catalog)+'\n',encoding='utf-8')

if __name__=='__main__':main()
