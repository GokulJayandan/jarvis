"""Print reproducible local environment information without modifying the host."""
import json
import os
import platform
import shutil
import sys

if __name__ == '__main__':
    print(json.dumps({'python': sys.version, 'executable': sys.executable,
                      'platform': platform.platform(), 'cpu_count': os.cpu_count(),
                      'docker': shutil.which('docker')}, indent=2))
