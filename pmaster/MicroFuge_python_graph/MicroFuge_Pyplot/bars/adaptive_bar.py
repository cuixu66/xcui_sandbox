#!/usr/bin/python
import numpy as np
import matplotlib
import matplotlib.pyplot as pl
import datetime
from plt_helper import save_fig as saver


# Full set of data, 32 points
# data = \
# """13.129 6.1802 4.6131 0.98494 0.42334 0.37844 0.35962 0.31823 0.28426 0.31819 0.27862 0.36834 0.32135 0.2734 0.2966 0.24706 0.20248 0.23699 0.31055 0.24534 0.20604 0.24285 0.18047 0.26548 0.21979 0.21659 0.19748 0.1956 0.143 0.16438 0.1593 0.039004"""

# first 10 & last 3
data = \
"""13.129 6.1802 4.6131 0.98494 0.42334 0.37844 0.35962 0.31823 0.28426 0.31819 0.0 0 0 0.16438 0.1593 0.039004"""


values = []
dates = []

i = 0
# for multiplier in data.split(" "):
#     i += 1
#     values.append(float(multiplier))
#     dates.append(r'$\mathrm{m}_{' + str(i) + '}$' )

for multiplier in data.split(" "):
    i += 1
    values.append(float(multiplier))
#     dates.append(r'$\mathrm{m}_{' + str(i) + '}$' )

for i in range(1,11):
    dates.append(i)
dates.append(0)
dates.append(0)
dates.append(0)
dates.append(30)
dates.append(31)
dates.append(32)

pl.clf()
pl.figure(None, figsize=(8, 4), dpi = 300)
# The next line solves the problem that the x-axis label is not showing
# source:
# http://stackoverflow.com/questions/6774086/why-is-my-xlabel-cut-off-in-my-matplotlib-plot
# TODO learn why gfc() should be replaced by pl for me
pl.subplots_adjust(bottom=0.15)
# ax = pl.subplot(111)

# ax.bar(dates, values, width=100)
# ax.xaxis_date()


width= .8
pl.bar(range(len(dates)), values, width = width)
pl.ylabel('Values of Multipliers')
pl.xlabel('Queue Numbers of the Adaptive Multiplier Values')
x_tick_locations = []
x_tick_labels = []
for i in range(0, 16):
    if(i < 10):
        x_tick_labels.append( str(i + 1))
    x_tick_locations.append( float(i) + width / 2 )

x_tick_labels.append("")
x_tick_labels.append("Omitted")
x_tick_labels.append("")
x_tick_labels.append('30')
x_tick_labels.append('31')
x_tick_labels.append('32')

pl.xticks(x_tick_locations, x_tick_labels)
pl.xlim(xmax=16)

# pl.show()
saver.save(pl, 'EC2_BAR/adaptive_multipliers')
