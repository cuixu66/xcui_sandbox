#!/usr/bin/python -B

import os

for i  in range(12,72,12):
    os.system("./cache_hit.py " + str(i))
    # os.system("./cache_hit.py " + str(i))
    os.system("./cache_hit.py " + str(i) + " true")
    os.system("./miss_rate.py " + str(i))
    os.system("./miss_rate.py " + str(i) + " true")
    os.system("./reject_vs_miss.py " + str(i))
