#!/usr/bin/python3

import subprocess
import argparse
import os
from time import time
from re import search, sub


parser = argparse.ArgumentParser(description='LibFuzzer Time Checker')

parser.add_argument('-L', '--libfuzzer_target', metavar='[path/libfuzzer_target]', type=str, required=True)
parser.add_argument('-c', '--corpus', metavar='[path/corpus_directory]', type=str, help="corpus directory path")
parser.add_argument('-t', '--time', metavar='[time in seconds]', type=int, required=True, help="time in seconds to fuzz without new cov")
parser.add_argument('-a', '--args', metavar='[additional libfuzzer arguments]', nargs="*", type=str, help="additional arguments for libfuzzer target")
parser.add_argument('-o', '--output', metavar='[output_file.log]', type=str, help="optional file to write output to")

args = parser.parse_args()
fuzz_target = [args.libfuzzer_target]

if args.args is not None:
    additional_args = ["-" + x for x in args.args]
    fuzz_target += additional_args

if args.corpus is not None:
    fuzz_target.append(args.corpus)

time_limit = args.time

output_file = None
if args.output:
    output_file = open(args.output, 'w', buffering=1, encoding='utf-8')

def log_line(text):
    print(text)
    if output_file:
        output_file.write(text + '\n')
        output_file.flush()

process = subprocess.Popen(fuzz_target, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
coverage = 0
start_time = time()

try:
    for line in iter(process.stdout.readline, ''):
        line = line.rstrip('\n')
        if 'cov:' in line:
            match = search(r'cov: (\d+)', line)
            if match:
                new_coverage = int(match.group(1))
                dt = int(time() - start_time)
                ft = '%02i:%02i:%02i' % (dt // 3600, (dt % 3600) // 60, dt % 60)
                new_line = sub(r'(cov: (\d+))', r'\1 (last: ' + ft + r')', line)
                log_line(new_line)
                if new_coverage > coverage:
                    coverage = new_coverage
                    start_time = time()
                else:
                    if time() - start_time > time_limit:
                        process.terminate()
                        break
            else:
                log_line(line)
        else:
            log_line(line)
finally:
    if output_file:
        output_file.close()