from unicodedata import name
import yfinance as yf
from forex_python.converter import CurrencyRates
import sys

def Error_Exit(msg):
    input(msg)
    exit(1)

def ConvertCurrency(amount, from_curr, to_curr):
    final_amt=0.0
    cr = CurrencyRates()
    final_amt = cr.convert(from_curr, to_curr, amount)
    return round(final_amt, 2)

def GetStockPrice(stockname):
    data=yf.Ticker(stockname)
    if not 'symbol' in data.info.keys():
        Error_Exit('No symbol found: {0}'.format(stockname))
    currency = data.info['currency']
    price = data.info['open']
    return price, currency

if __name__ == "__main__":
    if len(sys.argv) != 2:
        Error_Exit ('Error! Give the symbol as an arg')
    stockname=sys.argv[1]
    if stockname is None or '':
        Error_Exit ('Error! Enter valid symbol!')

    # a tuple
    stock_price = GetStockPrice(stockname)
    stock_price_inr = ConvertCurrency(stock_price[0], stock_price[1], 'INR')
    print (str(stock_price_inr) + ' INR')
