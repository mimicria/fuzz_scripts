#!/usr/bin/python3

import sys, os, subprocess

if len(sys.argv) > 1:
    path = sys.argv[1]
    dirlist = [f.path for f in os.scandir(path) if f.is_dir()]
    for i in dirlist:
        subprocess.run(['afl-plot', i, i.replace('out', 'plot')])