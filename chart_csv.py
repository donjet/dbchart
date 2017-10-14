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

def paint(csv_content, csv_file_name):
    global data_set_len

    png_file_name = csv_file_name.split('.')[0]

    fg = pl.figure()
    ax1 = fg.add_subplot(221)
    ax1.set_title("Revenue Profit Gross",fontsize=12)
    ax1.plot(list(range(data_set_len)), csv_content[2][1:],0.4, 'r')
    ax1.plot(list(range(data_set_len)), csv_content[5][1:],0.4, 'g')

    ax2 = ax1.twinx()
    ax2.plot(list(range(data_set_len)), csv_content[1][1:], 'black')

    ax3 = fg.add_subplot(222)
    ax3.set_title("ROE",fontsize=12)
    ax3.plot(list(range(data_set_len)), csv_content[0][1:], 'y')

    ax4 = fg.add_subplot(223)
    ax4.set_title("Cash Flow vs Profit",fontsize=12)
    ax4.plot(list(range(data_set_len)), csv_content[5][1:], 'b')
    ax4.plot(list(range(data_set_len)), csv_content[8][1:], 'r')

    pl.tight_layout()
    pl.savefig(str(png_file_name))
    pl.close()


def adjust_to_quarter(csv_content):
    global quarter_list

    list_rvnu = [1,1,1]
    list_prft = [1,1,1]
    list_gros = [1,1,1]

    time_slot = data_set_len
    for j in range(time_slot):
	if not quarter_list[time_slot - j -1].endswith('Q1X'):
            csv_content[2][time_slot - j] = ( string.atof(csv_content[2][time_slot -j]) -\
                                    string.atof(csv_content[2][time_slot -j - 1]))
            csv_content[5][time_slot - j] = ( string.atof(csv_content[5][time_slot -j]) -\
                                    string.atof(csv_content[5][time_slot -j - 1]))
        else:
            csv_content[2][time_slot - j] = string.atof(csv_content[2][time_slot -j])
            csv_content[5][time_slot - j] = string.atof(csv_content[5][time_slot -j])
        csv_content[1][time_slot - j] = string.atof(csv_content[1][time_slot -j])
        csv_content[0][time_slot - j] = string.atof(csv_content[0][time_slot -j])
        csv_content[8][time_slot - j] = string.atof(csv_content[8][time_slot -j])

    for j in range(9):
        print csv_content[j]

def chart_csv(csv_file_name):
    row_count = 0
    csv_contents = ['','','','','','','','','','']
    data_set_len = len(all_code.time_quarter_set)
    roe         =['roe'] 
    gross       =['gross'] 
    revenue     =['revenue'] 
    yoy_rev     =['yoy_rev'] 
    qoq_rev     =['qoq_rev'] 
    profit      =['profit'] 
    yoy_net     =['yoy_net'] 
    qoq_net     =['qoq_net'] 
    cf_sale     =['cf_sale'] 
    cf_sale_qoq =['cf_qoq'] 

    with open(csv_file_name, 'rb') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
                roe.append( row[1] )
                gross.append( row[2] )
                revenue.append( row[3] )
                yoy_rev.append( row[4] )
                qoq_rev.append( row[5] )
                profit.append( row[6] )
                yoy_net.append( row[7] )
                qoq_net.append( row[8] )
                cf_sale.append( row[9] )
                cf_sale_qoq.append(row[10])
                row_count +=1
        csv_contents[0] = roe
        csv_contents[1] = gross
        csv_contents[2] = revenue
        csv_contents[3] = yoy_rev
        csv_contents[4] = qoq_rev
        csv_contents[5] = profit
        csv_contents[6] = yoy_net
        csv_contents[7] = qoq_net
        csv_contents[8] = cf_sale
        csv_contents[9] = cf_sale_qoq

    adjust_to_quarter(csv_contents)
    paint(csv_contents, csv_file_name)

def chart_dir(csv_dir_name):
    file_list = os.listdir(csv_dir_name)

    for i in range(0,len(file_list)):
        file_path = os.path.join(csv_dir_name,file_list[i])
        if os.path.isfile(file_path) and \
                (os.path.basename(file_path)).endswith('csv'):
            chart_csv(file_path)

def usage():
    print("-h --help: print this help message.")
    print("-f --file: csv file used to draw chart.")
    print("-d --dir : all files in the directory will be painted.")

def chart_it(argv):
    global data_set_len
    global quarter_list

    data_set_len = len(all_code.time_quarter_set)
    quarter_list = list(all_code.time_quarter_set)
    try:
        opts,args = getopt.getopt(argv[1:], 'hf:d:',['help','file=','dir='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    print(opts,args)

    for opt, value in opts:
        if opt in("-h","--help"):
            usage()
            sys.exit()
        elif opt in("-f","--file"):
            csv_file = value
            print(csv_file)
            chart_csv(csv_file)
        elif opt in("-d","--dir"):
            csv_dir = value
            print(csv_dir)
            chart_dir(csv_dir)




if __name__ == "__main__":
    chart_it(sys.argv)

