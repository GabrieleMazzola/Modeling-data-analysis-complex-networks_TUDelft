import json

import networkx as nx
import numpy as np

with open('./data/network.json') as f:
    edges_list = json.load(f)

print(f"Loading network with {len(edges_list)} timesteps")

# Build aggregated network
flat_list = [item for sublist in edges_list for item in sublist]
tmp = list(map(list, zip(*flat_list)))
unique_nodes = set(tmp[0] + tmp[1])

G = nx.Graph()
G.add_nodes_from(list(unique_nodes))
G.add_edges_from([tuple(item) for sublist in edges_list for item in sublist])

density = nx.density(G)

# Create Null Model: Erdos-Renyi graph
ensemble_null_models = []
for i in range(0, 10):
    ensemble_null_models.append(nx.erdos_renyi_graph(167, density))

# Compute the average of the mean shortest path length
average_shortest_paths = []
for graph in ensemble_null_models:
    average_shortest_paths.append(nx.average_shortest_path_length(graph))

avg_mean_shortest_path_ensemble = np.mean(average_shortest_paths)

# Compute the mean clustering coefficient
clust_coefs = []
for graph in ensemble_null_models:
    clust_coefs.append(nx.average_clustering(graph))

avg_clust_coef_ensemble = np.mean(clust_coefs)

# Calculate mean shortest path and clustering coefficient of out network
mean_shortest_path = nx.average_shortest_path_length(G)
clust_coef = nx.average_clustering(G)

# Calculate normalised shortest path and clustering coefficient
norm_shortest_path = mean_shortest_path / avg_mean_shortest_path_ensemble
norm_clust_coef = clust_coef / avg_clust_coef_ensemble

print(f"Normalized shortest path: {norm_shortest_path}")
print(f"Normalized clustering coefficient: {norm_clust_coef}")
