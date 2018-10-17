from django.shortcuts import render
from .loader import *
from django.http import HttpResponse

# Create your views here.


def index(request):
    load_stock_data()
    return render(request, 'index.html')

def load_ts(request):
    ts = load_ohlc_stock('SCP')
    context = {'data': ts}
    return render(request, 'load_ts.html', context)

def raw(request):

    read_all_csv()
    #write_stocks_file()
    #write_stocks_index()
    context = {'pizza1': 10,
               'pizza2': 20,
               'pizza3': 30,
               'pizza4': 40,
               }
    return render(request, 'raw.html', context)
    '''
    stock_lst = load_stock_data()
    context = {
        'stock_lst': stock_lst,
    }
    for key, values in stock_lst.items():
        print(key)
        print(values['d'])
        print(values['o'])
        print(values['h'])
        print(values['l'])
        print(values['c'])
        print(values['vol'])
        print(values['val'])

    return render(request, 'raw.html', context)'''