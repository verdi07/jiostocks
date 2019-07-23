# Program that gets data from the internet and saves it to plot later

# Libraries
import pandas as pd # Work with databases
from pandas_datareader import data as web # Get data from the internet
import yfinance as yf # Fix the connection problem with the yahoo API
import datetime as dt # Work with dates
import sys # In case of error quit

yf.pdr_override() # Fix the API con

def main():
    mode = input('You can select the companies you want to get data from (manual) [enter "M"] or get 4 automatic companies (automatic) [press "A"]')
    start = dt.datetime(1960, 1, 1)
    end = dt.datetime.now()
    if mode == 'M':
        company1 = input('Enter the ticker of the first company you want to study')
        comp1 = web.DataReader(company1, 'yahoo', start, end)

        company2 = input('Enter the ticker of the second company you want to study')
        comp2 = web.DataReader(company2, 'yahoo', start, end)

        company3 = input('Enter the ticker of the third company you want to study')
        comp3 = web.DataReader(company3, 'yahoo', start, end)

        company4 = input('Enter the ticker of the fourth company you want to study')
        comp4 = web.DataReader(company4, 'yahoo', start, end)

    elif mode == 'A':
        comp1 = web.DataReader('AAPL', 'yahoo', start, end)
        comp2 = web.DataReader('TSLA', 'yahoo', start, end)
        comp3 = web.DataReader('NKE', 'yahoo', start, end)
        comp3 = web.DataReader('AMZN', 'yahoo', start, end)

    else:
        print('You did not select automatic "A" or manual "M" mode')
        sys.exit()


if __name__ == '__main__':
    main()
