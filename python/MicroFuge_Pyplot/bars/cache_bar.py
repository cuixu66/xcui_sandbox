#!/usr/bin/env python
# a stacked bar plot with errorbars
import numpy as np
import matplotlib.pyplot as plt
import re
from os.path import expanduser
from calculators import confidence_interval_calculator as CI
import rw_help as rw_helper
from plt_helper import save_fig as saver

HOME_DIR = expanduser("~")

PATTERN = [ "/" , "\\" ,"o", "*", "O", "x", ".", '-', "|" , "+" ]

MM_DIR = HOME_DIR + "/ICDCS/ICDCS_DATA/EC2" + "/EC2_mm_v1/test/"
MM_CLIENT_NUMBERS = [24,48] # [24,48,96,192]

CS_DIR = HOME_DIR + "/ICDCS/ICDCS_DATA/EC2" + "/cs/test/"
CS_CLIENT_NUMBERS = [24,48] # [24,48,96,192]
SH_DIR = HOME_DIR + "/ICDCS/ICDCS_DATA/EC2" + "/sh/no_ac/"
SH_CLIENT_NUMBERS = [24,48] # [24,48,96,192]
AC_DIR = HOME_DIR + "/ICDCS/ICDCS_DATA/EC2" + "/sh/ac/"
AC_CLIENT_NUMBERS = [24,48] # [24,48,96,192]
DN_DIR = HOME_DIR + "/ICDCS/ICDCS_DATA/EC2" + "/dn/test/"
DN_CLIENT_NUMBERS = [24,48] # [24,48,96,192]
CS_RW_DIR = HOME_DIR + "/ICDCS/ICDCS_DATA/EC2" + "/rw/cs_rw/"
CS_RW_CLIENT_NUMBERS = [24,48]
SH_RW_DIR = HOME_DIR + "/ICDCS/ICDCS_DATA/EC2" + "/rw/sh_rw/"
SH_RW_CLIENT_NUMBERS = [24,48]


def get_overall_arr(key_word, data_dir, client_num, ac_perc, offset):
    rtn = []
    for i in range(1,6):
        data = open(data_dir
                    + "client" + str(client_num)
                    + "_size100k_"
                    + "run" + str(i)
                    + "_acPerc" + str(ac_perc)
                    + '_off' + str(offset),
                    "r")
        for line in data:
            if(re.search(key_word, line)):
                tokens = line.split(" ")
                rtn.append(float(tokens[len(tokens) - 1]))
    return rtn


# return values will be filled into rtn_mean, rtn_std
def get_results(data_dir, client_nums, rtn_mean, rtn_std, ac_huh = False, rejection_huh = False, rw_huh = False):
    if(rejection_huh):
        keyword = "CACHE-HITS-PERCENTAGE"
        ac_perc = 88
        offset = 0
    elif(ac_huh):
        keyword = "CACHE-HITS-PERCENTAGE"
        ac_perc = 88
        offset = 0
    else:
        keyword = "CACHE-HITS-PERCENTAGE"
        ac_perc = -1
        offset = -1
    for i in range(len(client_nums)):
        overall_arr = get_overall_arr(keyword, data_dir, client_nums[i], ac_perc, offset)
        stdmean_stderr = CI.get_conf_int(overall_arr)
        rtn_mean.append(stdmean_stderr[0])
        rtn_std.append(stdmean_stderr[1])


# N = 4
N = 2
ind = np.arange(N)    # the x locations for the groups
width = 0.13      # the width of the bars: can also be len(x) sequence

### plotting now
# this clears the current figure

plt.clf()


plt.figure(None, figsize=(8,4))

mean_values = []
stderr_values = []
get_results(DN_DIR, DN_CLIENT_NUMBERS, mean_values, stderr_values)
print mean_values
p0 = plt.bar(ind + width * 0,  mean_values,width, color='w',
             yerr=stderr_values, ecolor='r',
             edgecolor='black', hatch=PATTERN[0])


mean_values = []
stderr_values = []
get_results(MM_DIR, MM_CLIENT_NUMBERS, mean_values, stderr_values)
p1 = plt.bar(ind + width * 1, mean_values, width, color='w',
             yerr=stderr_values, ecolor='r',
             edgecolor='black', hatch=PATTERN[1])

mean_values = []
stderr_values = []
get_results(CS_DIR, CS_CLIENT_NUMBERS, mean_values, stderr_values)
p2 = plt.bar(ind + width * 2, mean_values,width, color='w', yerr=stderr_values,
             ecolor='r',
             edgecolor='black', hatch=PATTERN[2])


mean_values = []
stderr_values = []
get_results(SH_DIR, SH_CLIENT_NUMBERS, mean_values, stderr_values)
p3 = plt.bar(ind + width * 3,  mean_values,width, color='w',
             yerr=stderr_values, ecolor='r',
             edgecolor='black', hatch=PATTERN[3])

mean_values = []
stderr_values = []
get_results(AC_DIR, AC_CLIENT_NUMBERS, mean_values, stderr_values, True)
p4 = plt.bar(ind + width * 4,  mean_values,width, color='w',
             yerr=stderr_values, ecolor='r',
             edgecolor='black', hatch=PATTERN[4])


mean_values = []
stderr_values = []
get_results(CS_RW_DIR, CS_RW_CLIENT_NUMBERS, mean_values, stderr_values)
p6 = plt.bar(ind[:2] + width * 5.3,  mean_values, width, color='w',
             yerr=stderr_values, ecolor='r',
             edgecolor='black', hatch=PATTERN[6])


mean_values = []
stderr_values = []
get_results(SH_RW_DIR, SH_RW_CLIENT_NUMBERS, mean_values, stderr_values)
p7 = plt.bar(ind[:2] + width * 6.3,  mean_values, width, color='w',
             yerr=stderr_values, ecolor='r',
             edgecolor='black', hatch=PATTERN[5])




plt.axis([0.0, 4, 0, 10])
plt.ylabel('Cache Hit Rate in %')
plt.xlabel('Number of Concurrent Clients')
plt.xticks(ind+width * 3.5, ('96', '192', '384', '768') )
plt.yticks(np.arange(0,101,10))
plt.legend((p1[0], p2[0], p3[0], p4[0], p6[0], p7[0]),
           ('Memcached',
            'DLC', 'DLC + DLS', "DLC + DLS + AC",
            'DLC with 10% Write', 'DLC + DLS with 10% Write'),
           loc = 'upper right', prop={'size':12})

# plt.show()
saver.save(plt, 'EC2_BAR/cache_bar')
