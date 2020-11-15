import requests
import os
import json
from google.cloud import language_v1
from errors import NoReturnPayload


def get_twitter_data(symbol):
    query = symbol + ' -is:retweet lang:en'
    tweet_fields = "tweet.fields=author_id,created_at,text"
    params = 'max_results=25'
    bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')
    headers =  {"Authorization": "Bearer {}".format(bearer_token)}
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&{}".format(
        query, tweet_fields, params
    )
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        raise NoReturnPayload()
    output = response.json()['data']
    return output

def get_sentiment(tweet):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=tweet, type_=language_v1.Document.Type.PLAIN_TEXT)
    result = client.analyze_sentiment(request={'document': document}).document_sentiment.score
    return(result)

def get_average_sentiment(ticker):
    twitter_text = get_twitter_data(ticker)
    output = [get_sentiment(tweet['text']) for tweet in twitter_text]
    output = {"average_sentiment_score": sum(output)/len(output)}
    return(output)