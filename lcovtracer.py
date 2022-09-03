#!/usr/bin/python3

import os.path as path
import sys

#tfile = '/home/user/fuzzj/out/cov/lcov/trace.lcov_info_final'
tfile = sys.argv[1]
thereisnewfile = False

with open(tfile+'.res',"wt") as outf:
    with open(tfile, 'rt') as inf:
        for str in inf:
            if thereisnewfile:
                thereisnewfile = False
                if str.startswith('SF:'):
                    fname = str[3:-1]
                    if path.exists(fname):
                        print('[+]', fname)
                        found = True
                        seq = [nfstr,str]
                        outf.writelines(seq)
                        continue
                    else:
                        print('[-]', fname)
                        found = False
                        continue
            if str.startswith('TN:'):
                thereisnewfile = True
                nfstr = str
                continue
            else:
                if found:
                    seq = [str]
                    outf.writelines(seq)
                    continue
                else:
                    continue
