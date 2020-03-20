import pymongo
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import datetime
import time
import sys

myclient = pymongo.MongoClient('localhost', 27017)
db = myclient.Stream
collection = db.football_stream

import twitter_credentials as credentials

keywords = ["aston villa", "leicester", "chelsea", "everton", "man utd", "man city", "liverpool","bournemouth","arsenal", "west ham", "crystal palace", "watford", "sheffield united", "norwich", "southampton", "newcastle", "wolves", "brighton", "burnley", "tottenham"]

consumer_key = credentials.CONSUMER_KEY
consumer_secret = credentials.CONSUMER_SECRET
access_token = credentials.ACCESS_TOKEN
access_token_secret = credentials.ACCESS_TOKEN_SECRET

class StdOutListener(StreamListener):

    def __init__(self, time_limit = 3600):
        self.duplicates = 0
        self.limit = time_limit
        self.start_time = time.time()

    def on_data(self, tweets):
        if (time.time() - self.start_time) < self.limit:
            tweet = json.loads(tweets)
            try:          
                tweet_id = tweet['id_str']  
                username = tweet['user']['screen_name'] 
                followers = tweet['user']['followers_count'] 
                date = tweet['created_at'] 
                language = tweet['lang']
                hashtags = tweet['entities']['hashtags']
                mentions = tweet['entities']['user_mentions']
                created = datetime.datetime.strptime(date, '%a %b %d %H:%M:%S +0000 %Y')
                text = tweet['text']
                
                if tweet['truncated']==True:
                    
                    text = tweet['extended_tweet']['full_text']

                
                location = tweet['user']['location']
                tweet = {'_id': tweet_id, 'username': username, 'followers': followers, 'text': text, 'hashtags': hashtags,
                         'language': language, 'created': created, 'mentions': mentions, 'user_location': location}
               
                collection.insert_one(tweet)
                return True
            except:
                print(tweet_id)
                self.duplicates += 1
        else:
            return False
    def on_error(self, status):
        print(status)

l = StdOutListener()
try:
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    print("AUTH SUCCESS")
except:
    print("AUTH FAILED")
    sys.exit()

stream = Stream(auth, l)
stream.filter(track=keywords)
print(l.duplicates)