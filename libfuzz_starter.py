#!/usr/bin/python3

import subprocess
from time import time
from re import search
from sys import argv

if len(argv) < 3:
    print ("Usage: python libfuzz_starter.py [path/libfuzzer_target] [time in seconds to fuzz without new cov]\n \
  For example: python libfuzz_starter.py ~/test 7200")
    exit()

fuzz_target = argv[1]
time_limit = int(argv[2])

process = subprocess.Popen(fuzz_target, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
coverage = 0
start_time = time()
for line in process.stdout:
    print(line)
    if 'cov:' in line:
        new_coverage = int(search(r'cov: (\d+)', line).group(1))
        if new_coverage > coverage:
            coverage = new_coverage
            start_time = time()
        else:
            if time() - start_time > time_limit:
                process.terminate()
