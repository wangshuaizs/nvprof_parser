# -*- coding: utf-8 -*-  
from __future__ import print_function

import numpy as np  
import argparse
import socket
import linecache

def main():
    parser = argparse.ArgumentParser(description="progrom description")
    parser.add_argument('-f', '--file', type=str, default="parameter_shape.txt")
    args = parser.parse_args()
    tracefile = args.file

    line_cur = 1
    while 1 :
        line = linecache.getline(tracefile, line_cur)
        if not line:
            break
        line = line.split(',')
        mul = 1
        for i in xrange(len(line)):
            if i == 0:
                mul = mul * int(line[i][1:])
            elif i == len(line) - 1:
                if len(line[i]) > 2:  # )\n
                    mul = mul * int(line[i][:-2])
            else:
                mul = mul * int(line[i])

        print(mul)     
        line_cur = line_cur + 1


if __name__ == '__main__':
    main()