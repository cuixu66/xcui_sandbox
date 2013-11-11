#!/usr/bin/python -B
import sys
import re
import sliding_avg_calculator as cal

def cal_overall_miss_rate(test_type, client_num):
    sum = 0.0
    for i in range(4, 11):
        tmp_overall_cache = get_overall_some_rate("../data/" + test_type
                                                  + ("" if test_type == "sh/no_ac" else "/test")
                                                  + "/client" + str(client_num)
                                                  + "_size100k_run"
                                                  + str(i) + "_acPerc-1_off-1",
                                                  3,
                                                  9)

        sum += tmp_overall_cache
    return sum/7.0;

def cal_overall_cache_aggregated(test_type, client_num):
    sum = 0.0
    for i in range(4, 11):
        tmp_overall_cache = get_overall_cache_hit_rate("../data/" + test_type
                                                       + ("" if test_type == "sh/no_ac" else "/test")
                                                       + "/client" + str(client_num)
                                                       + "_size100k_run"
                                                       + str(i) + "_acPerc-1_off-1")

        sum += tmp_overall_cache
    return sum/7.0;

def get_overall_some_rate(file_name, index_one, index_two):
    array_one = cal.read_value_into_array(file_name, index_one)
    array_two = cal.read_value_into_array(file_name, index_two)
    return cal.cal_overall_cache_hit_rate(array_one, array_two)

# given a file name, calculate the overall cache hit rate
def get_overall_cache_hit_rate(file_name):
    array_6 = cal.read_value_into_array(file_name, 6)
    array_9 = cal.read_value_into_array(file_name, 9)
    return cal.cal_overall_cache_hit_rate(array_6, array_9)

def cal_one_sliding_avg(file_name, index):
    cache_hit=cal.read_value_into_array(file_name, index)
    sliding_avg_1=cal.cal_sliding_avg(cache_hit,3)
    sliding_avg_2=cal.cal_sliding_avg(cache_hit,7)
    sliding_avg_3=cal.cal_sliding_avg(cache_hit,31)
    # sliding_avg=cal.cal_sliding_avg(cache_hit,31)
    sliding_avg = sliding_avg_1[0:21] + sliding_avg_2[21:91] + sliding_avg_3[91:990]
    return sliding_avg

def cal_miss_sliding_avg(test_type, client_num):
    matrix = []
    CACHE_INDEX = 3
    for i in range(4,11):
        tmp_sliding_avg = cal_one_sliding_avg("../data/" + test_type
                                              + ("" if test_type == "sh/no_ac" else "/test")
                                              + "/client" + str(client_num)
                                              + "_size100k_run"
                                              + str(i) + "_acPerc-1_off-1", CACHE_INDEX)
        matrix.append(tmp_sliding_avg)
    return cal.cal_avg(matrix)

def cal_cache_avg_sliding_avg(test_type, client_num):
    rtn = []
    matrix = []
    for i in range(4,11):
        tmp_sliding_avg = cal_one_sliding_avg("../data/" + test_type
                                              + ("" if test_type == "sh/no_ac" else "/test")
                                              + "/client" + str(client_num)
                                              + "_size100k_run"
                                              + str(i) + "_acPerc-1_off-1", 6)

        matrix.append(tmp_sliding_avg)
    for i in range(0,990):
        sum = 0.0
        for j in range(0,7):
            sum += float(matrix[j][i])
        rtn.append(sum/7.0)
    verifier = cal.cal_avg(matrix)
    if(verifier == rtn):
        xcui = "i win or do nothing"
    else:
        print rtn[:2]
        print verifier[:2]
        print "kill me"
    return rtn
