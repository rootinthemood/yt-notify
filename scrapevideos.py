import scrapetube

def scrape_channel(channel_name, channel_list):
    #Gets index from the given channel
    for name in channel_list['channels']:
        if name['name'] == channel_name:
            url = name['url']
            break

    channel_list[channel_name] = []
    videos = scrapetube.get_channel(channel_url=url)
    for video in videos:
        video_id = video['videoId']
        title = video['title']['runs'][0]['text']
        channel_list[channel_name].append({'video_id': video_id, 'title': title, 'seen': False})



def scrape_all_channels(channel_list):
    for channel in channel_list['channels']:
        channel_name = channel['name']
        scrape_channel(channel_name, channel_list)
#        scrape_channel(channel, channel_list)
#    """Scrapes all videos and titles for each channel and appends them in channel_list"""
#    #Writes the channel names in channel_list with an empy list as value
#    for channel in channel_list['channels']:
#            channel_list[channel['name']] = []
#    for channel in channel_list['channels']:
#        videos = scrapetube.get_channel(channel_url=channel['url'])
#        for video in videos:
#            video_id = video['videoId']
#            title = video['title']['runs'][0]['text']
#            channel_list[channel['name']].append({'video_id': video_id, 'title': title, 'seen': ""})


def update_channel(channel_name, channel_list):
    """Scrapes the last 'n' videos from a channel and compares them to the already saved videos and then updates the main video dictionary"""
    #Scrapes the last 'n' videos from a given channel and appends them to a temp list
    temp_videos = []
    for channel in channel_list['channels']:
        if channel_name == channel['name']:
            videos = scrapetube.get_channel(channel_url=channel['url'], limit=10)
            for video in videos:
                video_id = video['videoId']
                title = video['title']['runs'][0]['text']
                temp_videos.append({'video_id': video_id, 'title': title, 'seen': False})
    #Compares the temp list with the main 'CHANNELS' list and removes duplicates from temp list
    for old_video in channel_list[channel_name]:
        for video in temp_videos:
            if old_video['video_id'] == video['video_id']:
                temp_videos.remove(video)
    #Prints found videos and inserts temp list(new videos) to main 'CHANNELS' dictionary
    if len(temp_videos) <= 0:
        return f"{channel_name}\t - No new videos found"
#        print(f"{channel_name}\t - No new videos found")
#        return
    else:
        count = 0
        for video in temp_videos:
            channel_list[channel_name].insert(0, video)
            count += 1
    return f"{channel_name}\t - {count} new video(s) found."
#    print(f"{channel_name}\t - {count} new video(s) found.")


def update_all_channels(channel_list):
    for channel in channel_list:
        if channel == "channels":
            continue
        update_channel(channel, channel_list)
