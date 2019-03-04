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

plt.plot(f_values, RTs)
plt.ylabel("Temporal Feature")
plt.xlabel("f")
plt.show()

