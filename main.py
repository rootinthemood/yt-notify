import json
import os
from functions import add_channel

CHANNELS = dict()
CHANNEL_JSON = "test.json"

if not os.path.isfile(CHANNEL_JSON):
    with open(CHANNEL_JSON, 'w') as f:
        to_write = {'channels': []}
        json.dump(to_write, f)

with open(CHANNEL_JSON, 'r') as f:
    CHANNELS = json.load(f)

def write_json():
    with open (CHANNEL_JSON, 'w') as f:
        json.dump(CHANNELS, f)


add_channel("NileBlue", "http://youtube.com", CHANNELS)
add_channel("V for Valentine", "http://youtube.com", CHANNELS)

write_json()


print(CHANNELS)








