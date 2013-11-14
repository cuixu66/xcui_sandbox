#!/usr/bin/python -B
import sys
import re
import calculators.moving_avg_calculator as cal
import microfuge_specific.reader as reader
import microfuge_specific.microfuge_calculator as mf

def cal_overall_miss_rate(test_type, client_num):
    result_type = mf.MicrofugeResultType.DEADLINE_MISS
    if(test_type == "mm" or test_type == "cs"):
        base_dir = "../data/" + test_type + "/test/"
    else:
        base_dir = "../data/sh/no_ac//"
    ac_perc = -1
    offset = -1
    zero_fill = False
    generator = mf.MicrofugeArrayGenerator(2, base_dir, client_num, 4, 11, ac_perc,offset, zero_fill)
    # print generator.get_overall_percentage(result_type)
    return generator.get_overall_percentage()

def cal_overall_cache_aggregated(test_type, client_num):
    result_type = mf.MicrofugeResultType.CACHE_HIT
    if(test_type == "mm" or test_type == "cs"):
        base_dir = "../data/" + test_type + "/test/"
    else:
        base_dir = "../data/sh/no_ac//"
    ac_perc = -1
    offset = -1
    zero_fill = False
    generator = mf.MicrofugeArrayGenerator(1, base_dir, client_num, 4, 11, ac_perc,offset, zero_fill)
    # print generator.get_overall_percentage(result_type)
    return generator.get_overall_percentage()

def cal_one_sliding_avg(file_name, index):
    generator = mf.MicrofugeArrayGenerator(1, "abc", 12, 4, 11, -1, -1, True)
    return generator.get_single_moving_avg(file_name, index)

def cal_miss_sliding_avg(test_type, client_num):
    return some_wrapper(test_type,client_num, 2)
def cal_cache_avg_sliding_avg(test_type, client_num):
    return some_wrapper(test_type, client_num, 1)

def some_wrapper(test_type, client_num, value):
    result_type = value
    if(test_type == "mm" or test_type == "cs"):
        base_dir = "../data/" + test_type + "/test/"
    else:
        base_dir = "../data/sh/no_ac//"
    ac_perc = -1
    offset = -1
    zero_fill = False
    generator = mf.MicrofugeArrayGenerator(result_type, base_dir, client_num, 4, 11, ac_perc,offset, zero_fill)
    return generator.get_moving_avg()
