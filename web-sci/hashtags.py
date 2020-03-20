import pandas as pd
import numpy as np
from scipy import stats
import json
import matplotlib.pyplot as plt
import networkx as nx
import pymongo
from collections import Counter
import itertools

client = pymongo.MongoClient('localhost', 27017)
db = client.Stream
tweets = db.football_stream

def get_hashtags(row):
    user = row['hashtags']
    hashtags=[]
    if row['hashtags'] !=[]:
        for item in row['hashtags']:
            hashtags.append(item['text'])
    return user, hashtags



tweets_df = pd.json_normalize(tweets.find({}).limit(50000), max_level=2)
graph = nx.Graph()
for index, tweet in tweets_df.iterrows():
    user, hashtags = get_hashtags(tweet)
    #tweet_id = tweet['_id']
    if len(hashtags) > 1:
        combos = list(itertools.combinations(hashtags,2))
        for combo in combos:
            graph.add_edge(combo[0],combo[1])
    elif len(hashtags) == 1:
        graph.add_node(hashtags[0])
        #graph.nodes()["name"] = user
        #graph.nodes()["name"] = mention
print(f"Graph has {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges.")
degrees = [val for (node, val) in graph.degree()]
print(f"The maximum degree of the Graph is {np.max(degrees)}")
print(f"The minimum degree of the Graph is {np.min(degrees)}")
print(f"The average degree of the nodes in the Graph is {np.mean(degrees):.1f}")
print(f"The most frequent degree of the nodes found in the Graph is {stats.mode(degrees)[0][0]}")
#print(graph.nodes())
pos = nx.spring_layout(graph, k=0.15)
plt.figure()
nx.draw(graph, pos=pos, edge_color="black", linewidths=0.05,
        node_size=10, alpha=0.6, with_labels=True)
nx.draw_networkx_nodes(graph, pos=pos, node_size=50, node_color=range(graph.number_of_nodes()), cmap="PiYG",)
plt.savefig('graphfinal.png')
plt.show()