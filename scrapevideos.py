import scrapetube

def scrape_channel(channel_list):
    for channel in channel_list['channels']:
        print(channel['name'], channel['url'])

    answer = input("\nWhat channel url to scrape?: ")
    videos = scrapetube.get_channel(channel_url=answer)
    for video in videos:
        print(video['videoId'])

def scrape_all_channels(channel_list):
    """Scrapes all videos and titles for each channel and appends them in channel_list"""
    #Writes the channel names in channel_list with an empy list as value
    for channel in channel_list['channels']:
            channel_list[channel['name']] = []
    for channel in channel_list['channels']:
        videos = scrapetube.get_channel(channel_url=channel['url'])
        for video in videos:
            video_id = video['videoId']
            title = video['title']['runs'][0]['text']
            channel_list[channel['name']].append({'video_id': video_id, 'title': title, 'seen': ""})
