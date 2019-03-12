import json

import matplotlib.pyplot as plt
import networkx as nx

from util import load_network, load_infection_ranking, build_graph_from_dataset, compute_ranking

graph_dataset = load_network('./data/network.json')
infect_ranking = load_infection_ranking("./data/ranking.json")

graph, unique_nodes = build_graph_from_dataset(graph_dataset)

# Degree
degrees = graph.degree
degrees = sorted(degrees, key=lambda x: x[1], reverse=True)
# print(degrees)

# Clustering coefficient
clust_coef = list(nx.clustering(graph).items())
clust_coef = sorted(clust_coef, key=lambda x: x[1], reverse=True)


# print(clust_coef)

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


#
#
# nodes_to_infect = 0.8 * len(unique_nodes)
#
# timestep_infection_reached = []
# nodes_reached = []
#
# nodes = sorted(list(unique_nodes))
# average_infection_timesteps = []
#
#
# for node in nodes:
#
#     seed_node = node
#     cumulative = obtain_cumulative_infection(seed_node, graph_dataset)
#     infected_80perc = []
#
#     print(seed_node)
#
#     for index, infected in enumerate(cumulative):
#         if len(infected) >= nodes_to_infect:
#             infected_80perc = infected
#
#     infected_at_timestep = 0
#     for infected_node in infected_80perc:
#         for index, nodes_infected in enumerate(cumulative):
#             if infected_node in nodes_infected:
#                 infected_at_timestep += index
#                 break
#
#     average_infection_timesteps.append((node, (infected_at_timestep/len(infected_80perc)) if infected_80perc else 99999999))
#
# average_infection_timesteps = sorted(average_infection_timesteps, key=lambda x: x[1])
# print(average_infection_timesteps)
#
# with open('data/timestep_rankings.json', 'wb') as f:
#     json.dump(average_infection_timesteps, codecs.getwriter('utf-8')(f), ensure_ascii=False)
#

with open("./data/timestep_rankings.json") as f:
    average_infection_timesteps = json.load(f)

with open("./data/ranking.json") as f:
    ranking_initial = json.load(f)

f_values, RDs = compute_ranking(average_infection_timesteps, degrees)
f_values, RCs = compute_ranking(average_infection_timesteps, clust_coef)
f_values, Rr_prime = compute_ranking(average_infection_timesteps, ranking_initial)

plt.plot(f_values, RDs, label="rDs")
plt.plot(f_values, RCs, label="rCs")
plt.plot(f_values, Rr_prime, label="rRs")
plt.xlabel("f")
plt.legend(loc="upper left")
plt.show()
