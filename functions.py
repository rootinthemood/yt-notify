import json
import os
import re

#Initializes the json file if not found. Then loads the json file
def init_database(json_location):
    if not os.path.isfile(json_location):
        with open(json_location, 'w') as f:
            to_write = {'channels': []}
            json.dump(to_write, f)

    with open(json_location, 'r') as f:
        data = json.load(f)
        return data

#Writes everything from channel_list to json_location
def write_json(channel_list, json_location):
    with open (json_location, 'w') as f:
        json.dump(channel_list, f, indent=2)

#Get the length of the longest string from channels
def get_max_button_length(channel_list):
    chan_list = [channel['name'] for channel in channel_list['channels'] if not channel == "channels"]
    if len(chan_list) >= 1:
        max_string = max(chan_list, key=len)
        max_len = len(max_string)
        button_width = max_len
    else:
        button_width = 5
    return button_width

#Checks if channel has unseen videos
def check_unseen(channel_name, channel_list):
    for channel in channel_list[channel_name]:
        if channel['seen'] == False:
            return True
    return False

#Check if url matches youtube url
def url_check(url):
    re_http = re.compile("^https?://www.youtube.com/c/.*$")
    re_http2 = re.compile("^https?://www.youtube.com/channel/.*$")
    if re.search(re_http, url):
        return True
    elif re.search(re_http2, url):
        return True
    else:
        return False
