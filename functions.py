import json
import os
import re

def init_database(json_location):
    """Initializes the data dir and the json file if not found, 
    then loads the json file"""
    dir = os.path.dirname(json_location)

    if not os.path.isdir(dir):
        os.makedirs(dir)

    try: 
        with open(json_location, 'r') as f:
            data = json.load(f)
            return data

    except FileNotFoundError:
        with open(json_location, 'w') as f:
            to_write = {'channels': []}
            json.dump(to_write, f)

        with open(json_location, 'r') as f:
            data = json.load(f)
            return data

def write_json(channel_list, json_location):
    """Writes everything from channel_list to json_location"""
    try:
        with open (json_location, 'w') as f:
            json.dump(channel_list, f, indent=2)
    except FileNotFoundError:
        print("json file not found")

def check_unseen(channel_name, channel_list):
    """Checks if channel has unseen videos"""
    count = 0
    for channel in channel_list[channel_name]:
        if channel['seen'] == False:
            count += 1
            continue
    return count

def url_check(url):
    """Check if url matches youtube url"""
    re_http = re.compile("^https?://www.youtube.com/c/.*$")
    re_http2 = re.compile("^https?://www.youtube.com/channel/.*$")
    if re.search(re_http, url):
        return True
    elif re.search(re_http2, url):
        return True
    else:
        return False
