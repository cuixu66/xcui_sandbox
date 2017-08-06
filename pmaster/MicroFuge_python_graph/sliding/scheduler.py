#!/usr/bin/python -B
import re
import sys
import sliding_avg_calculator as cal
import matplotlib.pyplot as plt
import helper as h
import scheduler_helper as ssh


## DELETE LATER
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

## END OF DELETION LATER



inputs = sys.argv
if(len(inputs) != 3):
    print 'Usage: ' + inputs[0] + " client_num" + " acPerc"
    sys.exit(1)

CLIENT_NUM = int(inputs[1])
AC_PERC = int(inputs[2])

x_axis = []
for i in range(10,1000):
    x_axis.append(i)

# sliding_avg_mm=h.cal_one_sliding_avg("../data/mm/test/client12_size100k_run6_acPerc-1_off-1",6)
# sliding_avg_cs=h.cal_one_sliding_avg("../data/cs/test/client12_size100k_run6_acPerc-1_off-1",6)
sliding_avg_mm=h.cal_miss_sliding_avg("mm", CLIENT_NUM)
sliding_avg_cs=h.cal_miss_sliding_avg("cs", CLIENT_NUM)
sliding_avg_sch=h.cal_miss_sliding_avg("sh/no_ac", CLIENT_NUM)
sliding_avg_ac_miss=ssh.cal_miss_sliding_avg(CLIENT_NUM, AC_PERC)
sliding_avg_ac_miss = [x * 100 for x in sliding_avg_ac_miss]
sliding_avg_ac_reject=ssh.cal_reject_sliding_avg(CLIENT_NUM, AC_PERC)
sliding_avg_ac_reject=[x * 100 for x in sliding_avg_ac_reject]
sliding_avg_ac_miss_reject=map(lambda x: x[0] + x[1], zip(sliding_avg_ac_miss, sliding_avg_ac_reject))
# sys.exit(66)

normalized_x_axis=cal.normalize_ranges(10,30,100,1000)

# overall cache hit rate
overall_mm=h.cal_overall_miss_rate("mm",CLIENT_NUM)
overall_cs=h.cal_overall_miss_rate("cs",CLIENT_NUM)
overall_sch=h.cal_overall_miss_rate("sh/no_ac", CLIENT_NUM)
overall_ac_miss=find_overall("DEADLINE-MISSED\]",AC_PERC, CLIENT_NUM)
overall_ac_reject=find_overall("REJECT", AC_PERC, CLIENT_NUM)
overall_ac_miss_reject=overall_ac_miss + overall_ac_reject

# all about graphs now
plt.figure(None, figsize=(16, 12), dpi=100)


plt.subplot(211)
# normalized_x_axis[:]=[ (x-10.0) / 60.0* 990.0 + 10.0 for x in normalized_x_axis]
# print normalized_x_axis
plt.title("Sliding Deadline Miss Rate over Request Deadlines with Scaled x-axis and "
          + str(CLIENT_NUM * 4) + " Clients")
plt.plot(normalized_x_axis, sliding_avg_cs, 'r-.', label='DLC')
plt.plot(normalized_x_axis, sliding_avg_sch, 'b--', label='DLS')
plt.plot(normalized_x_axis, sliding_avg_ac_miss, 'k:', label="DLS with admission control")
plt.plot(normalized_x_axis, sliding_avg_ac_miss_reject, 'c-', label='Rejected plus Deadline Missed')

plt.axis([10,70,0,50])
plt.xlabel("Request Deadline in (ms), scaled such that 10-30,30-100,100-1000 ranges have the same length")
plt.ylabel("Deadline Missed Rate 100%")


plt.axhline(y=overall_cs, linestyle='-.', color='r', label='Overvall Deadline Missed DLC')
plt.axhline(y=overall_sch, linestyle='--', color='b', label='Overvall Deadline Missed DLS')
plt.axhline(y=overall_ac_miss, linestyle=':', color='k', label='Overvall Deadline Missed with DLS AC')
plt.axhline(y=overall_ac_miss_reject, linestyle='-', color='c', label='Overvall Deadline Missed + Rejection for DLS AC')

print overall_ac_miss

## Three vertical lines to distinguish buckets
plt.axvline(x=30,linestyle='-', color='k')
plt.axvline(x=50,linestyle='-', color='k')
plt.axvline(x=70,linestyle='-', color='k')

# # plt.legend()
plt.legend(loc='upper right', prop={'size':9})
plt.xticks([10,15,20,25,30,          35, 40, 45,            50, 55, 60, 65, 70],
           ['10','15','20','25','30', '47.5', '65', '83.5', '100', '325', '550', '775' ,'1000'])

plt.show()





# plt.subplot(212)
# plt.title("Sliding Cache Hit Rate over Request Deadlines with "
#           + str(CLIENT_NUM * 4) + " Clients")
# plt.plot(x_axis,sliding_avg_mm, "r--", label='Memcached')
# plt.plot(x_axis,sliding_avg_cs, "b-", label='DLC')
# if(scheduler):
#     plt.plot(x_axis,sliding_avg_no_ac, "k:", label='DLS')
# # TIPS must have plt.legend() so the "label='DLC'" can show up in the graph
# plt.legend()
# plt.axis([10,1000,0,100])
# plt.xlabel("Request Deadline in (ms)")
# plt.ylabel("Cache Hit Rate in 100%")
# plt.show()

# #print len(sliding_avg_mm)
# #print normalized_x_axis
