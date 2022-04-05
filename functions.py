import json

def add_channel(name, url, location):
    """name, url, list location"""
#    name = input("Channel name: ")
#    url = input("Channel url: ")
    location['channels'].append({'name': name, 'url': url})
    return True 
