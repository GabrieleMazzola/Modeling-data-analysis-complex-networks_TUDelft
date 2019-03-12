# Point 11
import json

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

with open('./data/network.json') as f:
    edges_list = json.load(f)

print(f"Loading network with {len(edges_list)} timesteps")

with open('./data/ranking.json') as f:
    influence = json.load(f)

# Build aggregated network
flat_list = [item for sublist in edges_list for item in sublist]
tmp = list(map(list, zip(*flat_list)))
unique_nodes = set(tmp[0] + tmp[1])

G = nx.Graph()
G.add_nodes_from(list(unique_nodes))
G.add_edges_from([tuple(item) for sublist in edges_list for item in sublist])

# Degree
degrees = G.degree
degrees = sorted(degrees, key=lambda x: x[1], reverse=True)
# print(degrees)

# Clustering coefficient
clust_coef = list(nx.clustering(G).items())
clust_coef = sorted(clust_coef, key=lambda x: x[1], reverse=True)
# print(clust_coef)

print(len(influence), len(degrees), len(clust_coef))


def compute_Rrd(f):
    Rf = [node for node, _ in influence[0:int(f * len(influence))]]
    Df = [node for node, _ in degrees[0:int(f * len(degrees))]]

    intersect = []
    for node in Rf:
        if node in Df:
            intersect.append(node)

    return len(intersect) / len((Rf))


def compute_Rrc(f):
    Rf = [node for node, _ in influence[0:int(f * len(influence))]]
    Cf = [node for node, _ in clust_coef[0:int(f * len(clust_coef))]]

    intersect = []
    for node in Rf:
        if node in Cf:
            intersect.append(node)

    return len(intersect) / len((Rf))


RRCs = []
RRds = []
f_values = np.linspace(0.05, 0.5, 10)
for f in f_values:
    RRCs.append(compute_Rrc(f))
    RRds.append(compute_Rrd(f))

plt.plot(f_values, RRCs, label="Rrc")
plt.xlabel("f")
plt.plot(f_values, RRds, label="Rrd")
plt.xlabel("f")
plt.legend(loc="top left")
plt.show()
