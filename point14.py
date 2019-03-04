from random import shuffle

import pandas as pd


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


new_shuffled_dataframe = createG2_csv()
new_shuffled_dataframe.to_csv("./data/g2.csv", index=False)
