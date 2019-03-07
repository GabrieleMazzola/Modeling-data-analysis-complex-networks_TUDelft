import json
import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
import json, codecs

from complex_net_assignment.util import obtain_cumulative_infection, load_network, build_graph_from_dataset

# Point 9
graph_dataset = load_network('./data/network.json')
G, unique_nodes = build_graph_from_dataset(graph_dataset)

cumulative_functions = []
seed_nodes = []
for seed_node in unique_nodes:
    print(seed_node)
    cumulative = obtain_cumulative_infection(seed_node, graph_dataset)
    cumulative_functions.append(cumulative)
    seed_nodes.append(seed_node)

aggregated = list(zip(*cumulative_functions))

avg_values = []
std_values = []
for infections in aggregated:
    infected = [len(infected) for infected in infections]
    avg_values.append(np.average(infected))
    std_values.append(np.std(infected))

plt.errorbar(np.array(list(range(len(avg_values)))),
             np.array(avg_values),
             np.array(std_values),
             ecolor="red",
             )
plt.xlabel("Timestep")
plt.ylabel("# Infected nodes")
plt.show()










