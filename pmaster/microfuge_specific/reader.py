#!/usr/bin/python -B

import sys

# Read a set of values into an array from a YCSB result file
# Index meanings:
# 3 deadline missed
# 6 cache hit percentage
# 7 total # of read that missed deadline in this deadline bucket
# 8 total # of read rejections in this deadline bucket
# 9 total # of read in this deadline bucket
# Verified by hand@@
def read_value_into_array(file_name, index):
    rtn = []
    data = open(file_name, "r")
    # print data.name
    for line in data:
        if "READ-DEADLINE" in line:
            # sys.stdout.write(line);
            tokens = line.split()
            # tokens[6] is the cache hit percentage
            # sys.stdout.write(tokens[6] + "\n");
            rtn.append(tokens[index])
    data.close()
    return rtn[10:]


# Verified by experimental result output
# calculate overall rate based on array_one and array_two
# where array_one is the percentage array
# and the array_two is the count array
def cal_overall_rate(array_percentage, array_count):
    assert (len(array_percentage) == len(array_count))
    total_event = 0.0
    total_interested_event = 0.0
    for i in range(0, len(array_percentage)):
        total_event += float(array_count[i]);
        assert(array_count[i] != 0.0)
        total_interested_event += float(array_percentage[i]) * float(array_count[i]);
    return total_interested_event / total_event
