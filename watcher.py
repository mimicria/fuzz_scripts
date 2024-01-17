
import psutil, time, datetime
while True:
    now = datetime.datetime.now()
    print("***", now)
    for proc in psutil.process_iter(['name']):
        pname = proc.info['name'].lower()
        if 'perl' in pname:
            try:
                pproc = proc.parent()
                if pproc is not None:
                    ppname = pproc.name().lower()
                    if 'afl-fuzz' not in ppname:
                        start_time = datetime.datetime.fromtimestamp(proc.create_time())
                        runtime = now - start_time
                        sec = int(str(runtime).split(':')[2].split('.')[0])
                        print("Process:", pname, "PID:", proc.pid, "Parent:", ppname, "Started at:", start_time, "Runtime:", str(runtime), end = '')
                        if sec > 15:
                            proc.terminate()
                            print(" ::: Kill...")
                        else:
                            print(" ::: OK")
            except:
                pass
    time.sleep(15)  # Wait for a second before checking again

