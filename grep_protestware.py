#!/usr/bin/python3
# pip install python-magic

import sys, os
import magic
from progress.bar import Bar

words_to_check = ["protest", "peacenotwar", "node-ipc", "украин", "мобилиз", "агресс", "фсб", "войн", "воен", "зеленск", 
                  "напал", "санкци", "преступ", "путин", "убив", "ukrain", "putin", "russia", "крым", "crimea", "militar", "invasion"]

def get_filelist(directory):
    fl = []
    mime = magic.Magic(mime=True)
    for root, dirs, files in os.walk(directory):
    	for file in files:
            full_filename = root + "/" + file
            mime_type = mime.from_file(full_filename)
            if mime_type.startswith('text'):
    	        fl.append(full_filename)
    return fl

def contains_words(file_path, words):
    log = []
    try:
        with open(file_path, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                lower_line = line.lower()
                if len(lower_line) > 255:
                    continue
                for word in words:
                    if word in lower_line:
                        log.append(f"- `{word}` найдено в строке {line_number}: `{line.strip()}`")
        if log:
            log.insert(0, f"## Файл  {file_path}")
        return log
    except FileNotFoundError:
        print(f"Файл {file_path} не считан.", file=sys.stderr)
        return log
    except UnicodeDecodeError:
        print(f"Файл  {file_path} в непонятной кодировке.", file=sys.stderr)
        return log


if len(sys.argv) < 2:
    print(f'Usage: python3 {os.path.basename(sys.argv[0])} <directory>')
    exit(0)
path = sys.argv[1]
file_list = get_filelist(path)
found_log = []
full_log = []
bar = Bar('Поиск в файлах...', max = len(file_list))
for file in file_list:
    found_log = contains_words(file, words_to_check)
    if len(found_log) > 0:
        full_log.extend(found_log)
    bar.next()
bar.finish()
if len(full_log)  >  0:
    for log in full_log:
        print(log)
else:
    print("Ничего не найдено.")