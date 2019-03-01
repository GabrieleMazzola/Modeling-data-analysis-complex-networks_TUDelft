# Point 11
import json
import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt

with open('network.json') as f:
    edges_list = json.load(f)

print(f"Loading network with {len(edges_list)} timesteps")

with open('ranking.json') as f:
    ranking = json.load(f)

# Build aggregated network
flat_list = [item for sublist in edges_list for item in sublist]
tmp = list(map(list,zip(*flat_list)))
unique_nodes = set(tmp[0] + tmp[1])

G = nx.Graph()
G.add_nodes_from(list(unique_nodes))
G.add_edges_from([tuple(item) for sublist in edges_list for item in sublist])


#Degree
degrees = G.degree
degrees = sorted(degrees, key=lambda x: x[1], reverse=True)
#print(degrees)

#Clustering coefficient
clust_coef =list(nx.clustering(G).items())
clust_coef = sorted(clust_coef, key=lambda x: x[1], reverse=True)
#print(clust_coef)

print(len(ranking), len(degrees), len(clust_coef))

