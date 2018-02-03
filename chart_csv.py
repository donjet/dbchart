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
    data_len = len(csv_content[0]) - 1

    if ((csv_content[5][data_len] > 20) and \
               (csv_content[5][data_len-1] > 20)
               and csv_content[5][data_len - 2] > 20) \
       and ((csv_content[3][data_len] > 20) and \
               (csv_content[3][data_len-1] > 20)\
               and csv_content[3][data_len - 2] > 20):
        pass
    else:
        return

    fg = pl.figure()
    ax1 = fg.add_subplot(221)
    ax1.set_title("Revenue vs Gross",fontsize=12)
    ax1.plot(list(range(data_len)), csv_content[2][1:],0.4,'blue' )
    #ax1.plot(list(range(data_len)), csv_content[5][1:],0.4, 'g')

    ax2 = ax1.twinx()
    ax2.plot(list(range(data_len)), csv_content[1][1:], 'red')

    ax3 = fg.add_subplot(222)
    ax3.set_title("ROE vs Profit/Y",fontsize=12)
    roe_yoy = []
    for i in range((data_len+3)/4) :
        if not data_len%4:
            roe_yoy.append(csv_content[0][i*4 + 4])
        else:
            roe_yoy.append(csv_content[0][i*4 +  data_len%4])
    ax3.plot(list(range((data_len+3)/4) ), roe_yoy[0:], 'y')

    ax31 = ax3.twinx()
    cash_flow = []
    profit = []
    i = 0
    for i in range(data_len/4):
        cash_flow.append(csv_content[6][i*4+1] + csv_content[6][i*4+2] \
                + csv_content[6][i*4+3] + csv_content[6][i*4+4])
        profit.append(csv_content[4][i*4+1] + csv_content[4][i*4+2] \
                + csv_content[4][i*4+3] + csv_content[4][i*4+4])
    i = i+1
    cash_flow_last = 0.0
    profit_last = 0.0
    if  (data_len%4):
        last_len = data_len%4
        for j in range(last_len ):
            cash_flow_last += csv_content[6][i*4 + j + 1]
            profit_last += csv_content[4][i*4 + j + 1]
        cash_flow_last = cash_flow_last * 4 / (data_len%4)
        profit_last = profit_last * 4 / (data_len%4)
        cash_flow.append(cash_flow_last)
        profit.append(profit_last)
    ax31.plot(list(range((data_len+3)/4) ), cash_flow[0:], 'black')
    ax31.plot(list(range((data_len+3)/4) ), profit[0:], 'red')
    print(cash_flow)
    print(profit)

    ax4 = fg.add_subplot(223)
    ax4.set_title("Cash Flow vs Profit",fontsize=12)
    ax4.plot(list(range(data_len)), csv_content[4][1:], 'b')
    ax4.plot(list(range(data_len)), csv_content[6][1:], 'r')

    ax5 = fg.add_subplot(224)
    ax5.set_title("Profit YoY Ratio",fontsize=12)
    ax5.plot(list(range(data_len)), csv_content[5][1:], 'b')
    '''
    ax6 = ax5.twinx()
    ax6.plot(list(range(data_len)), csv_content[5][1:], 'r')
    '''
    pl.tight_layout()
    pl.savefig(str(png_file_name))
    pl.close()


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
        print csv_content[j]

def chart_csv(csv_file_name):
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
        csv_contents[0] = roe
        csv_contents[1] = gross
        csv_contents[2] = revenue
        csv_contents[3] = yoy_rev
        csv_contents[4] = profit
        csv_contents[5] = yoy_net
        csv_contents[6] = cf_sale
        csv_contents[7] = cf_sale_qoq

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

    print(argv)
    data_set_len = len(all_code.time_quarter_set)
    quarter_list = list(all_code.time_quarter_set)
    try:
        opts,args = getopt.getopt(argv[1:], 'lhf:d:',['last','help','file=','dir='])
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
        elif opt in("-l","--last"):
            data_set_len = len(all_code.time_quarter_set)-1
            quarter_list = list(all_code.time_quarter_set)
            quarter_list.pop()




if __name__ == "__main__":
    chart_it(sys.argv)

