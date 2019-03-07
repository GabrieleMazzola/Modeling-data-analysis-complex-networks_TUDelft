from complex_net_assignment.util import load_network, build_graph_from_dataset, cumulative_infection_network
import matplotlib.pyplot as plt
import numpy as np
import pickle

G_dataset = load_network('./data/network.json')
G, G_unique_nodes = build_graph_from_dataset(G_dataset)

G2_dataset = load_network('./data/g2.json')
G2, G2_unique_nodes = build_graph_from_dataset(G2_dataset)

G3_dataset = load_network('./data/g3.json')
G3, G3_unique_nodes = build_graph_from_dataset(G3_dataset)

print(len(G_dataset), len(G2_dataset), len(G3_dataset))

COMPUTE = False

if COMPUTE:
    simulations = {}
    simulations['G'] = cumulative_infection_network(G_unique_nodes, G_dataset)
    simulations['G2'] = cumulative_infection_network(G2_unique_nodes, G2_dataset)
    simulations['G3'] = cumulative_infection_network(G3_unique_nodes, G3_dataset)

    with open('./data/point15simulations.p', 'wb') as fp:
        pickle.dump(simulations, fp, protocol=pickle.HIGHEST_PROTOCOL)


with open("./data/point15simulations.p", 'rb') as fin:
    simulations = pickle.load(fin)

values = [simulations['G'], simulations['G2'], simulations['G3']]

for index, (avg, std) in enumerate(values):
    plt.errorbar(np.array(list(range(len(avg)))),
             np.array(avg),
             np.array(std),
             ecolor="red",
             )
    plt.xlabel("Timestep")
    plt.ylabel("# Infected nodes")
    plt.title("G" + str(index))
    plt.show()



