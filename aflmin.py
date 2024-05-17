#!/usr/bin/python3
# pip install termcolor


from os import walk, path
import argparse
import re
import os
from termcolor import colored

def get_filelist(report_dir):
    fl = []
    pattern = re.compile(".+:id:.+,sig:.+,src.+,time:.+,execs:.+,op:.+,rep.+")
    for root, dirs, files in walk(report_dir):
    	for file in files:
		    if(re.match(pattern, file)):
			    fl.append(path.join(root,file))
    return fl


print(colored('AFLmin', 'cyan'), '1.0', colored('by mimicria <mimicria@mail.ru>', 'blue'))
parser = argparse.ArgumentParser(description = 'Crash minimizer utility for afl-collect with afl-tmin')
parser.add_argument('crashdir', metavar='PATH_CRASHES_DIR', type=str, help="path to crashes directory (checked_crashes after afl-collect)")
parser.add_argument('aflbin', metavar='FUZZ_COMMAND_LINE', nargs='*', type=str, help="path to program-under-test compiled with AFL instrumentation with @@ if needed")
args = parser.parse_args()

fl = get_filelist(args.crashdir)
if len(fl) == 0:
     print(colored('No crashes found in provided directory','red'))
     exit()

for file in fl:
    print(colored('[+]', 'green'), 'Minimizing:', colored(file, 'white'))
    new_file = file + '_minimized'
    run_str = 'afl-tmin -i ' + file + ' -o ' + new_file + ' -- ' + ' '.join(args.aflbin)
    os.system(run_str)
