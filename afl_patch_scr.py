# Run in AFLplusplus/src directory before `make`
# After fuzzing stop there will be `fuzzer_screen` file in output directory with screenshot
import fileinput
import os

filename = "afl-fuzz.c"
insertion_lines = "  u8 scrfile[PATH_MAX]; snprintf(scrfile,PATH_MAX,\"%s/fuzzer_screen\",afl->out_dir);  FILE* sfn = freopen(scrfile,\"w\",stdout); show_stats(afl); fclose(sfn);"
temp_filename = f"{filename}.tmp"
with open(filename, "r") as file, open(temp_filename, "w") as temp_file:
    for line in file:
        temp_file.write(line)
        if "show_stats(afl);" in line:
            temp_file.write(insertion_lines)
os.replace(temp_filename, filename)
