import json
from prettytable import PrettyTable

def add_channel(name, url, location):
    """Adds a channel and url to location"""
#    name = input("Channel name: ")
#    url = input("Channel url: ")
    location['channels'].append({'name': name, 'url': url})
    return True 

def return_id_title_seen(channel_name, channel_list):
    """Returns title and videoid for a given channel"""
    video_id_list = []
    title_list = []
    seen_list = []
    for id in range(len(channel_list[channel_name])):
        video_id = channel_list[channel_name][id]['video_id']
        title = channel_list[channel_name][id]['title']
        seen = channel_list[channel_name][id]['seen']
        video_id_list.append(video_id)
        title_list.append(title)
        seen_list.append(seen)

    return(video_id_list, title_list, seen_list)

def print_id_title_seen(channel_name, channel_list):
    id_title = return_id_title_seen(channel_name, channel_list)

    pt = PrettyTable()
    pt.add_column("VideoId", id_title[0])
    pt.add_column("Title", id_title[1])
    pt.add_column("Seen", id_title[2])
    pt.align = "l"
    print(pt)


def set_channel_seen(channel_name, channel_list, boolean):
    """Sets the boolean True or False for all videos for the given channel"""
    for channel in channel_list[channel_name]:
        channel.update({"seen": boolean})

