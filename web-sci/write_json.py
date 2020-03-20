import pymongo
import json
from bson import json_util

#connect to db
client = pymongo.MongoClient('localhost', 27017)
db = client.Stream
tweets = db.secondary_stream

#get the first 100 tweets
tweet_set = tweets.find().limit(100)

#write them toa json file
json.dump(json_util.dumps(tweet_set), open("text.json", "w"))