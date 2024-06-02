#!/usr/bin/python3
# pip install python-magic tqdm

import sys, os
import magic
from tqdm.auto import tqdm

words_to_check = ["protest", "peacenotwar", "node-ipc", "украин", "мобилиз", "агресс", "фсб", "войн", "военн", "зеленск", 
                  "напал", "санкци", "преступ", "путин", "убив", "ukrain", "putin", "russia", "крым", "crimea", "militar", "invasion"]

def get_filelist(directory):
    fl = []
    mime = magic.Magic(mime=True)
    for root, dirs, files in tqdm(os.walk(directory)):
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
print(f"Поиск текстовых файлов в каталоге `{path}`: ")
file_list = get_filelist(path)
found_log = []
full_log = []
full_log.append(f"# Каталог {path}, файлов: {len(file_list)}")
print(f"Поиск совпадений...")
for file in tqdm(file_list):
    found_log = contains_words(file, words_to_check)
    if len(found_log) > 0:
        full_log.extend(found_log)
for log in full_log:
    print(log)
