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
        with open(json_location, "r") as f:
            data = json.load(f)
            return data

    except FileNotFoundError:
        with open(json_location, "w") as f:
            to_write = {"channels": []}
            json.dump(to_write, f)

        with open(json_location, "r") as f:
            data = json.load(f)
            return data


def init_settings(settings_location):
    mpv_args, vlc_args, darkmode_args = None, None, None
    try:
        with open(settings_location, "r") as f:
            for line in f:
                if line.startswith("[mpv]"):
                    mpv_args = f.readline().rstrip("\n")
                if line.startswith("[vlc]"):
                    vlc_args = f.readline().rstrip("\n")
                if line.startswith("[darkmode]"):
                    darkmode_args = f.readline().rstrip("\n")

        return mpv_args, vlc_args, darkmode_args

    except FileNotFoundError:
        try:
            with open(settings_location, "w") as f:
                data = "[mpv]\n\n[vlc]\n\n[darkmode]\nauto\n"
                f.write(data)

            with open(settings_location, "r") as f:
                for line in f:
                    if line.startswith("[mpv]"):
                        mpv_args = f.readline().rstrip("\n")
                    if line.startswith("[vlc]"):
                        vlc_args = f.readline().rstrip("\n")
                    if line.startswith("[darkmode]"):
                        darkmode_args = f.readline().rstrip("\n")

            return mpv_args, vlc_args, darkmode_args

        except FileNotFoundError:
            print("Error")


def save_settings(mpv_args, vlc_args, darkmode_args, settings_location):
    data = []
    try:
        with open(settings_location, "r") as f:
            data = f.readlines()
            for index, line in enumerate(data):
                if line.startswith("[mpv]"):
                    data[index + 1] = mpv_args + "\n"
                if line.startswith("[vlc]"):
                    data[index + 1] = vlc_args + "\n"
                if line.startswith("[darkmode]"):
                    data[index + 1] = darkmode_args + "\n"

    except FileNotFoundError:
        print("File not found")

    try:
        with open(settings_location, "w") as f:
            f.writelines(data)
    except FileNotFoundError:
        print("Error")


def write_json(channel_list, json_location):
    """Writes everything from channel_list to json_location"""
    try:
        with open(json_location, "w") as f:
            json.dump(channel_list, f, indent=2)
    except FileNotFoundError:
        print("json file not found")

def check_total(channel_name, channel_list):
    """Counts total videos"""
    count = 0
    for _ in channel_list[channel_name]:
        count += 1
    return count

def check_unseen(channel_name, channel_list):
    """Checks if channel has unseen videos"""
    count = 0
    for channel in channel_list[channel_name]:
        if not channel["seen"]:
            count += 1
            continue
    return count

def check_seen(channel_name, channel_list):
    """Checks if channel has seen videos"""
    count = 0
    for channel in channel_list[channel_name]:
        if channel["seen"]:
            count += 1
            continue
    return count

def check_watching(channel_name, channel_list):
    """Checks if channel has currently watching videos"""
    count = 0
    for channel in channel_list[channel_name]:
        if channel["seen"] == "Watching":
            count += 1
            continue
    return count


def url_check(url):
    """Check if url matches youtube url"""
    re_http = re.compile("^https?://www.youtube.com/c/.*$")
    re_http2 = re.compile("^https?://www.youtube.com/channel/.*$")
    re_http3 = re.compile("^https?://www.youtube.com/user/.*$")
    re_http4 = re.compile("^https?://www.youtube.com/@.*$")
    if re.search(re_http, url):
        return True
    elif re.search(re_http2, url):
        return True
    elif re.search(re_http3, url):
        return True
    elif re.search(re_http4, url):
        return True
    else:
        return False
