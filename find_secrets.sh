#!/bin/bash
grep -R --color=always -ir -E "(password|private_key|login|user|username|secret|cipher|passwd|hash|md5|sha1)" > grep_pass.result
grep -R --color=always -ir -E "(hardcode|hack|malware|backdoor|trojan|exploit|RAT|brute)" > grep_hack.result