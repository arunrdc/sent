import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from bs4 import BeautifulSoup
import urllib
from newsapi.articles import Articles
from flask import Flask
import json
from pws import Google
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
import requests
import http, urllib, json
class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'fY4Y4VO88mp1wC4pp0FgZpFEG'
        consumer_secret = 'Nmcf1FTDnBsEVKqZWUVbhIeRRPcK0EGjQ45y0BcRzp1EsJMHPF'
        access_token = '253840413-7QlzbpOewByBmUHv0H2td8DbFzt2gn8745HEvdR2'
        access_token_secret = 'dwDmR5HGGcQc1sOXkmNthahisToxov5looybgWHKtl3Ys'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment methodx
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def getTweets(query='AAPL'):
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query, count=20)
    return json.dumps(tweets)
    # picking positive tweets from tweets
    #ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    #print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    # picking negative tweets from tweets
    #ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    #print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    # percentage of neutral tweets
    #print("Neutral tweets percentage: {} %".format(100 * len(tweets - ntweets - ptweets) / len(tweets)))

    # printing first 5 positive tweets
   # print("\n\nPositive tweets:")
    #for tweet in ptweets[:100]:
        #print(tweet['text'])

    # printing first 5 negative tweets
    #print("\n\nNegative tweets:")
    #for tweet in ntweets[:100]:
        #print(tweet['text'])

def news():
  #news = 'this is awesome'
  from newsapi.sources import Sources
  s = Sources(API_KEY="6e8a402cd42f454c80e1377a86cada80")
  print s.search('cnn')
  #analysis = TextBlob(news)
  #print s.search('Obama')
  from pws import Bing

  URL = 'https://www.google.com/search?pz=1&cf=all&ned=us&hl=en&tbm=nws&gl=us&as_q={query}'

  #def run(**params):
      #response = requests.get(URL.format(**params))
      #print response.content, response.status_code

  #run(query="Obama")
  #r = urllib.urlopen('https://www.google.com/search?pz=1&cf=all&ned=us&hl=en&tbm=nws&gl=us&as_q=Obama').read()
  #soup = BeautifulSoup(r,"html")
  #print soup.prettify()
  #print analysis.polarity

subscriptionKey = "9b0d077cb6f648e7855c9286ed0eed0f"

# Verify the endpoint URI.  At this writing, only one endpoint is used for Bing
# search APIs.  In the future, regional endpoints may be available.  If you
# encounter unexpected authorization errors, double-check this value against
# the endpoint for your Bing search instance in your Azure dashboard.
host = "api.cognitive.microsoft.com"
path = "/bing/v7.0/news/search"

term = "Microsoft"

def BingNewsSearch(search):
    "Performs a Bing News search and returns the results."

    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
    conn = http.client.HTTPSConnection(host)
    query = urllib.parse.quote(search)
    conn.request("GET", path + "?q=" + query, headers=headers)
    response = conn.getresponse()
    headers = [k + ": " + v for (k, v) in response.getheaders()
                   if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]
    return headers, response.read().decode("utf8")

    print('Searching news for: ', term)

    headers, result = BingNewsSearch(term)
    print("\nRelevant HTTP Headers:\n")
    print("\n".join(headers))
    print("\nJSON Response:\n")
    print(json.dumps(json.loads(result), indent=4))

@app.route("/tweets/<topic>")
def tweetSentiment(topic):
    return getTweets(query=topic)

if __name__ == "__main__":
    #BingNewsSearch('Obama')
    # calling main function
    news();
    #app.run(host='0.0.0.0', debug=True, port=5000)