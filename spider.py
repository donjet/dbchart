#!/usr/bin/python
## -*- coding: utf-8 -*-

import os
import re
import sys
import codecs
import csv
import string
#import pylab as pl
import getopt
import all_code
import subprocess
"""
    Download all fundamental info from sina finance data.
"""
profit_url   = "http://money.finance.sina.com.cn/corp/go.php/vDOWN_ProfitStatement/displaytype/4/stockid/STK_CODE/ctrl/all.phtml"
debet_url    = "http://money.finance.sina.com.cn/corp/go.php/vDOWN_BalanceSheet/displaytype/4/stockid/STK_CODE/ctrl/all.phtml"
cashflow_url = "http://money.finance.sina.com.cn/corp/go.php/vDOWN_CashFlow/displaytype/4/stockid/STK_CODE/ctrl/all.phtml"
testing_stk_code = ("002223.SZ",
"300003.SZ",
"300396.SZ",
"002690.SZ",
"300038.SZ",
"002174.SZ",
"002619.SZ",
"600754.SH",
"601318.SH",
"300285.SZ",
"002455.SZ",
"600731.SH",
"002597.SZ",
"300429.SZ",
"600273.SH",
"002562.SZ",
"600075.SH",
"002206.SZ",
"600789.SH",
"002294.SZ",
"600867.SH",
"600201.SH",
"600436.SH",
"600332.SH",
"002019.SZ",
"300009.SZ",
"600566.SH",
"600557.SH",
"002262.SZ",
"600085.SH",
"000538.SZ",
"600513.SH",
"600750.SH",
"002773.SZ",
"000513.SZ",
"300357.SZ",
"600276.SH",
"300015.SZ",
"600763.SH",
"601888.SH",
"002027.SZ",
"600978.SH",
"600477.SH",
"000156.SZ",
"002739.SZ",
"300144.SZ",
"002466.SZ",
"002372.SZ",
"000887.SZ",
"002450.SZ",
"002382.SZ",
"002320.SZ",
"601000.SH",
"600798.SH",
"600323.SH",
"002536.SZ",
"603306.SH",
"002126.SZ",
"601799.SH",
"300258.SZ",
"300176.SZ",
"603568.SH",
"300296.SZ",
"600703.SH",
"300373.SZ",
"002635.SZ",
"002600.SZ",
"002189.SZ",
"002449.SZ",
"002222.SZ",
"300455.SZ",
"300136.SZ",
"002129.SZ",
"000333.SZ",
"002508.SZ",
"000418.SZ",
"002706.SZ",
"002677.SZ",
"600163.SH",
"600308.SH",
"002078.SZ",
"600987.SH",
"002516.SZ",
"600009.SH",
"000089.SZ",
"600179.SH",
"002405.SZ",
"300185.SZ",
"300145.SZ",
"300193.SZ",
"000429.SZ",
"002032.SZ",
"601398.SH",
"603939.SH",
"601607.SH",
"603883.SH",
"600176.SH",
"600529.SH",
"600887.SH",
"002311.SZ",
"600419.SH",
"603288.SH",
"603369.SH",
"600519.SH",
"000568.SZ")


def wget_stk_profit(stk_code):
    url_string = profit_url.replace("STK_CODE",stk_code)
    wget_cmd = "wget -o /tmp/PROFIT/log -O /tmp/PROFIT/" + stk_code +".csv  " + url_string
    subprocess.call(wget_cmd,shell=True)

def wget_stk_debet(stk_code):
    url_string = debet_url.replace("STK_CODE",stk_code)
    wget_cmd = "wget -o /tmp/PROFIT/log  -O /tmp/DEBET/" + stk_code +".csv  " + url_string
    subprocess.call(wget_cmd,shell=True)


def wget_stk_cashflow(stk_code):
    url_string = cashflow_url.replace("STK_CODE",stk_code)
    wget_cmd = "wget -o /tmp/PROFIT/log  -O /tmp/CASHFLOW/" + stk_code +".csv " + url_string
    subprocess.call(wget_cmd,shell=True)


def wget_stk_data(stk_code):
    wget_stk_profit(stk_code)
    wget_stk_debet(stk_code)
    wget_stk_cashflow(stk_code)

def wget_all_info():
    for i in range(len(all_code.all_stk_codes)):
        stock_code = (all_code.all_stk_codes[i]).split('.')[0]
        wget_stk_profit(stock_code)
        wget_stk_debet(stock_code)
        wget_stk_cashflow(stock_code)

def unit_test():
    for i in range(len(testing_stk_code)):
        stock_code = (testing_stk_code[i]).split('.')[0]
        wget_stk_profit(stock_code)
        wget_stk_debet(stock_code)
        wget_stk_cashflow(stock_code)

if __name__ == "__main__":
    unit_test()

