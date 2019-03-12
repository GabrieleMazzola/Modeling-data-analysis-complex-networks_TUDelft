import json

import networkx as nx
import numpy as np


def load_network(filepath):
    with open(filepath) as f:
        edges_list = json.load(f)
    return edges_list


def load_infection_ranking(filepath):
    with open(filepath) as f:
        ranking = json.load(f)
    return ranking


def build_graph_from_dataset(dataset):
    flat_list = [item for sublist in dataset for item in sublist]
    tmp = list(map(list, zip(*flat_list)))
    unique_nodes = set(tmp[0] + tmp[1])

    g = nx.Graph()
    g.add_nodes_from(list(unique_nodes))
    g.add_edges_from([tuple(item) for sublist in dataset for item in sublist])
    return g, unique_nodes


def compute_ranking(target_ranking, est_ranking):
    result = []
    f_values = np.linspace(0.05, 0.5, 10)

    for f in f_values:
        target = [node for node, _ in target_ranking[0:int(f * len(target_ranking))]]
        est = [node for node, _ in est_ranking[0:int(f * len(est_ranking))]]

        intersect = []
        for node in target:
            if node in est:
                intersect.append(node)

        result.append(len(intersect) / len(target))

    return f_values, result


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


def cumulative_infection_network(unique_nodes, graph_dataset):
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
    return avg_values, std_values
