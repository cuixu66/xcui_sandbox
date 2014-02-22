#!/usr/bin/python -B
import sys
from os.path import expanduser
import matplotlib.pyplot as plt
import plt_helper.save_fig as saver
import calculators.moving_avg_calculator as cal
import microfuge_specific.microfuge_calculator as mf

inputs = sys.argv
if(len(inputs) != 5):
    print 'Usage: ' + inputs[0] + " client_num" + " CS_DATA" + " SH_DATA" + " EC2_HUH"
    sys.exit(1)

CLIENT_NUM = int(inputs[1])
CS_DATA = str(inputs[2])
SH_DATA = str(inputs[3])
EC2_HUH = bool(inputs[4])
if(EC2_HUH):
    SAVE_DIR = 'EC2_SH_CS/'
else:
    SAVE_DIR = 'LOCAL_SH_CS/'

HOME = expanduser("~")

x_axis = []
for i in range(10,1000):
    x_axis.append(i)

cs_generator = mf.MicrofugeArrayGenerator(mf.MicrofugeResultType.CACHE_HIT,
                                          HOME + CS_DATA, CLIENT_NUM, 1, 6, -1, -1, False)
sh_generator = mf.MicrofugeArrayGenerator(mf.MicrofugeResultType.CACHE_HIT,
                                          HOME + SH_DATA, CLIENT_NUM, 1, 6, -1, -1, False)
cs_sliding_avg = cs_generator.get_moving_avg()
sh_sliding_avg = sh_generator.get_moving_avg()

cs_overall=cs_generator.get_overall_percentage()
sh_overall=sh_generator.get_overall_percentage()

normalized_x_axis=cal.normalize_ranges(10,30,100,1000)

# all about graphs now
plt.figure(None, figsize=(10, 5), dpi=100)


plt.title("Sliding Cache Hit Rate over Request Deadlines with Scaled x-axis for "
          + str(CLIENT_NUM * 4) + " Clients")
plt.plot(normalized_x_axis, sh_sliding_avg, 'r--', label='DLC + DLS')
plt.plot(normalized_x_axis, cs_sliding_avg, 'k:', label="DLC")

plt.axis([10,70,0,100])
plt.xlabel("Request Deadline in (ms), scaled such that ranges 10-30,30-100 and 100-1000 have the same length")
plt.ylabel("Cache Hit Rate in 100%")

## Three vertical lines to distinguish buckets
plt.axvline(x=29.9,linestyle='-', color='k')
plt.axvline(x=30.1,linestyle='-', color='k')
plt.axvline(x=49.9,linestyle='-', color='k')
plt.axvline(x=50.1,linestyle='-', color='k')

plt.axhline(y=sh_overall, linestyle='--', color='r', label="Overall Cache Hit Rate DLC + DLS")
plt.axhline(y=cs_overall, linestyle=':', color='k', label="Overall Cache Hit Rate DLC")
plt.legend(loc='lower left', prop={'size':11})
plt.xticks([10,15,20,25,30,          35, 40, 45,            50, 55, 60, 65, 70],
           ['10','15','20','25','30', '47.5', '65', '83.5', '100', '325', '550', '775' ,'1000'])


saver.save(plt, SAVE_DIR + "/cache_" + str(CLIENT_NUM))
