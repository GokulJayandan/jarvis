"""Re-run untouched official baselines after installing the custom adapter."""
import subprocess
import sys

if __name__=='__main__':
    for name in ('greedy','no_asks','random'):
        subprocess.run([sys.executable,'evaluate.py','--policy','official_policy.py','--baseline',name,
                        '--seeds','101,102,103','--variants','all','--output',f'results/{name}.json'],check=True)
