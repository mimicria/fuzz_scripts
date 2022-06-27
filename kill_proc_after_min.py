#!/usr/bin/python3
import psutil, time, sys

def kill_proc_after_time(process_name):
    maxtime=1
    pid_list = psutil.pids()
    for i in pid_list:
        proc = psutil.Process(i)
        pname = proc.name()
        if pname==process_name:
            cline = proc.cmdline()
            if cline[1].find('queue/id:')!=-1:
                ptime = proc.create_time()
                curr_time = time.time()
                diff = curr_time - ptime
                if diff/60 > maxtime:
                    proc.kill()

kill_proc_after_time(sys.argv[1])