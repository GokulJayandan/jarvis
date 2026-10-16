"""Sequential dependent research stages; safe to resume at completed stages."""
from pathlib import Path
from run_logged import run

root=Path(__file__).resolve().parents[1]
stages=[('validation','experiments.run_ablations','results/selection.json'),
        ('pruning','experiments.run_pruning','results/pruning/regret.json'),
        ('calibration','experiments.run_calibration','results/calibration/metrics.json'),
        ('future_value','experiments.run_future_value','results/future/paired.json'),
        ('robustness','experiments.run_robustness','results/robustness/resources.json')]
for label,module,result in stages:
    if (root/result).exists():continue
    if run(label,['python','-m',module])!=0:raise SystemExit('Stage failed: '+label)
