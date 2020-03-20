import pymongo
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.feature_extraction import DictVectorizer

import re
from collections import Counter


client = pymongo.MongoClient('localhost', 27017)
db = client.Stream
tweets = db.football_stream

documents = []
string_data=[]
username_data = []
hashtag_data = []
grouping_data = []

print("=== Retrieving tweets from database ===")

tweets = tweets.find().limit(50)

for tweet in tweets:
    try:
        grouping_data.append({tweet['username']:tweet['text']})
        if tweet['hashtags'] != []:
            for item in tweet['hashtags']:
                hashtag_data.append(item.get('text'))
            #print(tweet['hashtags'])
        documents.append(tweet['text'])
        username_data.append(tweet['username'])
        ex = tweet['text'].strip().split(' ')
        for item in ex:
            string_data.append(item)
    except:
        pass

#print(hashtag_data)
print("=== Vectorising ===")
vectorizer = TfidfVectorizer(stop_words="english")
vectorizer2 = TfidfVectorizer(stop_words="english")
vectorizer3 = TfidfVectorizer(stop_words="english")
vectorizer4 = DictVectorizer()
text_vector = vectorizer.fit_transform(documents)
hash_vector = vectorizer2.fit_transform(hashtag_data)
user_vector = vectorizer3.fit_transform(username_data)
group_vector = vectorizer4.fit_transform(grouping_data)

true_k = 6
print("=== Preforming KMeans with %d clusters ===" % true_k)
text_model = KMeans(n_clusters=true_k, init='random', max_iter=300, n_init=10)
text_model.fit(text_vector)
hash_model = KMeans(n_clusters=true_k, init='random', max_iter=300, n_init=10)
hash_model.fit(hash_vector)
user_model = KMeans(n_clusters=true_k, init='random', max_iter=300, n_init=10)
user_model.fit(user_vector)
group_model = KMeans(n_clusters=true_k, init='random', max_iter=300, n_init=10)
group_model.fit(group_vector)

print("Top terms per cluster:")
order_centroids = text_model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print("=== Cluster %d, Size: %d ===" % (i,len(order_centroids[i])))
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind])

print("Top hashtags per cluster:")
order_centroids = hash_model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer2.get_feature_names()
for i in range(true_k):
    print("=== Cluster %d, Size: %d ===" % (i,len(order_centroids[i])))
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind])

print("Top usernames per cluster:")
order_centroids = user_model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer3.get_feature_names()
for i in range(true_k):
    print("=== Cluster %d, Size: %d ===" % (i,len(order_centroids[i])))
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind])

print("Users and hashtags per cluster")
order_centroids = group_model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer4.get_feature_names()
for i in range(true_k):
    hashtags = []
    usernames = []
    print("\t=== Cluster %d, Size: %d ===" % (i,len(order_centroids[i])))
    for ind in order_centroids[i, :10]:
        tweet = terms[ind]
        print (tweet)
        tweet = '@'+tweet
        users = re.findall(r'(@\w+)', tweet)
        hashes = re.findall(r'(#\w+)', tweet)
        for item in users:
            usernames.append(item)
        for item in hashes:
            hashtags.append(item)
    print("=== Usernames ===")
    print(Counter(usernames))
    if not hashtags==[]:
        print("=== Hashtags ===")
        print(Counter(hashtags))
    else:
        print("no hashtags")


print(Counter(username_data).most_common(5))
print(Counter(hashtag_data).most_common(5))
print(Counter(string_data).most_common(5))