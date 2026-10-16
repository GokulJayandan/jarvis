"""Wait for the local research selector, then execute mandatory final checks."""
from pathlib import Path
import subprocess
import sys
import time

root=Path(__file__).resolve().parents[1]
deadline=time.monotonic()+3600
while not (root/'results/selection.json').exists():
    if time.monotonic()>deadline:raise SystemExit('No completed selection within one hour')
    time.sleep(5)
subprocess.run([sys.executable,str(root/'scripts/finalize_local.py')],cwd=root,check=True)
for label,seeds,output in [('manifest_test','20261008,20261009','results/raven/manifest_test.json'),
                           ('fresh_final','13004,13005','results/raven/fresh_test.json')]:
    subprocess.run([sys.executable,str(root/'scripts/run_logged.py'),label,'python','-m','experiments.run_suite',
                    '--config','final','--seeds',seeds,'--variants','all','--output',output],cwd=root,check=True)
