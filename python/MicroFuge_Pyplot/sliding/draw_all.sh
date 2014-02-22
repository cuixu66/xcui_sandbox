#!/bin/bash

echo "" > EC2_CHARTS/CACHE_HIT_MM_CS
echo "" > EC2_CHARTS/MISS_RATE_MM_CS
for i in 24 48 96 192
do
    ./cache_hit_mm_cs.py $i '/ICDCS/ICDCS_DATA/EC2/EC2_mm_v1/test/' "/ICDCS/ICDCS_DATA/EC2/cs/test/" true \
        >> EC2_CHARTS/CACHE_HIT_MM_CS
    ./miss_rate_mm_cs.py $i '/ICDCS/ICDCS_DATA/EC2/EC2_mm_v1/test/' "/ICDCS/ICDCS_DATA/EC2/cs/test/" true \
        >> EC2_CHARTS/MISS_RATE_MM_CS
done

echo "" > EC2_CHARTS/CACHE_HIT_MM_SH
echo "" > EC2_CHARTS/MISS_RATE_MM_SH

for i in 24 48 96 192
do
    ./cache_hit_mm_sh.py $i '/ICDCS/ICDCS_DATA/EC2/EC2_mm_v1/test/' "/ICDCS/ICDCS_DATA/EC2/sh/no_ac/" true \
        >> EC2_CHARTS/CACHE_HIT_MM_SH
    ./miss_rate_mm_sh.py $i '/ICDCS/ICDCS_DATA/EC2/EC2_mm_v1/test/' "/ICDCS/ICDCS_DATA/EC2/sh/no_ac/" true \
        >> EC2_CHARTS/MISS_RATE_MM_SH
done

echo "" > EC2_CHARTS/CACHE_HIT_AC_SH
echo "" > EC2_CHARTS/MISS_RATE_AC_SH
for i in 24 48 96 192
do
    ./cache_hit_mm_ac.py $i '/ICDCS/ICDCS_DATA/EC2/EC2_mm_v1/test/' "/ICDCS/ICDCS_DATA/EC2/sh/ac/" true \
        >> EC2_CHARTS/CACHE_HIT_AC_SH
    ./miss_rate_mm_ac.py $i '/ICDCS/ICDCS_DATA/EC2/EC2_mm_v1/test/' "/ICDCS/ICDCS_DATA/EC2/sh/ac/" true \
        >> EC2_CHARTS/MISS_RATE_AC_SH
done
