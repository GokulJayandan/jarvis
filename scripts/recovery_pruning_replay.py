"""Repeat all exact pruning cases, preserving original results and timings."""
import json
from unittest.mock import patch
from experiments import run_pruning
from experiments.common import ROOT,write

def main():
    original=json.loads((ROOT/'results/pruning/regret.json').read_text())
    def save(path,obj):write('results/recovery/pruning_reproduced.json',obj)
    with patch.object(run_pruning,'write',side_effect=save):run_pruning.main()
    repeated=json.loads((ROOT/'results/recovery/pruning_reproduced.json').read_text())
    assert len(original['rows'])==len(repeated['rows'])==540
    ignored={'oracle_seconds','pruned_seconds','peak_python_bytes'}
    for a,b in zip(original['rows'],repeated['rows']):
        assert {k:v for k,v in a.items() if k not in ignored}=={k:v for k,v in b.items() if k not in ignored}
    print('540 exact pruning comparisons reproduced; all portfolios, utility values and regrets match.')

if __name__=='__main__':main()
