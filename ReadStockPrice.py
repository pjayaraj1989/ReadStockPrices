import json
from unicodedata import name
import yfinance as yf
from currency_converter import CurrencyConverter
from mftool import Mftool
import sys

def Error_Exit(msg):
    input(msg)
    exit(1)

def ConvertCurrency(amount, from_curr, to_curr):
    final_amt=0.0
    c = CurrencyConverter()
    final_amt = c.convert(amount, from_curr, to_curr)
    return round(final_amt, 2)

def GetStockPrice(stockname):
    data=yf.Ticker(stockname)
    if not 'symbol' in data.info.keys():
        Error_Exit('No symbol found: {0}'.format(stockname))
    currency = data.info['currency']
    price = data.info['open']
    return price, currency

def GetStockValue(symbol, units):
    stock_price_inr = 0.0
    amt, curr = GetStockPrice(symbol)
    #convrt from curr to inr
    if curr != 'INR':
        stock_price_inr = ConvertCurrency(amt, curr, 'INR')
    stock_price_inr = amt * units
    return round(stock_price_inr, 2)

#MF data
# this is from 
# https://raw.githubusercontent.com/NayakwadiS/mftool/master/Scheme_codes.txt
# many thanks to the author!
def GetFundData(FundName):
    mt = Mftool()
    codes = mt.get_scheme_codes()
    # search in codes for FundName
    if FundName == '' or None:  Error_Exit('Invalid fund name')
    FundCode = ''
    for k,v in codes.items():
        if FundName in v:   FundCode = k
    if FundCode == '':  Error_Exit('Unable to read fund code for %s' % FundName)
    data = mt.get_scheme_details(FundCode)
    return data['scheme_start_date']['nav']

if __name__ == "__main__":
    json_file = 'MyStockData.json'
    import pandas as pd
    with open(json_file) as data_file:
        data = json.load(data_file)

    if data is None or {}:
        Error_Exit('Invalid user data')

    total_investment_stocks = []
    total_investment_mf = []
    for stock_list in ['NSE', 'NASDAQ']:
        for stock in data[stock_list]:  total_investment_stocks.append(stock)
    for mf_list in ['MF',]:
        for mf in data[mf_list]:    total_investment_mf.append(mf)

    for investment in total_investment_mf:
        for fundname, amt in investment.items():
            print ("Fund:\t%s, NAV:\t%s, Invested Amount:\t%s" 
                        % (fundname, GetFundData(fundname), amt))

    total_valuation = 0.0
    for stock_info in total_investment_stocks:
        for symbol, units in stock_info.items():
            val = GetStockValue(symbol, units)
            print ('Stock: %s, Units: %s, Total Value(INR): %s'
                     %(symbol, units, val))
            total_valuation += val
    
    print ('Total valuation: %s' %total_valuation)
