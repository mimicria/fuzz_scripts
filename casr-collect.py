#!/usr/bin/python3
# pip install termcolor


from os import walk, path
from sys import argv
from termcolor import colored

def get_filelist(report_dir):
    fl = []
    for root, dirs, files in walk(report_dir):
    	for file in files:
		    if(file.endswith(".casrep")):
			    fl.append(path.join(root,file))
    return fl

def get_severity_type(report):
    with open(report, 'r') as fd:
        for line in fd:
            if '\"Type\":' in line:
                type = line.split('\"')
                return type[3]

print(colored('CASR-collect', 'cyan'), '1.0', colored('by mimicria <mimicria@mail.ru>', 'blue'))
print('Crash report processing utility for afl-casr')
if len(argv) < 2:
    print(colored('[-]', 'red'), 'Option [REPORT_DIR] is needed')    
    exit()
report_dir = argv[1]
print(colored('[+]', 'green'), 'Collecting crash reports from:', colored(report_dir, 'white'))
fl = get_filelist(report_dir)
get_col = {'EXPLOITABLE': 'red', 'PROBABLY_EXPLOITABLE': 'yellow', 'NOT_EXPLOITABLE': 'green'}
for file in fl:
    type = get_severity_type(file)
    color = get_col.get(type, 'white')
    print(file, ':', colored(type, color))
