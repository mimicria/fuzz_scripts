import os
import json

example_dir = '.'
with os.scandir(example_dir) as files:
    subdir = [file.name for file in files if file.is_dir()]

for module in subdir:
    print ("==== " + module + " ====")
    statfile = "./" + module + "/FUZZ-MASTER_0/fuzzer_stats.json"
    f = open(statfile)
    data = json.load(f)
    pf = data['paths_found']
    pi = data['processed_inputs']
    state = "[+]" if (pf > (pi*2)) else "[-]"
    print(f"{state} Paths found/inputs: {pf}/{pi}")
    ed = data['execs_done']
    state = "[+]" if (ed > 100000) else "[-]"
    print(f"{state} Execs done: {ed}")
    lu = data['last_update']
    lp = data['last_path']
    td = (lu - lp)/3600
    state = "[+]" if (td > 2) else "[-]"
    print(f"{state} Last found: {td}")
    f.close()
