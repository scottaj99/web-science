import pandas as pd
import json
import matplotlib.pyplot as plt
import networkx as nx
import pymongo
from collections import Counter
import numpy as np
from scipy import stats

#connect to db
client = pymongo.MongoClient('localhost', 27017)
db = client.Stream
tweets = db.football_stream

#method that returns all users, if any, mentioned in the tweet
def get_mentions(row):
    user = row['username']
    mentions=[]
    if row['mentions'] !=[]:
        for item in row['mentions']:
            mentions.append(item['screen_name'])
    return user, mentions

#Normalise data so that it is usable in json format
tweets_df = pd.json_normalize(tweets.find({}).limit(10000), max_level=2)
#declare graph
graph = nx.Graph()
#for statement that gets the mentions for each user and creates an edge between them
for index, tweet in tweets_df.iterrows():
    user, mentions = get_mentions(tweet)
    for mention in mentions:
        graph.add_edge(user, mention)

#graph statistics for analysis
print(f"Graph has {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges.")
degrees = [val for (node, val) in graph.degree()]
print(f"The maximum degree of the Graph is {np.max(degrees)}")
print(f"The minimum degree of the Graph is {np.min(degrees)}")
print(f"The average degree of the nodes in the Graph is {np.mean(degrees):.1f}")
print(f"The most frequent degree of the nodes found in the Graph is {stats.mode(degrees)[0][0]}")

#draws graph and saves it as a .png image file
pos = nx.spring_layout(graph, k=0.15)
plt.figure()
nx.draw(graph, pos=pos, edge_color="black", linewidths=0.05,
        node_size=10, alpha=0.6, with_labels=False)
nx.draw_networkx_nodes(graph, pos=pos, node_size=50, node_color=range(graph.number_of_nodes()), cmap="coolwarm",)
plt.savefig('graphfinal.png')
plt.show()
