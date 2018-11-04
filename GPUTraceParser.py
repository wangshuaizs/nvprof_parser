# -*- coding: utf-8 -*-  
from __future__ import print_function

import numpy as np  
import argparse
import matplotlib.pyplot as plt 
import socket
import linecache
from openpyxl import Workbook

locator = 'K40c'
computation_start_flag = 'cudnn::detail::implicit_convolve_sgemm'
computation_stop_flag = 'cudnn::detail::wgrad_alg0_engine'
computation_start_time_list = []
computation_stop_time_list = []

def get_time_in_ms(str):
    s = str[:-1]
    if s[-1] == 'n':
        t = float(s[:-1])/1000000
    elif s[-1] == 'u':
        t = float(s[:-1])/1000
    elif s[-1] == 'm':
        t = float(s[:-1])
    else:
        t = float(s)*1000
    return t

def main():
    parser = argparse.ArgumentParser(description="progrom description")
    parser.add_argument('-f', '--file', type=str, default="nvprofoutput.txt")
    parser.add_argument('-x', '--xlsxfile', type=str, default="wait_time.xlsx")
    args = parser.parse_args()
    tracefile = args.file
    xlsxfile = args.xlsxfile

    line_cur = 2
    while 1 :
        line = linecache.getline(tracefile, line_cur) # skip the first line
        if not line:
            break
        line = line.split()
        if len(line) >= 20:  # for CUDA compute
            if locator in line:
                base_position=line.index(locator)
                if line[base_position + 5].find(computation_start_flag) != -1:
                    computation_start_time_list.append(get_time_in_ms(line[0]))
                elif line[base_position + 5].find(computation_stop_flag) != -1:
                    computation_stop_time_list.append(get_time_in_ms(line[0])+get_time_in_ms(line[1]))
        elif len(line) == 19:  # for CUDA memcpy copy
            pass
                
        line_cur = line_cur + 1

    
    wb = Workbook()
    sheet = wb.active
    sheet["A1"].value = "relative_step"
    sheet["B1"].value = "start_time (ms)"
    sheet["C1"].value = "stop_time (ms)"
    sheet["D1"].value = "wait_time_after_last_step (ms)"
    sheet["E1"].value = "compute_time (ms)"
    for i in xrange(len(computation_start_time_list)):
        sheet["A"+str(i+2)].value = i+1
        sheet["B"+str(i+2)].value = computation_start_time_list[i]
        sheet["C"+str(i+2)].value = computation_stop_time_list[i]
        if i < len(computation_start_time_list) - 1:
            wait_time = computation_start_time_list[i+1] - computation_stop_time_list[i]
            sheet["D"+str(i+3)].value = wait_time
        sheet["E"+str(i+2)].value = computation_stop_time_list[i] - computation_start_time_list[i]
    wb.save(xlsxfile)

if __name__ == '__main__':
    main()