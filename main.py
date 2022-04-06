import json
import os
from functions import add_channel, return_id_title_seen, set_channel_seen, print_id_title_seen, remove_channel
from scrapevideos import scrape_channel, scrape_all_channels ,update_channel, update_all_channels

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


#add_channel(CHANNELS)
#scrape_all_channels(CHANNELS)
#remove_channel("V for Valentine", CHANNELS)        
#print(CHANNELS)
#update_all_channels(CHANNELS)
#for channel in CHANNELS:
#    if channel == "channels":
#        continue
#    update_channel(channel, CHANNELS)
#update_channel("NileBlue", CHANNELS)
#print(CHANNELS['NileBlue'])
#print(len(CHANNELS['NileBlue']))
#print(CHANNELS['NileBlue'][0])

#scrape_all_channels(CHANNELS)
scrape_channel("V for Valentine", CHANNELS)
print(CHANNELS)
#print(CHANNELS['V for Valentine'])
#set_channel_seen("NileBlue", CHANNELS, True)
#print_id_title_seen("NileBlue", CHANNELS)
#write_json()


#print(CHANNELS)
