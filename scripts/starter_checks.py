from run_logged import run

for label, command in [
    ('starter_tests', ['python', '-m', 'unittest', '-v']),
    ('starter_data', ['python', 'verify_data.py']),
    ('starter_smoke', ['python', 'evaluate.py', '--seeds', '101', '--output', 'results/starter_smoke.json']),
]:
    if run(label, command) != 0:
        raise SystemExit('Starter failure: ' + label)
for baseline in ['greedy', 'no_asks', 'random']:
    if run('baseline_' + baseline, ['python', 'evaluate.py', '--baseline', baseline,
           '--seeds', '101,102,103', '--variants', 'all', '--output', 'results/' + baseline + '.json']) != 0:
        raise SystemExit('Baseline failure: ' + baseline)
