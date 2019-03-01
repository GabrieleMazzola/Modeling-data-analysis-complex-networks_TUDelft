import json
import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
import json, codecs

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

# Point 9


def obtain_cumulative_infection(seed_node, dataset):
    infected_nodes = [seed_node]
    cumulative_function = []
    for index, interactions in enumerate(dataset):
        newly_infected = []

        for interaction in interactions:
            if interaction[0] in infected_nodes:
                newly_infected.append(interaction[1])
            if interaction[1] in infected_nodes:
                newly_infected.append(interaction[0])

        infected_nodes += list(set(newly_infected))
        infected_nodes = list(set(infected_nodes))

        cumulative_function.append(infected_nodes.copy())
    return cumulative_function


num_of_iter = 2
cumulative_functions = []
seed_nodes = []
for _ in range(num_of_iter):
    seed_node = random.choice(list(unique_nodes))
    cumulative = obtain_cumulative_infection(seed_node, edges_list)
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
#plt.show()




# Point 10
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
            timestep_infection_reached.append((node, index+1))
            break
    else:
        timestep_infection_reached.append((node, 99999999))
ranking = sorted(timestep_infection_reached, key=lambda x: x[1])
print(nodes_to_infect)
print(ranking[0:10])

with open('ranking.json', 'wb') as f:
    json.dump(ranking, codecs.getwriter('utf-8')(f), ensure_ascii=False)





