# stock-info-flask-api
This API returns stock price and volume information, important financial metrics, and the average sentiment score of the latest 25 tweets for a given stock symbol.

## Using the API
To query stock information, build the app in Google App Engine and append the desired stock symbol to the app's endpoint.

Example:
```
https://stock-info-flask-api.ue.r.appspot.com/MSFT
```

This will return json output like this:
```
{
  "average_twitter_sentiment":0.08399999976158141,
  "fetched_at":"Sun, 22 Nov 2020 20:33:13 GMT",
  "latest_market_data": {
    "2020-11-20": {
      "adjusted_close":"210.39",
      "close":"210.39",
      "dividend_amount":"0.0000",
      "high":"213.285",
      "low":"210.0",
      "open":"212.2",
      "split_coefficient":"1.0",
      "volume":"22843119"
    }
  },
  "overview":{
    "AnalystTargetPrice":"239.37",
    "AssetType":"Common Stock",
    "Beta":"0.8681",
    "Country":"USA",
    "Currency":"USD",
    "EPS":"6.199",
    "Exchange":"NASDAQ",
    "FiscalYearEnd":"June",
    "Industry":"SoftwareInfrastructure",
    "LatestQuarter":"2020-09-30",
    "MarketCapitalization":"1590653616128",
    "Name":"Microsoft Corporation",
    "PEGRatio":"2.4622",
    "PERatio":"33.9339",
    "PayoutRatio":"0.3376",
    "PriceToBookRatio":"12.8911",
    "ReturnOnEquityTTM":"0.414",
    "Sector":"Technology"
    },
  "symbol":"MSFT"
}
```

## How does it work?
The API is a Flask app deployed to Google App Engine. The stock information comes from [Alpha Vantage](https://www.alphavantage.co/) APIs, using the [Daily Adjusted Time-Series API](https://www.alphavantage.co/documentation/#dailyadj) for equity price and volume information and the [Company Overview API](https://www.alphavantage.co/documentation/#company-overview) for company information and financial ratios/metrics.

The average sentiment score is an average of scores returned by Google's [Cloud Natural Language API](https://cloud.google.com/natural-language/docs/analyzing-sentiment) for the latest 25 tweets containing the input stock symbol. Twitter data is obtained using the [Twitter API](https://developer.twitter.com/en/docs/twitter-api).
