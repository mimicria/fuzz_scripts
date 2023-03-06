#!/usr/bin/python3

import subprocess
import argparse
import os
from time import time
from re import search,sub


parser = argparse.ArgumentParser(description = 'LibFuzzer Time Checker')

parser.add_argument('-L', '--libfuzzer_target', metavar='[path/libfuzzer_target]', type=str, required=True)
parser.add_argument('-c', '--corpus', metavar='[path/corpus_directory]',  type=str,help="corpus directory path")     
parser.add_argument('-t', '--time', metavar='[time in seconds]',  type=int, required=True,help="time in seconds to fuzz without new cov") 
parser.add_argument('-a', '--args', metavar='[additional libfuzzer arguments]',nargs="*",  type=str,help="additional arguments for libfuzzer target") 

args = parser.parse_args()
fuzz_target = [args.libfuzzer_target]

if args.args!=None:
     additional_args = ["-" + x for x in args.args]
     fuzz_target+=additional_args
(fuzz_target.append(args.corpus) if args.corpus is not None else None)

time_limit = args.time

process = subprocess.Popen(fuzz_target, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
coverage = 0
start_time = time()
for line in iter(process.stdout.readline,''):
     line = line.replace("\n","")
     if 'cov:' in line:
          new_coverage = int(search(r'cov: (\d+)', line).group(1))
          dt = int(time() - start_time)
          ft = '%02i:%02i:%02i' % (dt//3600, (dt%3600)//60, dt%60)
          new_line = sub(r'(cov: (\d+))', r'\1 (last: '+ft+r')', line)
          print(new_line)
          if new_coverage > coverage:
               coverage = new_coverage
               start_time = time()
          else:
               if time() - start_time > time_limit:
                    process.terminate()
     else:
          print(line)
