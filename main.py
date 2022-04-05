import json
import os
import os
from functions import add_channel, return_id_title_seen, set_channel_seen, print_id_title_seen
from scrapevideos import scrape_channel, scrape_all_channels

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
        json.dump(CHANNELS, f, indent=2)


#add_channel("NileBlue", "https://www.youtube.com/c/NileRed2/", CHANNELS)
#add_channel("V for Valentine", "https://www.youtube.com/c/VforValentine/", CHANNELS)
#scrape_all_channels(CHANNELS)
        

#set_channel_seen("NileBlue", CHANNELS, False)
print_id_title_seen("NileBlue", CHANNELS)
#write_json()


#print(CHANNELS)
