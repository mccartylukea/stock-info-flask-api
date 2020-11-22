import os
from flask import Flask, jsonify
from datetime import datetime, timezone
from errors import NoReturnPayload
from get_stock_info import get_metadata, get_stock_price
from get_twitter_data import get_average_sentiment
from google.cloud import language_v1
from google.cloud import secretmanager

app = Flask(__name__)

PROJECT_ID = os.environ.get('PROJECT_ID')

secrets = secretmanager.SecretManagerServiceClient()
os.environ['ALPHAVANTAGE_API_KEY'] = secrets.access_secret_version("projects/"+PROJECT_ID+"/secrets/alphavantage_api_key/versions/1").payload.data.decode("utf-8")
os.environ['TWITTER_BEARER_TOKEN'] = secrets.access_secret_version("projects/"+PROJECT_ID+"/secrets/twitter_bearer_token/versions/1").payload.data.decode("utf-8")
os.environ['GOOGLE_API_KEY'] = secrets.access_secret_version("projects/"+PROJECT_ID+"/secrets/google_api_key/versions/1").payload.data.decode("utf-8")

@app.errorhandler(NoReturnPayload)
def handle_exception(error):
    response = jsonify(error.to_dict())
    return(response)

@app.route('/')
def home():
    return "Please enter a stock symbol (e.g. MSFT) to receive price and sentiment information."

@app.route('/<ticker>')
def return_payload(ticker):
    ticker = ticker.replace('$', '').upper()
    payload = {}
    payload['fetched_at'] =  datetime.now(timezone.utc)
    payload['symbol'] = ticker
    payload['overview'] = get_metadata(ticker)
    payload['latest_market_data'] = get_stock_price(ticker)
    average_sentiment = get_average_sentiment(ticker)['average_sentiment_score']
    payload['average_twitter_sentiment'] = average_sentiment
    return(jsonify(payload))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)