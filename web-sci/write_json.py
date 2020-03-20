import pymongo
import json
from bson import json_util

client = pymongo.MongoClient('localhost', 27017)
db = client.Stream
tweets = db.secondary_stream

tweet_set = tweets.find().limit(100)

json.dump(json_util.dumps(tweet_set), open("text.json", "w"))