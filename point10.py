import codecs
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

# Point 10
from complex_net_assignment.util import obtain_cumulative_infection

nodes_to_infect = 0.8 * len(unique_nodes)

timestep_infection_reached = []

nodes = sorted(list(unique_nodes))
print(len(nodes))
for node in nodes:
    seed_node = node
    cumulative = obtain_cumulative_infection(seed_node, edges_list)
    print(seed_node)
    for index, infected in enumerate(cumulative):
        if len(infected) >= nodes_to_infect:
            timestep_infection_reached.append((node, index + 1))
            break
    else:
        timestep_infection_reached.append((node, 99999999))
ranking = sorted(timestep_infection_reached, key=lambda x: x[1])
print(nodes_to_infect)
print(ranking[0:10])

with open('ranking.json', 'wb') as f:
    json.dump(ranking, codecs.getwriter('utf-8')(f), ensure_ascii=False)
