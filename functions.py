import json
import re
from prettytable import PrettyTable

def add_channel(channel_list):
    """Adds a channel and url to channel_list"""
    re_http = re.compile("^https?://www.youtube.com/c/.*/$")
    while True:
        name = input("Channel name: ")
        for channel in channel_list['channels']:
            if name == channel['name']:
                print(f"{name} already in database")
                return

        url = input("Channel url: ")
        for channel in channel_list['channels']:
            if url == channel['url']:
                print(f"url already in database")
                return
            if re.search(re_http, url) is None:
                print("URL is not the correct format")
                return
        break
    channel_list['channels'].append({'name': name, 'url': url})


def remove_channel(name, channel_list): 
    """Removes a channel in 'channels:' and all of it'v videos"""
    for index, channel in enumerate(channel_list['channels']):
        if name == channel['name']:
            if input(f"are you sure you want to delete, {name} and all it's video's? 'y/n'") == "y":
                channel_list['channels'].pop(index)
                channel_list.pop(name)
        else:
            print("Channel not found")


def return_id_title_seen(channel_name, channel_list):
    """Returns title ,videoid and seen for a given channel"""
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

