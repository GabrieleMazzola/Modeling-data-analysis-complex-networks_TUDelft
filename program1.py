import json

import networkx as nx

with open('network.json') as f:
    edges_list = json.load(f)

print(f"Loading network with {len(edges_list)} timesteps")

# Build aggregated network
flat_list = [item for sublist in edges_list for item in sublist]
tmp = list(map(list, zip(*flat_list)))
unique_nodes = set(tmp[0] + tmp[1])

G = nx.Graph()
G.add_nodes_from(list(unique_nodes))
G.add_edges_from([tuple(item) for sublist in edges_list for item in sublist])

print(G.number_of_nodes())
print(G.number_of_edges())
