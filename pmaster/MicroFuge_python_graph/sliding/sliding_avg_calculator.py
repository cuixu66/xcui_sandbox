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
    return rtn

# Verified by hand@@
def cal_sliding_avg(array, window):
    rtn = []
    if(window % 2 != 1):
        print "please use an odd number as window"
        sys.exit(66)
        return rtn
    for i in range(10,1000):
        tmp_window = float(window)
        sum = 0.0
        for k in range(i-window/2, i+window/2 + 1):
            if(k < 10) or (k > 999):
                tmp_window -= 1.0
                # sum += float(array[i]);
            else:
                sum += float(array[k]);
        rtn.append(sum / float(tmp_window))
    return rtn

# Verified by experimental result output
def cal_overall_cache_hit_rate(array_6, array_9):
    total_num_read = 0.0
    total_cache_hit = 0.0
    for i in range(10, 1000):
        total_num_read += float(array_9[i]);
        if(float(array_9[i]) == 0.0):
            print "PANIC PLEASE"
            sys.exit(66)
        total_cache_hit += float(array_6[i]) * float(array_9[i]);
    return total_cache_hit / total_num_read

# cache_hit=read_value_into_array("./data/test/client12_size100k_run1_acPerc-1_off-1", 6)
# num_read=read_value_into_array("./data/test/client12_size100k_run1_acPerc-1_off-1", 9)
# sliding_avg=cal_sliding_avg(cache_hit,51)
#print len(sliding_avg)
#print sliding_avg

#print cal_overall_cache_hit_rate(cache_hit, num_read)

## Ranges Must be in ascend order
# Verified by hand@@
def normalize_ranges(range_one, range_two, range_three, range_four):
    rtn = []
    base_range = range_two - range_one
    for i in range(range_one, range_two):
        rtn.append(i)
    for i in range(range_two, range_three):
        rtn.append((i - range_two) * base_range / float(range_three-range_two)+ base_range + range_one)
    for i in range(range_three, range_four):
        rtn.append((i - range_three) * base_range / float(range_four-range_three)+ base_range * 2 + range_one)
    return rtn

# To be verified by hand
# Verified by duplicated helper method in "cal_cache_sliding_avg"
def cal_avg(array_of_arrays):
    rtn = []
    for j in range(len(array_of_arrays[0])):
        sum = 0.0
        for i in range(len(array_of_arrays)):
            sum += array_of_arrays[i][j]
        rtn.append(sum/len(array_of_arrays))
    return rtn
