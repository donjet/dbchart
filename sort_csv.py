#!/usr/bin/python
## -*- coding: utf-8 -*-

import os
import re
import sys
import codecs
import csv
import string
import matplotlib.pyplot as plt
import pylab as pl
import getopt
import all_code
"""
    draw charts according to the csv data
"""
data_set_len = 0
quarter_list = ['','']
sort_info = []

def adjust_to_quarter(csv_content):
    global quarter_list
    global data_set_len


    time_slot = len(csv_content[0]) - 1
    print( time_slot)
    for j in range(time_slot):
        if j < (time_slot-1):
	    if not quarter_list[data_set_len - 1 - j ].endswith('Q1X'):
                csv_content[2][time_slot - j ] = round(
                    string.atof(csv_content[2][time_slot -j ]) -\
                                    string.atof(csv_content[2][time_slot -j - 1]),2)
                csv_content[4][time_slot - j ] = round(
                    string.atof(csv_content[4][time_slot -j ]) -\
                                    string.atof(csv_content[4][time_slot -j -
                                        1]), 2)
            else:
                csv_content[2][time_slot - j ] =  \
                    round(string.atof(csv_content[2][time_slot -j ]),2)
                csv_content[4][time_slot - j ] =  \
                    round(string.atof(csv_content[4][time_slot -j ]),2)
        csv_content[1][time_slot - j ] = \
                    round(string.atof(csv_content[1][time_slot - j ]),2)
        csv_content[0][time_slot - j ] = \
                    round(string.atof(csv_content[0][time_slot- j ]),2)
        for i in range(8):
            if csv_content[i][time_slot - j] == str('\\N'):
                csv_content[i][time_slot - j] = 0
            else:
                csv_content[i][time_slot - j] = \
                    round(string.atof(csv_content[i][time_slot -j]),2)

    for j in range(8):
        pass #print csv_content[j]


def create_sort_info(csv_file_name):
    global sort_info
    row_count = 0
    csv_contents = ['','','','','','','','','','']
    data_set_len = len(all_code.time_quarter_set)
    roe         =['roe']
    gross       =['gross']
    revenue     =['revenue']
    yoy_rev     =['yoy_rev']
    profit      =['profit']
    yoy_net     =['yoy_net']
    cf_sale     =['cf_sale']
    cf_sale_qoq =['cf_qoq']
    profit_qrt_cnt = 0
    profit_yoy_sum = 0
    cash_flow_cnt = 0

    with open(csv_file_name, 'rb') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
                roe.append( row[1] )
                gross.append( row[2] )
                revenue.append( row[3] )
                yoy_rev.append( row[4] )
                profit.append( row[5] )
                yoy_net.append( row[6] )
                cf_sale.append( row[7] )
                cf_sale_qoq.append(row[8])
                row_count +=1
                print(row)
        csv_contents[0] = roe
        csv_contents[1] = gross
        csv_contents[2] = revenue
        csv_contents[3] = yoy_rev
        csv_contents[4] = profit
        csv_contents[5] = yoy_net
        csv_contents[6] = cf_sale
        csv_contents[7] = cf_sale_qoq

    adjust_to_quarter(csv_contents)

    time_slot = len(csv_contents[0]) - 1
    for j in range(time_slot):
        if csv_contents[5][time_slot - j ] > 0:
            profit_qrt_cnt += 1
            profit_yoy_sum += csv_contents[5][time_slot-j]
        else:
            break

    for j in range(time_slot):
        if string.atof(csv_contents[6][time_slot -j ]) > 0:
                cash_flow_cnt  += 1
        else:
            break

    if profit_qrt_cnt > 11 and cash_flow_cnt > 3:  #recent 3 years
        sort_info.append( [profit_qrt_cnt,round(profit_yoy_sum/profit_qrt_cnt, \
            2),cash_flow_cnt,os.path.basename(csv_file_name).split('.')[0][2:]])
    else:
        return
    #    sort_info = [csv_file_name.split('.')[0], profit_qrt_cnt, 0]

def quick_sort(array):
    def recursive(begin, end, index):
        if begin > end:
            return
        l, r = begin, end
        pivot = array[l][index]
        while l < r:
            while l < r and array[r][index] > pivot:
                r -= 1
            while l < r and array[l][index] <= pivot:
                 l += 1
            array[l], array[r] = array[r], array[l]
        array[l], array[begin] = array[begin], array[l]
        recursive(begin, l - 1,index)
        recursive(r + 1, end,index)

    recursive(0, len(array) - 1,0)

    end = len(array)-1
    begin = len(array)-1
    pivot = array[len(array)-1][0]
    for i in range(len(array)):
        if array[len(array)-i-2][0] == pivot:
            begin -=1
        else:
            recursive(begin, end,1)
            end = begin-1
            begin = begin-1
            pivot = array[len(array)-1-i][0]

    return array

def sort_dir(argv):
    global data_set_len
    global quarter_list

    data_set_len = len(all_code.time_quarter_set)
    quarter_list = list(all_code.time_quarter_set)
    try:
        opts,args = getopt.getopt(argv[1:], 'd:',['dir='])
    except getopt.GetoptError:
        sys.exit(2)
    print(opts,args)

    for opt, value in opts:
        if opt in("-d","--dir"):
            csv_dir_name = value

    file_list = os.listdir(csv_dir_name)

    for i in range(0,len(file_list)):
        file_path = os.path.join(csv_dir_name,file_list[i])
        if os.path.isfile(file_path) and \
                (os.path.basename(file_path)).endswith('csv'):
            create_sort_info(file_path)
    quick_sort(sort_info)
    with open('/tmp/sorted.csv', 'a+') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(sort_info)


if __name__ == "__main__":
    sort_dir(sys.argv)

