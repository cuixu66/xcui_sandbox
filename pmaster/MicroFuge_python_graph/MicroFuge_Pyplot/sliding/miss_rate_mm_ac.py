#!/usr/bin/python -B
import sys
from os.path import expanduser
import calculators.moving_avg_calculator as cal
import matplotlib.pyplot as plt
import microfuge_specific.microfuge_calculator as mf
import plt_helper.save_fig as saver

inputs = sys.argv
if(len(inputs) != 5):
    print 'Usage: ' + inputs[0] + " client_num" + " MM_DATA" + " SH_DATA" + " EC2_HUH"
    sys.exit(1)

CLIENT_NUM = int(inputs[1])
MM_DATA = str(inputs[2])
SH_DATA = str(inputs[3])
EC2_HUH = bool(inputs[4])

if(EC2_HUH):
    SAVE_DIR = 'EC2_AC_MM/'
else:
    SAVE_DIR = 'LOCAL_AC_MM/'


HOME = expanduser("~")
x_axis = []
for i in range(10,1000):
    x_axis.append(i)

# overall cache hit rate
mm_generator = mf.MicrofugeArrayGenerator(mf.MicrofugeResultType.DEADLINE_MISS,
                                          HOME+MM_DATA, CLIENT_NUM, 1, 6, -1, -1, False)
sh_generator = mf.MicrofugeArrayGenerator(mf.MicrofugeResultType.DEADLINE_MISS,
                                          HOME+SH_DATA, CLIENT_NUM, 1, 6, 88, 0, False)
mm_sliding_avg = mm_generator.get_moving_avg()
sh_sliding_avg = sh_generator.get_moving_avg()

mm_overall = mm_generator.get_overall_percentage()
sh_overall = sh_generator.get_overall_percentage()
print "CS_MISS " + str(CLIENT_NUM) + " " + str(sh_overall)
print "MM_MISS " + str(CLIENT_NUM) + " " + str(mm_overall)

normalized_x_axis=cal.normalize_ranges(10,30,100,1000)

# all about graphs now
plt.figure(None, figsize=(8,4), dpi=100)

# plt.title("Sliding Deadline Miss Rate over Request Deadlines with Scaled x-axis for "
          # + str(CLIENT_NUM * 4) + " Clients")

plt.plot(normalized_x_axis, sh_sliding_avg, 'r-', label='DLC + DLS + AC')
plt.plot(normalized_x_axis, mm_sliding_avg, 'k--', label="Memcached")


plt.axis([10,70,0,50])
plt.xlabel("Request Deadline in (ms)")
plt.ylabel("Deadline Miss Rate in %")


plt.axvline(x=29.9,linestyle='-', color='k')
plt.axvline(x=30.1,linestyle='-', color='k')
plt.axvline(x=49.9,linestyle='-', color='k')
plt.axvline(x=50.1,linestyle='-', color='k')


plt.axhline(y=sh_overall, linestyle='-', color='r', label="Overall Dealine Miss Rate DLC + DLS + AC")
plt.axhline(y=mm_overall, linestyle='--', color='k', label="Overall Deadline Miss Rate Memcached")
# plt.legend()
plt.legend(loc='upper right', prop={'size':11})
plt.xticks([10,15,20,25,30,          35, 40, 45,            50, 55, 60, 65, 70],
           ['10','15','20','25','30', '47.5', '65', '83.5', '100', '325', '550', '775' ,'1000'])

saver.save(plt, SAVE_DIR + "/miss_" + str(CLIENT_NUM))
