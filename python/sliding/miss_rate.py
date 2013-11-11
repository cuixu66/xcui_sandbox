#!/usr/bin/python -B
import sys
import sliding_avg_calculator as cal
import matplotlib.pyplot as plt
import helper as h

inputs = sys.argv
if(len(inputs) != 2 and len(inputs) != 3):
    print 'Usage: ' + inputs[0] + " client_num" + " [anything string to turn on scheduler]"
    sys.exit(1)

scheduler = False
if(len(inputs) == 3):
    scheduler = True
client_num = int(inputs[1])

x_axis = []
for i in range(10,1000):
    x_axis.append(i)

sliding_avg_mm=h.cal_miss_sliding_avg("mm", client_num)
sliding_avg_cs=h.cal_miss_sliding_avg("cs", client_num)
sliding_avg_no_ac=h.cal_miss_sliding_avg("sh/no_ac", client_num)


normalized_x_axis=cal.normalize_ranges(10,30,100,1000)

# overall cache hit rate
overall_mm=h.cal_overall_miss_rate("mm",client_num)
overall_cs=h.cal_overall_miss_rate("cs",client_num)
overall_no_ac=h.cal_overall_miss_rate("sh/no_ac", client_num)

# all about graphs now
plt.figure(None, figsize=(16, 12), dpi=100)


plt.subplot(211)
#normalized_x_axis[:]=[ (x-10.0) / 60.0* 990.0 + 10.0 for x in normalized_x_axis]
#print normalized_x_axis
plt.title("Sliding Deadline Miss Rate over Request Deadlines with Scaled x-axis and "
          + str(client_num * 4) + " Clients")
plt.plot(normalized_x_axis, sliding_avg_mm, 'r-', label='Memcached')
plt.plot(normalized_x_axis, sliding_avg_cs, 'b--', label='DLC')
if(scheduler):
    plt.plot(normalized_x_axis, sliding_avg_no_ac, 'k:', label="DLS")


plt.axis([10,70,0,50])
plt.xlabel("Request Deadline in (ms), scaled such that 10-30,30-100,100-1000 ranges have the same length")
plt.ylabel("Deadline Miss Rate in 100%")
plt.axhline(y=overall_mm, linestyle='-', color='r', label='Overall Deadline Miss Rate Memcahced')
plt.axhline(y=overall_cs, linestyle='--', color='b', label="Overall Dealine Miss Rate DLC")
plt.axvline(x=30,linestyle='-', color='k')
plt.axvline(x=50,linestyle='-', color='k')
plt.axvline(x=70,linestyle='-', color='k')

if(scheduler):
    plt.axhline(y=overall_no_ac, linestyle=':', color='k', label="Overall Deadline Miss Rate DLS")
# plt.legend()
plt.legend(loc='upper right', prop={'size':9})
plt.xticks([10,15,20,25,30,          35, 40, 45,            50, 55, 60, 65, 70],
           ['10','15','20','25','30', '47.5', '65', '83.5', '100', '325', '550', '775' ,'1000'])


plt.subplot(212)
plt.title("Sliding Deadline Miss Rate over Request Deadlines with "
          + str(client_num * 4) + " Clients")
plt.plot(x_axis,sliding_avg_mm, "r--", label='Memcached')
plt.plot(x_axis,sliding_avg_cs, "b-", label='DLC')
if(scheduler):
    plt.plot(x_axis,sliding_avg_no_ac, "k:", label='DLS')
# TIPS must have plt.legend() so the "label='DLC'" can show up in the graph
plt.legend()
plt.axis([10,1000,0,50])
plt.xlabel("Request Deadline in (ms)")
plt.ylabel("Deadline Miss Rate in 100%")
plt.show()

#print len(sliding_avg_mm)
#print normalized_x_axis
