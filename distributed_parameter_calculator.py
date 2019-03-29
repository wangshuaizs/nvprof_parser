# -*- coding: utf-8 -*-  
from __future__ import print_function

import numpy as np  
import argparse
import socket
import linecache
import re

def main():
    parser = argparse.ArgumentParser(description="progrom description")
    parser.add_argument('-f', '--file', type=str, default="parameters.txt")
    args = parser.parse_args()
    tracefile = args.file

    parameter_load = {}

    line_cur = 1
    while 1 :
        line = linecache.getline(tracefile, line_cur)
        if not line:
            break
        line = re.sub(r'^v[a-z/0-9: ]*@[/a-z:]*', "", line)
        line = line.split(' ', 1)
        line_0 = line[0]
        line = line[1]
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

        if not parameter_load.has_key(line_0):
            parameter_load[line_0] = mul
            print("--- %d" % mul)
        else:
            parameter_load[line_0] = parameter_load[line_0] + mul
            print("+++ %d" % mul)

        line_cur = line_cur + 1

    print("PS id \t \t Size(Bytes)")
    for i in sorted(parameter_load.keys()):
        print("%s\t:\t%d" % (i, parameter_load[i]*4))

    max_key = max(parameter_load, key=parameter_load.get)
    print("max = %s\t:\t%d" % (max_key, parameter_load[max_key]*4))
    min_key = min(parameter_load, key=parameter_load.get)
    print("min = %s\t:\t%d" % (min_key, parameter_load[min_key]*4))

if __name__ == '__main__':
    main()