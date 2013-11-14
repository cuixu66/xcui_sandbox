#!/usr/bin/python -B

import sys

def get_moving_avg(array, window):
    rtn = []
    if(window % 2 != 1):
        print "Please use an odd number as window"
        sys.exit(66)
        return rtn
    for i in range(0,len(array)):
        tmp_window = float(window)
        sum = 0.0
        for k in range(i-window/2, i+window/2 + 1):
            if(k < 0) or (k >= len(array)):
                tmp_window -= 1.0
            else:
                sum += float(array[k]);
        rtn.append(sum / float(tmp_window))
    return rtn

## Ranges Must be in ascend order
def normalize_ranges(range_one, range_two, range_three, range_four):
    rtn = []
    base_range = range_two - range_one
    for i in range(range_one, range_two):
        rtn.append(i)
    for i in range(range_two, range_three):
        rtn.append((i - range_two) * base_range / float(range_three - range_two) + base_range + range_one)
    for i in range(range_three, range_four):
        rtn.append((i - range_three) * base_range / float(range_four-range_three)+ base_range * 2 + range_one)
    return rtn


def cal_avg_array_of_arrays(array_of_arrays):
    rtn = []
    for j in range(len(array_of_arrays[0])):
        sum = 0.0
        for i in range(len(array_of_arrays)):
            sum += array_of_arrays[i][j]
        rtn.append(sum/len(array_of_arrays))
    return rtn
