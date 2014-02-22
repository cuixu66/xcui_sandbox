#!/usr/bin/python -B
import sys
from os.path import expanduser
import calculators.moving_avg_calculator as cal
import matplotlib.pyplot as plt
import microfuge_specific.microfuge_calculator as mf
import plt_helper.save_fig as saver

inputs = sys.argv
if(len(inputs) != 5):
    print 'Usage: ' + inputs[0] + " client_num" + " DN_DATA" + " CS_DATA" + " EC2_HUH"
    sys.exit(1)

CLIENT_NUM = int(inputs[1])
DN_DATA = str(inputs[2])
CS_DATA = str(inputs[3])
EC2_HUH = bool(inputs[4])

if(EC2_HUH):
    SAVE_DIR = 'EC2_CS_DN/'
else:
    SAVE_DIR = 'LOCAL_CS_DN/'


HOME = expanduser("~")
x_axis = []
for i in range(10,1000):
    x_axis.append(i)

# overall cache hit rate
dn_generator = mf.MicrofugeArrayGenerator(mf.MicrofugeResultType.DEADLINE_MISS,
                                          HOME+DN_DATA, CLIENT_NUM, 1, 6, -1, -1, False)
cs_generator = mf.MicrofugeArrayGenerator(mf.MicrofugeResultType.DEADLINE_MISS,
                                          HOME+CS_DATA, CLIENT_NUM, 1, 6, -1, -1, False)
dn_sliding_avg = dn_generator.get_moving_avg()
cs_sliding_avg = cs_generator.get_moving_avg()

dn_overall = dn_generator.get_overall_percentage()
cs_overall = cs_generator.get_overall_percentage()
print "CS_MISS " + str(CLIENT_NUM) + " " + str(cs_overall)
print "DN_MISS " + str(CLIENT_NUM) + " " + str(dn_overall)

normalized_x_axis=cal.normalize_ranges(10,30,100,1000)

# all about graphs now
plt.figure(None, figsize=(10, 5), dpi=100)

plt.title("Sliding Deadline Miss Rate over Request Deadlines with Scaled x-axis for "
          + str(CLIENT_NUM * 4) + " Clients")

plt.plot(normalized_x_axis, cs_sliding_avg, 'r--', label='DLC')
plt.plot(normalized_x_axis, dn_sliding_avg, 'k:', label="DataNode")


plt.axis([10,70,0,80])
plt.xlabel("Request Deadline in (ms), scaled such that ranges 10-30, 30-100 and 100-1000 have the same length")
plt.ylabel("Deadline Miss Rate in 100%")


plt.axvline(x=29.9,linestyle='-', color='k')
plt.axvline(x=30.1,linestyle='-', color='k')
plt.axvline(x=49.9,linestyle='-', color='k')
plt.axvline(x=50.1,linestyle='-', color='k')


plt.axhline(y=cs_overall, linestyle='--', color='r', label="Overall Dealine Miss Rate DLC")
plt.axhline(y=dn_overall, linestyle=':', color='k', label="Overall Deadline Miss Rate DataNode")
# plt.legend()
plt.legend(loc='upper right', prop={'size':11})
plt.xticks([10,15,20,25,30,          35, 40, 45,            50, 55, 60, 65, 70],
           ['10','15','20','25','30', '47.5', '65', '83.5', '100', '325', '550', '775' ,'1000'])

saver.save(plt, SAVE_DIR + "/miss_" + str(CLIENT_NUM))
