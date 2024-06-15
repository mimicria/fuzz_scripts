import time
import requests
import os
import re
import sys
import shutil

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    requests.post(url, data=data)

# in: directory to find afl stats file
# out: full filepath to afl stats file
def get_fuzzer_stats_file(start_path):
    for root, dirs, files in os.walk(start_path):
        if 'fuzzer_stats' in files:
            file_path = os.path.join(root, 'fuzzer_stats')
            return file_path
    return None

# in: afl stats file
# out: `values` dict with needed stats
def get_fuzzer_stats(sfile):
    values = {}
    with open(sfile, 'r') as file:
        for line in file:
            if line.startswith('saved_crashes'):
                saved_crashes = line.split(':')[1].strip()
                values['saved_crashes'] = int(saved_crashes)
            elif line.startswith('afl_banner'):
                afl_banner = line.split(':')[1].strip()
                values['afl_banner'] = afl_banner
            elif line.startswith('last_update'):
                last_update = int(line.split(':')[1].strip())
            elif line.startswith('last_find'):
                last_find = int(line.split(':')[1].strip())
    time_wo_finds = (last_update - last_find) // 60
    values['time_wo_finds'] = time_wo_finds
    return values

# out: string with free/total space on hard drive
def get_df():
    total, used, free = shutil.disk_usage("/")
    out_str = f'Disk space free: {100 * free // total}% = {free // (2**30)} GiB'
    return out_str

telegram_token = os.getenv('TBOT_TOKEN')
if not telegram_token:
    print('Error: set environment variable TBOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11')
    exit()
chat_id = os.getenv('TCHAT_ID')
if not telegram_token or not chat_id:
    print('Error: set environment variable TCHAT_ID=@MyChannelName')
    exit()
if len(sys.argv) < 2:
    print('Error: needed option [path/to/afl/outdir]')
    exit()

start_path = sys.argv[1]
last_crashes = 0
check_period = 900 # 15 mins
hcounter = 0

sfile = get_fuzzer_stats_file(start_path)
if sfile == None:
    print('Error: no AFL fuzzer_stats file found')
    exit()
while True:
    statsd = get_fuzzer_stats(sfile)
    print(statsd)
    if statsd['saved_crashes'] > last_crashes:
        print("Saved crashes > last_crashes")
        hcounter = 0
        last_crashes = statsd['saved_crashes']
        print(f"hcounter = {hcounter}, last_crashes = {last_crashes}")
    if hcounter == 0:
        df = get_df()
        print("Send message")
        send_telegram_message("AFL-fuzz is running.\n\
        Target: " + statsd['afl_banner'] + "\n\
        Crashes: " + str(statsd['saved_crashes']) + "\n\
        EOT: " + str(statsd['time_wo_finds']) + " min\n" + df + "\n")
    if statsd['time_wo_finds'] == 120:
        print("Exit on time")
        send_telegram_message("AFL-fuzz process has stopped by EOT for " + statsd['afl_banner'])
        exit()
    hcounter = (hcounter + 1) % 4
    print(f"hcounter = {hcounter}, goto sleep")
    time.sleep(check_period)
