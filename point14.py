import random
from random import shuffle

import pandas as pd

from util import load_network, build_graph_from_dataset


def createG2_csv():
    df = pd.read_excel("..\manufacturing_emails_temporal_network.xlsx")

    timestamps = df.timestamp
    unique_timesteps = timestamps.unique()
    unique_timesteps_shuffled = unique_timesteps.copy()
    shuffle(unique_timesteps_shuffled)

    mapping = {}
    for index, base in enumerate(unique_timesteps):
        target = unique_timesteps_shuffled[index]
        mapping[base] = target

    def convert_to_target(base):
        return mapping[base]

    df['timestamp'] = df.timestamp.apply(convert_to_target)
    df.sort_values('timestamp', inplace=True)
    return df


def createG3_csv():
    g_data = load_network('./data/network.json')
    g_graph, g_unique_nodes = build_graph_from_dataset(g_data)

    g_edges = list(g_graph.edges)

    new_connections = []
    timestamps = pd.read_excel("..\manufacturing_emails_temporal_network.xlsx")['timestamp'].tolist()
    for timestamp in timestamps:
        selected_edge = random.choice(g_edges)
        new_connections.append([selected_edge[0], selected_edge[1], timestamp])

    df = pd.DataFrame(new_connections)
    df.columns = ['node1', 'node2', 'timestamp']
    return df

# g2 = createG2_csv()
# g2.to_csv("./data/g2.csv", index=False)
# g2_data = load_network('./data/g2.json')
# g2_graph, g2_unique_nodes = build_graph_from_dataset(graph_dataset)


# g3 = createG3_csv()
# g3.to_csv("./data/g3.csv", index=False)
# g3_data = load_network('./data/g3.json')
# g3_graph, g3_unique_nodes = build_graph_from_dataset(graph_dataset)
