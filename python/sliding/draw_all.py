#!/usr/bin/python -B

for i  in range(12,72,12):
    ./cache_hit.py i
    ./cache_hit.py i true
    ./miss_rate i
    ./miss_rate i true
    ./reject_vs_miss.py i
