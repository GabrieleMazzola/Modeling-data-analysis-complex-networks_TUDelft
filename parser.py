import pandas as pd
import json, codecs

filename_from = "./data/g3.csv"
filename_to = "./data/g3.json"

df = pd.read_csv(filename_from)

edges_list = []

for timestamp, sub_df in df.groupby("timestamp"):
    edges = list(zip(list(sub_df['node1']), list(sub_df['node2'])))
    edges_list.append(edges)

with open(filename_to, 'wb') as f:
    json.dump(edges_list, codecs.getwriter('utf-8')(f), ensure_ascii=False)
