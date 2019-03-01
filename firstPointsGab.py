import json
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

with open('network.json') as f:
    edges_list = json.load(f)

print(f"Loading network with {len(edges_list)} timesteps")


# Build aggregated network
flat_list = [item for sublist in edges_list for item in sublist]
tmp = list(map(list,zip(*flat_list)))
unique_nodes = set(tmp[0] + tmp[1])


G = nx.Graph()
G.add_nodes_from(list(unique_nodes))
G.add_edges_from([tuple(item) for sublist in edges_list for item in sublist])



# Point 1)
print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")

print(f"Density: {nx.density(G)}")
degrees = sorted([d for n, d in G.degree], reverse=True)  # degree sequence

print(f"Average Degree: { np.average(degrees)}")
print(f"Degree variance: {np.var(degrees)}")




# Point 2)
plt.hist(degrees, bins=30)
plt.show()

# Point 3)
print(f"Assortativity: {nx.degree_assortativity_coefficient(G)}")

# Point 4)
print(f"Average clustering coefficient: {nx.average_clustering(G)}")

# Point 5)
shortest_paths = list(nx.shortest_path_length(G))

unique_shortest_paths = []
for key, value in shortest_paths:
    value = dict(value)
    value.pop(key)

    for k, v in value.items():
        comb = tuple(sorted([key, k]) + [v])
        unique_shortest_paths.append(comb)

unique_shortest_paths = list(set(unique_shortest_paths))

avg_hopcount_s_paths = np.average([l[2] for l in unique_shortest_paths])
print(f"Average hopcount shortest paths: {avg_hopcount_s_paths}")

print(f"Diameter: {sorted(unique_shortest_paths, key=lambda x: x[2], reverse=True)[0]}")

# Point 6
nx.random_regular_graph()

# Point 7
A_sp = nx.adjacency_spectrum(G)
print(f"Spectral radius: {float(np.max(A_sp))}")

# Point 8
print(f"Algebraic connectivity: {nx.algebraic_connectivity(G)}")


print()