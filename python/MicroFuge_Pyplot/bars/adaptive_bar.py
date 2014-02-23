#!/usr/bin/python
import numpy as np
import pylab as pl
import datetime
from plt_helper import save_fig as saver

data = \
"""13.129 6.1802 4.6131 0.98494 0.42334 0.37844 0.35962 0.31823 0.28426 0.31819 0.27862 0.36834 0.32135 0.2734 0.2966 0.24706 0.20248 0.23699 0.31055 0.24534 0.20604 0.24285 0.18047 0.26548 0.21979 0.21659 0.19748 0.1956 0.143 0.16438 0.1593 0.039004"""

values = []
dates = []

i = 0
for multiplier in data.split(" "):
    i += 1
    values.append(float(multiplier))
    dates.append(r'$\mathrm{m}_{' + str(i) + '}$' )

pl.clf()
pl.figure(None, figsize=(8,6), dpi = 100)


ax = pl.subplot(111)
# ax.bar(dates, values, width=100)
# ax.xaxis_date()

width=0.6
ax.bar(range(len(dates)), values, width=width)
ax.set_ylabel('Values of Multipliers')
ax.set_xlabel('Adaptive Multipliers')
ax.set_xticks(np.arange(len(dates)) + width/2)
ax.set_xticklabels(dates, rotation=60)
pl.xlim(xmax=32)

# pl.show()

saver.save(pl, 'EC2_BAR/adaptive_multipliers')
