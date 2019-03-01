import json

with open('network.json') as f:
    data = json.load(f)

print(data[1])