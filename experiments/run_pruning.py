"""Exact small-state regret for the declared surrogate, not MSMI regret."""
import itertools
import json
import time
import tracemalloc
from kit import generate,Simulator,baseline_asks
from raven.config import config
from raven.constraints import missing_hard,recoverable
from raven.graphs import build
from raven.portfolio import exhaustive
from raven.pruning import screen
from experiments.common import write

def main():
    rows=[];cfg=config('joint')
    for seed in [14001,14002,14003,14004]:
        for variant in ('development','sparse','cold_start'):
            for n in (12,24,36):
                sim=Simulator(generate(seed,n,'pruning',variant))
                state=sim.observe()
                confirmed,potential=build(state,cfg)
                candidates=sorted((m['member_id'],'constraints') for m in state['members'] if m['available'] and missing_hard(m) and recoverable(m))
                for budget in (3,6,12):
                    tracemalloc.start();start=time.perf_counter()
                    optimal,value,count,exact=exhaustive(candidates,budget,confirmed,potential)
                    runtime=time.perf_counter()-start;peak=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
                    for limit in (2,4,6,8,12):
                        kept=screen(candidates,potential,limit)
                        start=time.perf_counter();chosen,pruned,_,_=exhaustive(kept,budget,confirmed,potential)
                        rows.append(dict(seed=seed,variant=variant,members=n,budget=budget,candidate_limit=limit,
                            original_candidates=len(candidates),pruned_candidates=len(kept),optimal_portfolio=optimal,
                            pruned_portfolio=chosen,overlap=len(set(optimal)&set(chosen)),best_portfolio_excluded=not set(optimal)<=set(kept),
                            absolute_regret=max(0,value-pruned),relative_regret=(value-pruned)/value if value else None,
                            best_value=value,pruned_value=pruned,oracle_seconds=runtime,pruned_seconds=time.perf_counter()-start,
                            peak_python_bytes=peak,oracle_portfolios=count,reference_exact=exact))
    write('results/pruning/regret.json',dict(utility='Greedy disjoint expected-edge-weight sum after unlocking all required hard bundles. Exact exhaustive hard-bundle portfolio oracle; surrogate regret only.',
        scope='This surrogate assigns zero gain to soft questions, answered bundles and unrecoverable declined bundles. Such positive-cost actions are dominated by omission. Enumeration covers all remaining legal hard questions; it is not an oracle for a richer soft-information utility.',rows=rows))

if __name__=='__main__':main()
