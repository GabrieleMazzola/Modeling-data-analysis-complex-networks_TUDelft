import pickle

import matplotlib.pyplot as plt
import numpy as np

from util import load_network, build_graph_from_dataset, cumulative_infection_network

G_dataset = load_network('./data/network.json')
G, G_unique_nodes = build_graph_from_dataset(G_dataset)

G2_dataset = load_network('./data/g2.json')
G2, G2_unique_nodes = build_graph_from_dataset(G2_dataset)

G3_dataset = load_network('./data/g3.json')
G3, G3_unique_nodes = build_graph_from_dataset(G3_dataset)

print(len(G_dataset), len(G2_dataset), len(G3_dataset))

COMPUTE = False
PLOT = True

if COMPUTE:
    simulations = {}
    simulations['G'] = cumulative_infection_network(G_unique_nodes, G_dataset)
    simulations['G2'] = cumulative_infection_network(G2_unique_nodes, G2_dataset)
    simulations['G3'] = cumulative_infection_network(G3_unique_nodes, G3_dataset)

    with open('./data/point15simulations.p', 'wb') as fp:
        pickle.dump(simulations, fp, protocol=pickle.HIGHEST_PROTOCOL)
else:
    with open("./data/point15simulations.p", 'rb') as fin:
        simulations = pickle.load(fin)

values = [simulations['G'], simulations['G2'], simulations['G3']]
nodes = [G_unique_nodes, G2_unique_nodes, G3_unique_nodes]
for index, (avg, std) in enumerate(values):
    unique_nodes = nodes[index]
    perc_infected_80 = 0.8 * len(unique_nodes)
    avg_num_of_node_above_thres = [x for x in avg if x >= perc_infected_80][0]
    infection_timestep = avg.index(avg_num_of_node_above_thres)
    plt.errorbar(np.array(list(range(len(avg)))),
                 np.array(avg),
                 np.array(std),
                 ecolor="red")
    plt.xlabel("Timestep")
    plt.ylabel("# Infected nodes")
    plt.axvline(x=infection_timestep, color="green")
    plt.title("G" + str(index + 1))
    print(f"Infection occurred at timestep {infection_timestep}")

    if PLOT:
        plt.show()
