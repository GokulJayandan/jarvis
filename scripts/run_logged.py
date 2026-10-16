"""Execute a command, retaining its exact arguments, output, time and exit status."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]

def run(label, command):
    target = ROOT / 'results' / 'execution'
    target.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    record = {'command': command, 'cwd': str(ROOT), 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    env = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8')
    env['PATH'] = str(Path(sys.executable).parent) + os.pathsep + env['PATH']
    with (target / (label + '.log')).open('w', encoding='utf-8') as log:
        try:
            result = subprocess.run(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
            record['exit_code'] = result.returncode
        except OSError as error:
            log.write(str(error))
            record.update(exit_code=None, error=str(error))
    record['seconds'] = time.perf_counter() - started
    record['log_sha256'] = hashlib.sha256((target / (label + '.log')).read_bytes()).hexdigest()
    (target / (label + '.json')).write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record), flush=True)
    return record.get('exit_code')

if __name__ == '__main__':
    code=run(sys.argv[1], sys.argv[2:])
    raise SystemExit(127 if code is None else code)
