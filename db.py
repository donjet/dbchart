#!/usr/bin/python
#encoding=utf-8

import os
import re
import sys
import codecs
import csv
import string
import getopt
import MySQLdb
import all_code

def usage():
    print("-h --help: print this help message.")
    print("-f --file: csv file used to draw chart.")
    print("-c --code: stock code.")


def db_to_csv(stk_code):
    global time_quarter_set

    conn = MySQLdb.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            db = 'stock_finance',
            charset="utf8",
            use_unicode=True)
    cur = conn.cursor()
    cur.execute('SET NAMES UTF8')

    sql_cmd = ""
    for j in range(len(all_code.time_quarter_set)):
        sql_cmd += "select * from " + all_code.time_quarter_set[j] + " where code=" + "'" + \
                stk_code + "'"
        if j < (len(all_code.time_quarter_set)-1):
            sql_cmd += " union "
    print sql_cmd
    try:
        cur.execute(sql_cmd)
        '''
        cur.execute("select * from Y17Q2 where                \
        code='600176.SH' union select * from Y17Q1 where code='600176.SH' union     \
        select * from Y16Q4 where code='600176.SH' union select * from Y16Q3        \
        where code='600176.SH' union select * from Y16Q2 where code='600176.SH'     \
        union select * from Y16Q1 where code='600176.SH' union select * from        \
        Y15Q4 where code='600176.SH'  union select * from Y15Q3 where               \
        code='600176.SH'  union select * from Y15Q2 where code='600176.SH' union    \
        select * from Y15Q1 where code='600176.SH'  union select * from Y14Q4       \
        where code='600176.SH'  union select * from Y14Q3 where code='600176.SH'    \
        union select * from Y14Q2 where code='600176.SH'  union select * from       \
        Y14Q1 where code='600176.SH' union select * from Y13Q4 where                \
        code='600176.SH'  union select * from Y13Q3 where code='600176.SH'          \
        union select * from Y13Q2 where code='600176.SH' union select * from        \
        Y13Q1 where code='600176.SH'  union select * from Y12Q4 where               \
        code='600176.SH'  union select * from Y12Q3 where code='600176.SH'          \
        union select * from Y12Q2 where code='600176.SH'  union select * from       \
        Y12Q1 where code='600176.SH' ;")
        '''
    except:
        print("exception!")
        return

    for row in cur.fetchall():
        print(row[1].decode('utf-8'))

    conn.commit()

    cur.close()
    conn.close()


def get_from_db(argv):
    try:
        opts,args = getopt.getopt(argv[1:], 'hf:c:',['help','file=','code='])
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
           #chart_csv(csv_file)
        elif opt in("-c","--code"):
            stk_code = value
            print(stk_code)
            db_to_csv(stk_code)
        else:
            usage()


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')

    get_from_db(sys.argv)

