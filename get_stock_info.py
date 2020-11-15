import requests
import json
import os
from datetime import datetime
from errors import NoReturnPayload

def get_metadata(symbol):
    parameters = {
        'function': 'OVERVIEW',
        'symbol': symbol,
        'apikey': os.environ.get('ALPHAVANTAGE_API_KEY')}
    response = requests.get("https://www.alphavantage.co/query", params=parameters)
    response_dict = response.json()
    if (bool(response_dict) == False):
        raise NoReturnPayload()
    keys = ['AssetType', 'Name', 'Exchange', 'Currency', 'Country', 'Sector',
     'Industry', 'FiscalYearEnd', 'LatestQuarter', 'MarketCapitalization', 'PERatio',
     'PEGRatio', 'EPS', 'ReturnOnEquityTTM', 'AnalystTargetPrice', 'PriceToBookRatio',
     'Beta', 'PayoutRatio']
    output = {k: response_dict[k] for k in keys}
    return(output)

def get_stock_price(symbol):
    parameters = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'symbol': symbol,
        'apikey': os.environ.get('ALPHAVANTAGE_API_KEY'),
        'outputsize': 'compact'}
    response = requests.get("https://www.alphavantage.co/query", params=parameters)
    response_dict = response.json()
    if ('Error Message' in response_dict.keys()):
        raise NoReturnPayload()
    response_dict = response_dict["Time Series (Daily)"]
    latest_info = max(response_dict.keys())
    response_dict = response_dict[latest_info]
    response_dict['open'] = response_dict.pop('1. open')
    response_dict['high']  = response_dict.pop('2. high')
    response_dict['low'] = response_dict.pop('3. low')
    response_dict['close'] = response_dict.pop('4. close')
    response_dict['adjusted_close'] = response_dict.pop('5. adjusted close')
    response_dict['volume'] = response_dict.pop('6. volume')
    response_dict['dividend_amount'] = response_dict.pop('7. dividend amount')
    response_dict['split_coefficient'] = response_dict.pop('8. split coefficient')
    output = {latest_info: response_dict}
    return(output)