import json
from unicodedata import name
import yfinance as yf
from forex_python.converter import CurrencyRates
import sys

# exit with error msg
def Error_Exit(msg):
    input(msg)
    exit(1)

# use forex_python module to convert currency
def ConvertCurrency(amount, from_curr, to_curr):
    final_amt=0.0
    cr = CurrencyRates()
    final_amt = cr.convert(from_curr, to_curr, amount)
    return round(final_amt, 2)

# get stp for a symbol, return a tuple of price,curr
def GetStockPrice(stockname):
    data=yf.Ticker(stockname)
    if not 'symbol' in data.info.keys():
        Error_Exit('No symbol found: {0}'.format(stockname))
    currency = data.info['currency']
    price = data.info['open']
    return price, currency

# get total stock value
def GetStockValue(symbol, units):
    stock_price = GetStockPrice(symbol)
    stock_price_inr = ConvertCurrency(stock_price[0], stock_price[1], 'INR')
    return round(stock_price_inr * units, 2)

if __name__ == "__main__":
    json_file = 'MyStockData.json'
    import pandas as pd
    with open(json_file) as data_file:
        data = json.load(data_file)

    if data is None or {}:
        Error_Exit('Invalid user data')

    total_investment_stocks = []
    for stock_list in data.keys():
        for stock in data[stock_list]:
            total_investment_stocks.append(stock)

    for stock_info in total_investment_stocks:
        for symbol, units in stock_info.items():
            print ('Stock: %s, Units: %s, Total Value(INR): %s' %(symbol, units, GetStockValue(symbol, units)))
        
    
