import pandas as pd
import csv
import os
import os.path
import glob
from django.contrib.staticfiles.templatetags.staticfiles import static

BASE_DIR = './staticfiles/stocks/'

#rename raw file to be format yyyymmdd this let to be
#able to sorted data time in order
def rename_raw_files():
    path = './staticfiles/csv/*.txt'
    files = sorted(glob.glob(path))
    for file in files:
        name = file
        l = len(name)
        year = name[l-8:l-4]
        month = name[l-10:l-8]
        date = name[l-12:l-10]
        new_name = name[0:l-12] + year + month + date + '.txt'
        print(new_name)
        os.rename(name, new_name)

    return True

#read all .csv in dir
#then call write_stock_file to write each stock file
def read_all_csv():
    path = './staticfiles/csv/*.txt'
    files = sorted(glob.glob(path))
    for file in files:
        print(file)
        write_stocks_file(file)

    return True

    #return how many number contain in stock name
def has_number(str):
    count = 0
    for c in str:
        if c.isdigit():
            count = count + 1

    return count;

def load_stock_data(fname):
    stock_files = fname
    stocks_lst = pd.read_csv(stock_files, delim_whitespace=True, header= None, error_bad_lines=False)
    lst_stock = stocks_lst.values.tolist()
    stock_dict = {}
    for stock in lst_stock:
        #print(stock[0]) #stock name
        #screen dw and something which is not stock out of list
        if '-' in stock[0]:
            continue

        if has_number(stock[0]) > 2 and 'SET' not in stock[0] :
            continue

        stock_dict[stock[0]] = {'d': stock[1], 'o': stock[2], 'h':stock[3], 'l': stock[4], 'c': stock[5], 'vol': stock[6], 'val': stock[7] }
        print(stock_dict[stock[0]])

    #stocks_lst = ['name', 'date', 'open', 'high', 'low', 'close', 'vol', 'val']
    return stock_dict

def write_stocks_file(fname):
    st_list = load_stock_data(fname)
    for key, values in st_list.items():
        print(key)
        print(values['d'])
        print(values['o'])
        print(values['h'])
        print(values['l'])
        print(values['c'])
        print(values['vol'])
        print(values['val'])

        fname = './staticfiles/stocks/' + key + '.csv'
        file_exists = os.path.isfile(fname)
        with open(fname, 'a') as csv_file:
            fieldnames = ['date', 'open', 'high', 'low', 'close', 'vol', 'val']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()

            writer.writerow({'date':values['d'], 'open':values['o'],
                             'high':values['h'], 'low':values['l'],
                             'close':values['c'], 'vol':values['vol'],
                             'val':values['val']})

    return True

#write all stock name to a file
def write_stocks_index():
    st_list = load_stock_data()
    fname =  './staticfiles/stocks/stock_index.csv'
    file_exists = os.path.isfile(fname)
    for key, values in st_list.items():
        with open(fname, 'a') as csv_file:
            fieldnames = ['stocks']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()

            writer.writerow( {'stocks': key} )

    return True

#load stock history price
#input stock name such SVI
#prerequisite all data must be pre prepared
def load_ohlc_stock(stock_name):
    fname = BASE_DIR + stock_name + '.csv'
    stock_ohlcs = pd.read_csv(fname, delimiter=',', header=None, error_bad_lines=False)
    time_series = stock_ohlcs.values.tolist()
    stock_dict = {}
    del time_series[0]
    count = 0
    for ohlc in time_series:
        stock_dict[count] = {'d': ohlc[0], 'o': ohlc[1], 'h': ohlc[2], 'l': ohlc[3]
            , 'c': ohlc[4], 'vol': ohlc[5], 'val': ohlc[6]}
        count = count + 1

    return stock_dict
