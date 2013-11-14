#!/usr/bin/python -B
import sys
import re
import microfuge_specific.reader as reader
import calculators.moving_avg_calculator as mac

class MicrofugeResultType:
    CACHE_HIT = 1
    DEADLINE_MISS = 2

class MicrofugeArrayGenerator:
    # TODO: get rid of this zero_fill
    def __init__(self,
                 result_type,
                 base_dir, client_num, run_start, run_end, ac_perc = -1, offset = -1, zero_fill = True):
        self.RESULT_TYPE = int(result_type)
        assert(self.RESULT_TYPE == MicrofugeResultType.CACHE_HIT
               or self.RESULT_TYPE == MicrofugeResultType.DEADLINE_MISS)
        self.CLIENT_NUM = str(client_num)
        self.BASE_DIR = str(base_dir)
        self.RUN_START = int(run_start)
        self.RUN_END = int(run_end)
        self.AC_PERC = str(ac_perc)
        self.OFFSET = str(offset)
        self.ZERO_FILL = zero_fill

    def get_overall_percentage(self):
        sum = 0.0
        for i in range(self.RUN_START, self.RUN_END):
            file_name = self.gen_file_name(i)
            count_index = 9
            percentage_index = self.get_index()
            percentage_array = reader.read_value_into_array(file_name, percentage_index)
            count_array = reader.read_value_into_array(file_name, count_index)
            sum += reader.cal_overall_rate(percentage_array, count_array)
        # print sum
        return sum / (self.RUN_END - self.RUN_START)

    def get_moving_avg(self):
        matrix = []
        for i in range(self.RUN_START, self.RUN_END):
            file_name = self.gen_file_name(i)
            index = self.get_index()
            tmp_result = self.get_single_moving_avg(file_name, index);
            matrix.append(tmp_result)
        return mac.cal_avg_array_of_arrays(matrix)

    def get_single_moving_avg(self, file_name, index):
        data_values = reader.read_value_into_array(file_name, index)
        moving_avg_one = mac.get_moving_avg(data_values, 3)
        moving_avg_two = mac.get_moving_avg(data_values, 7)
        moving_avg_three = mac.get_moving_avg(data_values, 31)
        rtn = moving_avg_one[0:21] + moving_avg_two[21:91] + moving_avg_three[91:990]
        return rtn

    # generate the relative index of results for the current calculation based on the current object state
    def get_index(self):
        if(self.RESULT_TYPE == MicrofugeResultType.CACHE_HIT):
            rtn = 6
        elif(self.RESULT_TYPE == MicrofugeResultType.DEADLINE_MISS):
            rtn = 3
        return rtn

    # generate file name to be read based on current object state
    def gen_file_name(self, run_number):
        file_name = (self.BASE_DIR
                     + "client" + str(self.CLIENT_NUM)
                     + "_size100k"
                     # TODO: get rid of this zero_fill
                     + "_run" + (str(run_number).zfill(3) if self.ZERO_FILL else str(run_number))
                     + "_acPerc" + str(self.AC_PERC)
                     + "_off" + str(self.OFFSET))
        return file_name
