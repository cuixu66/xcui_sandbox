#!/usr/bin/python -B
import sys
import re
import sliding_avg_calculator as cal

def cal_one_sliding_avg(array):
    sliding_avg_1=cal.cal_sliding_avg(range(10) + array,3)
    sliding_avg_2=cal.cal_sliding_avg(range(10) + array,7)
    sliding_avg_3=cal.cal_sliding_avg(range(10) + array,31)
    sliding_avg = sliding_avg_1[0:21] + sliding_avg_2[21:91] + sliding_avg_3[91:990]
    return sliding_avg

def cal_miss_sliding_avg(client_num, ac_perc):
    tmp = cal_avg_percentage_array(client_num, ac_perc, 7)
    return cal_one_sliding_avg(tmp)
def cal_reject_sliding_avg(client_num, ac_perc):
    tmp = cal_avg_percentage_array(client_num, ac_perc, 8)
    return cal_one_sliding_avg(tmp)

## index can be 7 or 8, where 7 is deadline miss column and 8 is the reject column
## This function calculates the avg pecentage
def cal_avg_percentage_array(client_num, ac_perc, index):
    matrix = []
    for i in range(4,11):
        file_name = ("../data/" + "sh/"
                     + "ac_" + str(ac_perc) + "_0"
                     + "/client" + str(client_num)
                     + "_size100k_run" + str(i)
                     + "_acPerc" + str(ac_perc)
                     + "_off0")
        target_arr = cal.read_value_into_array(file_name, index)
        base_arr = cal.read_value_into_array(file_name, 9)
        tmp_avg = map(lambda x: float(x[0]) / float(x[1]), zip(target_arr[10:], base_arr[10:]))
        matrix.append(tmp_avg)
    return cal.cal_avg(matrix)

# this is verified by execting these into commandline at data/sh/ac/acPerc50_0/
# YAY Hardest scripts I've ever written
# grep "\[24\]\|\[25\]\|\[26\]" `ls -lt | grep client12 | awk '{print $9}'` | sort | grep -v "run3\|run2\|run1_" > XCUIXCUI
# grep "\[24\|\[25\|\[26" XCUIXCUI | awk '{ sum += $4} END {print sum / 7 / 3}'
# and either python or awk has some rounding errors
# print cal_miss_sliding_avg(12,50)[5]
