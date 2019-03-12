from complex_net_assignment.util import load_network, load_infection_ranking, build_graph_from_dataset, compute_ranking
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


graph_dataset = load_network('./data/network.json')
infect_ranking = load_infection_ranking("./data/ranking.json")

graph, unique_nodes = build_graph_from_dataset(graph_dataset)

bets = list(nx.betweenness_centrality(graph).items())
bets = sorted(bets, key=lambda x: x[1], reverse=True)


f_values, RRbs = compute_ranking(infect_ranking, bets)
plt.plot(f_values, RRbs)
plt.ylabel("rRB")
plt.xlabel("f")
plt.show()


#Temporal networks
timestep_dict = dict.fromkeys(list(unique_nodes),0)

for timestep in graph_dataset:
    added_nodes = []
    for conn in timestep:
        if conn[0] not in added_nodes:
            timestep_dict[conn[0]] += 1
            added_nodes.append(conn[0])
        if conn[1] not in added_nodes:
            timestep_dict[conn[1]] += 1
            added_nodes.append(conn[1])

timesteps = list(timestep_dict.items())
timesteps = sorted(timesteps, key=lambda x: x[1], reverse=True)
print(timesteps)


f_values, RTs = compute_ranking(infect_ranking, timesteps)


# Point 11
import json
import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt

with open('./data/network.json') as f:
    edges_list = json.load(f)

print(f"Loading network with {len(edges_list)} timesteps")

with open('./data/ranking.json') as f:
    influence = json.load(f)

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

print(len(influence), len(degrees), len(clust_coef))


def compute_Rrd(f):
    Rf = [node for node, _ in influence[0:int(f*len(influence))]]
    Df = [node for node, _ in degrees[0:int(f*len(degrees))]]

    intersect = []
    for node in Rf:
        if node in Df:
            intersect.append(node)

    return len(intersect)/len((Rf))


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



plt.subplot(2, 2, 1)
plt.plot(f_values, RRCs)
plt.ylabel("rRC")
plt.xlabel("f")
plt.subplot(2, 2, 2)
plt.plot(f_values, RRds)
plt.ylabel("rRD")
plt.xlabel("f")
plt.subplot(2, 2, 3)
plt.plot(f_values, RTs)
plt.ylabel("rRT (Temporal Feature)")
plt.xlabel("f")
plt.subplot(2, 2, 4)
plt.plot(f_values, RRbs)
plt.ylabel("rRB (Betweennes")
plt.xlabel("f")
plt.show()
