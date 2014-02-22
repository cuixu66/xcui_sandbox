#!/bin/bash

echo "" > EC2_CHARTS/MISS_RATE_DN_CS
for i in 24 48 96 192
do
    ./miss_rate_dn_cs.py $i '/ICDCS/ICDCS_DATA/EC2/dn/test/' "/ICDCS/ICDCS_DATA/EC2/cs/test/" true \
        >> EC2_CHARTS/MISS_RATE_DN_CS
done

for i in 24 48 96 192
do
    ./cache_hit_cs_sh.py $i '/ICDCS/ICDCS_DATA/EC2/cs/test/' "/ICDCS/ICDCS_DATA/EC2/sh/no_ac/" true
    ./miss_rate_cs_sh.py $i '/ICDCS/ICDCS_DATA/EC2/cs/test/' "/ICDCS/ICDCS_DATA/EC2/sh/no_ac/" true
done

# echo "" > EC2_CHARTS/CACHE_HIT_AC_SH
# echo "" > EC2_CHARTS/MISS_RATE_AC_SH
# for i in 24 48 96 192
# do
#     ./cache_hit_mm_ac.py $i '/ICDCS/ICDCS_DATA/EC2/EC2_mm_v1/test/' "/ICDCS/ICDCS_DATA/EC2/sh/ac/" true \
#         >> EC2_CHARTS/CACHE_HIT_AC_SH
#     ./miss_rate_mm_ac.py $i '/ICDCS/ICDCS_DATA/EC2/EC2_mm_v1/test/' "/ICDCS/ICDCS_DATA/EC2/sh/ac/" true \
#         >> EC2_CHARTS/MISS_RATE_AC_SH
# done
