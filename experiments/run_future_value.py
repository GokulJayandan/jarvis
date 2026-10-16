"""Required paired future-value comparison on fresh, non-selection seeds."""
from experiments.run_suite import run
from experiments.common import write,paired_ci
from evaluate import VARIANTS

if __name__=='__main__':
    seeds=[13001,13002,13003]
    # Keep all selected components fixed; only the preregistered coefficient changes.
    # Fresh outcomes are reporting evidence and cannot reselect the frozen policy.
    a=run('final',seeds,VARIANTS,'results/future/present.json',overrides={'future_weight':0.0})
    b=run('final',seeds,VARIANTS,'results/future/future.json',overrides={'future_weight':0.5})
    write('results/future/paired.json',dict(seeds=seeds,msmi=paired_ci(b['episodes'],a['episodes']),
        coverage=paired_ci(b['episodes'],a['episodes'],'coverage'),
        ask_cost=paired_ci(b['episodes'],a['episodes'],'ask_cost')))
