#!/usr/bin/python -B

import sys
import matplotlib
import matplotlib.pyplot as plt
import re
from os.path import expanduser
from plt_helper import save_fig as saver
from matplotlib import rc


############## BOLD ##################
matplotlib.rc('text', usetex=True)
matplotlib.rcParams['text.latex.preamble'] = [r'\boldmath']
############## End of BOLD ##################

CLIENT_NUM= 48

KNOB_START = 50
KNOB_STOP = 100
KNOB_STEP = 1

HOME_DIR = expanduser("~")

overall_rejection = []
overall_miss = []
overall_sum = []
x_axis = []



def get_overall_arr(key_word, knob, client_num):
    rtn = []
    for i in range(1,2):
        data = open(HOME_DIR + "/ICDCS/ICDCS_DATA/EC2/sh/varying_acPerc_192_clients/"
                    + "client" + str(client_num)
                    + "_size100k_"
                    + "run" + str(i)
                    + "_acPerc" + str(knob)
                    + '_off0',
                    "r")
        for line in data:
            if(re.search(key_word, line)):
                tokens = line.split(" ")
                rtn.append(float(tokens[len(tokens) - 1]))
    return rtn


def find_overall(key_word, knob, client_num):
    overall_arr = get_overall_arr(key_word, knob, client_num)
    sum = 0.0
    for i in range(len(overall_arr)):
        sum += overall_arr[i]
    return sum / len(overall_arr)


for i in range(KNOB_START, KNOB_STOP, KNOB_STEP):
    overall_rejection.append(find_overall("REJECTED-",  str(i), CLIENT_NUM))
    overall_miss.append(find_overall("DEADLINE-MISSED\]", str(i), CLIENT_NUM))
    overall_sum.append(overall_rejection[len(overall_sum)] + overall_miss[len(overall_sum)])
    x_axis.append(i)

# The next line of code make sure that the xlabel is not cut off from the plot
plt.subplots_adjust(bottom=0.15)
# all about graph now
plt.figure(None, figsize=(8,4), dpi=300)
plt.plot(x_axis, overall_rejection, 'r-', label='Overall Rejection')
plt.plot(x_axis, overall_miss, 'b--', label='Overall Deadline Miss')
plt.plot(x_axis, overall_sum, "k*", label="Overall Sum of Rejection and Deadline Miss")


plt.xticks([50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 99],
           ['50', '55', '60', '65', '70', '75', '80', '85', '90', '95', '99'])

plt.ylim(ymin=0)
# Notice how I made beta into BOLD font
# Consult the source here:
# http://stackoverflow.com/questions/14324477/bold-font-weight-for-latex-axes-label-in-matplotlib
# Basically, I added lines enclosed by #### BOLD #### at top of this
# so my plt uses latex bold character and the expression $\boldssymbol{\beta}$
# is used to have the bold beta
plt.xlabel("System Parameter " + r'$\boldsymbol{\beta}$')
plt.ylabel("Deadline Miss and Rejection Rates in %")
# plt.twinx()
# plt.ylabel("Rejection Rate in %")
plt.axis([50,99,0,25])
plt.legend(loc='upper left')
# plt.show()

saver.save(plt, 'Varying_ac/varying_acPerc_192')
