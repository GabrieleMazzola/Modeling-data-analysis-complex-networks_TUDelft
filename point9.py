import matplotlib.pyplot as plt
import numpy as np

from complex_net_assignment.util import load_network, build_graph_from_dataset, \
    cumulative_infection_network

# Point 9
graph_dataset = load_network('./data/network.json')
G, unique_nodes = build_graph_from_dataset(graph_dataset)

avg_values, std_values = cumulative_infection_network(unique_nodes, graph_dataset)

plt.errorbar(np.array(list(range(len(avg_values)))),
             np.array(avg_values),
             np.array(std_values),
             ecolor="red",
             )
plt.xlabel("Timestep")
plt.ylabel("# Infected nodes")
plt.show()
