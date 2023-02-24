#!/usr/bin/python3

import subprocess
import time
import re

fuzz_target = '/home/user/TEST/test/TEST'
time_limit = 7200

process = subprocess.Popen(fuzz_target, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
coverage = 0
start_time = time.time()
for line in process.stdout:
    print(line)
    if 'cov:' in line:
        new_coverage = int(re.search(r'cov: (\d+)', line).group(1))
        if new_coverage > coverage:
            coverage = new_coverage
            start_time = time.time()
        else:
            if time.time() - start_time > time_limit:
                process.terminate()
