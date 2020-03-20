import pandas as pd
import numpy as np
from scipy import stats
from operator import itemgetter
import re
import json
import matplotlib.pyplot as plt

import networkx as nx
import pymongo


client = pymongo.MongoClient('localhost', 27017)
db = client.Stream
tweets = db.secondary_stream

# Get the basic information about user
def get_basics(tweets_final):
    print("=== Getting Basics ===")
    tweets_final["screen_name"] = tweets_df['user.screen_name']
    tweets_final["user_id"] = tweets_df["user.id"]
    tweets_final["followers_count"] = tweets_df["user.followers_count"]
    return tweets_final



# Get retweets
def get_retweets(tweets_final):
    if 'retweeted_status' in tweet:
        user = tweet['user']['screen_name']
        retweeted_user = tweet['retweeted_status']['user']['screen_name']
        return user, retweeted_user
    else:
        return None

# Get quoted tweets
def get_quoted(tweets_final):
    if tweet['is_quote_status']!=False:
        user = tweet['user']['screen_name']
        quoted_user = tweet['quoted_status']['user']['screen_name']

        return user, quoted_user
    else:
        return None 


# Get the interactions between the different users


# Get the information about replies
def get_in_reply(tweet):
    if tweet['in_reply_to_screen_name'] !=None:
        user = tweet['user']['screen_name']
        reply_user = tweet['in_reply_to_screen_name']
        return user, reply_user
    else:
        return None




#get tweets, defsult limit to 10000
tweets_df = tweets.find().limit(10000)
#declare three seperate graphs
Replygraph = nx.Graph()
Quotegraph = nx.Graph()
RetweetGraph = nx.Graph()

#Print statistics of the graph then draw it and save it to a png image file
def graphData(graph, graphName):
    print(f"There are {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges present in the Graph")

    degrees = [val for (node, val) in graph.degree()]
    print(f"The maximum degree of the Graph is {np.max(degrees)}")
    print(f"The minimum degree of the Graph is {np.min(degrees)}")
    print(f"The average degree of the nodes in the Graph is {np.mean(degrees):.1f}")
    print(f"The most frequent degree of the nodes found in the Graph is {stats.mode(degrees)[0][0]}")


    pos = nx.spring_layout(graph, k=0.15)
    plt.figure()
    nx.draw(graph, pos=pos, edge_color="black", linewidths=0.05,
            node_size=10, alpha=0.6, with_labels=False)
    nx.draw_networkx_nodes(graph, pos=pos, node_size=50, node_color=range(graph.number_of_nodes()), cmap="coolwarm",)
    plt.savefig(f'{graphName}.png')
    plt.show()

#For each tweets get their replies, quote tweets and retweets and draw an edge between the users this connects them to
for tweet in tweets_df:
    #print (tweet)
    if get_in_reply(tweet)!=None:
        user, interaction = get_in_reply(tweet)
        Replygraph.add_edge(user, interaction)
    if get_quoted(tweet) != None:
        user, interaction = get_quoted(tweet)
        Quotegraph.add_edge(user,interaction)
    if get_retweets(tweet) != None:
        user, interaction = get_retweets(tweet)
        RetweetGraph.add_edge(user, interaction)
#call graphData method for each of the three graphs   
graphData(Replygraph, 'ReplyGraph')
graphData(Quotegraph, 'QuoteGraph')
graphData(RetweetGraph, 'RetweetGraph')

