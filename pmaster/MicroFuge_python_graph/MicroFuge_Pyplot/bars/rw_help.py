#!/usr/bin/python -B
# a stacked bar plot with errorbars
import numpy as np
import matplotlib.pyplot as plt
import re
from os.path import expanduser
from calculators import confidence_interval_calculator as CI
from microfuge_specific import reader as reader


# Quick & Dirty & UGLY Implementation for rw support because the deadline is near
# should delete this soon

HOME_DIR = expanduser("~")

PATTERN = [ "/" , "\\" ,"o", "*", "O", "x", ".", "|", "-", "+" ]

CS_RW_DIR = HOME_DIR + "/ICDCS/ICDCS_DATA/EC2" + "/rw/cs_rw/"
CS_RW_CLIENT_NUMBERS = [24,48]
SH_RW_DIR = HOME_DIR + "/ICDCS/ICDCS_DATA/EC2" + "/rw/sh_rw/"
SH_RW_CLIENT_NUMBERS = [24,48]


# rtn is array of size, first element is the total update miss and second is the total update
def read_rw_total(file_name):
    rtn = []
    data = open(file_name, "r")
    update_miss_arr = []
    update_total_arr = []
    for line in data:
        if "NEW-UPDATE-DEADLINE" in line:
            tokens = line.split()
            update_miss_arr.append(float(tokens[len(tokens)-2]))
            update_total_arr.append(float(tokens[len(tokens)-1]))
    data.close()
    rtn.append(sum(update_miss_arr))
    rtn.append(sum(update_total_arr))
    return rtn
def get_one_overall_arr(data_dir, client_num, ac_perc, offset, i):
    total_total_miss = 0.0
    total_total_req = 0.0
    file_name = (data_dir
                 + "client" + str(client_num)
                 + "_size100k_"
                 + "run" + str(i)
                 + "_acPerc" + str(ac_perc)
                 + '_off' + str(offset))
    total_read_array = reader.read_value_into_array(file_name, 9)
    total_read_miss_array = reader.read_value_into_array(file_name, 7)
    total_read = 0.0
    total_read_miss = 0.0
    for i in range(len(total_read_array)):
        total_read += float(total_read_array[i])
        total_read_miss += float(total_read_miss_array[i])
    update_info = read_rw_total(file_name)
    print update_info[0] / update_info[1]
    total_miss = update_info[0] + total_read_miss
    total_req = update_info[1] + total_read
    total_total_miss += total_miss
    total_total_req += total_req
    print total_total_miss
    print total_total_req
    return total_total_miss / total_total_req * 100.

def get_overall_arr(data_dir, client_num, ac_perc, offset):
    rtn = []
    for i in range(1,6):
        value = get_one_overall_arr(data_dir, client_num , ac_perc, offset, i)
        rtn.append(value)
    return rtn

# return values will be filled into rtn_mean, rtn_std
def get_rw_results(data_dir, client_nums, rtn_mean, rtn_std):
    ac_perc = -1
    offset = -1
    overall_arr_client_num1 = get_overall_arr(data_dir, client_nums[0], ac_perc, offset)
    overall_arr_client_num2 = get_overall_arr(data_dir, client_nums[1], ac_perc, offset)
    stdmean_stderr = CI.get_conf_int(overall_arr_client_num1)
    rtn_mean.append(stdmean_stderr[0])
    rtn_std.append(stdmean_stderr[1])
    stdmean_stderr = CI.get_conf_int(overall_arr_client_num2)
    rtn_mean.append(stdmean_stderr[0])
    rtn_std.append(stdmean_stderr[1])

def test():
    arr1 = []
    arr2 = []
    get_rw_results(CS_RW_DIR, CS_RW_CLIENT_NUMBERS ,arr1, arr2)
    print arr1
    print arr2

test()
