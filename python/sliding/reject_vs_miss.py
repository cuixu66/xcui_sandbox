#!/usr/bin/python -B

import sys
import matplotlib.pyplot as plt
import re
import plt_helper.save_fig as saver
import xcui_global as xg

inputs = sys.argv
if(len(inputs) != 2):
    print "Usage: " + inputs[0] + " client_num"
    sys.exit(66)

CLIENT_NUM= int(inputs[1])

KNOB_START = 50
KNOB_STOP = 91
KNOB_STEP = 10

overall_rejection = []
overall_miss = []
overall_sum = []
x_axis = []



def get_overall_arr(key_word, knob, client_num):
    rtn = []
    for i in range(4,11):
        data = open("../data/sh/ac_" + str(knob) + "_0/"
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
    overall_rejection.append(find_overall("REJECT",  str(i), CLIENT_NUM))
    overall_miss.append(find_overall("DEADLINE-MISSED\]", str(i), CLIENT_NUM))
    overall_sum.append(overall_rejection[len(overall_sum)] + overall_miss[len(overall_sum)])
    x_axis.append(i)


# all about graph now
plt.figure(None, figsize=(10,10), dpi=100)
plt.title("Overall Deadline Miss and Overall Rejection Rate over Percentile used to predict Request Latency with "
          + str(CLIENT_NUM * 4) + " Clients")
plt.plot(x_axis, overall_rejection, 'r-', label='Overall Rejection')
plt.plot(x_axis, overall_miss, 'b--', label='Overall Deadline Miss')
plt.plot(x_axis, overall_sum, "k:", label="Overall Sum of Rejection and Deadline Miss")
# plt.axis([50,90,0,16])
plt.ylim(ymin=0)
plt.xlabel("Percentile Number used to Predict Request Lantency which is used to do admission control")
plt.ylabel("Percentage in %")
plt.legend(loc='upper left')
# plt.show()

saver.save(plt, xg.FIGURE_DIRECTORY
           + "miss_vs_reject_client"
           + str(CLIENT_NUM)
           ,ext='png', close=True, verbose=True)
