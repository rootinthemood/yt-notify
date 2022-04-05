import os
import json

def init_channels(channel_list, channel_json):
    if not os.path.isfile(channel_json):
        with open(channel_json, 'w') as f:
            to_write = {'channels': []}
            json.dump(to_write, f)

    with open(channel_json, 'r') as f:
        channel_list = json.load(f)
