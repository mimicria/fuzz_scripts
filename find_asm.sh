#!/bin/bash
grep --include=*.h --include=*.c --include=*.cpp --include=*.hpp -R --color=always -ir -E "_*asm_*\s*\{"