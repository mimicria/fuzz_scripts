#!/usr/bin/python3

import os

path = '/home/user/php-src/tests'
out_path = '/home/user/php-in'
for root, dirs, files in os.walk(path):
    for file in files:
        if(file.endswith(".phpt")):
            newfile=file.split('.')[0]+".php"
            phpt_file = os.path.join(root,file)
            php_file = os.path.join(root,newfile)
            content = []
            with open(phpt_file, "r", errors='ignore') as file:
                print(phpt_file, " -> ", php_file) 
                content.clear()
                record = False
                for line in file:
                    if line=='--FILE--\n':
                        record = True
                        continue
                    if record==True:
                        res = line.find('--')
                        if res==-1:
                            content.append(line)
                        elif res==0:
                            record = False
                            break
                        else:
                            content.append(line)
            with open(php_file, "w") as file:
                file.writelines(content)


