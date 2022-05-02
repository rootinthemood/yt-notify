import scrapetube
from PyQt6.QtCore import pyqtSignal, QThread
from time import sleep


class UpdateChannel(QThread):
    update_progress = pyqtSignal(int, str)
    worker_complete = pyqtSignal(list, dict)

    def __init__(self, channel_name, channel_list):
        super().__init__()
        self.channel_name = channel_name
        self.channel_list = channel_list

    def run(self):
        total_channels = len(self.channel_name)
        completed_list = []
        """Scrapes the last 'n' videos from a channel and compares them to
        the already saved videos and sends the completed list via an emit"""
        #Scrapes the last 'n' videos from a given channel and appends them to a temp list
        for channel in self.channel_list['channels']:
            if isinstance(self.channel_name, list):
                for index, name in enumerate(self.channel_name):
                    if name == channel['name']:
                        prog = round(((index + 1) / total_channels) * 100)
                        limit_count = 10
                        #Keeps scraping videos until the new videos found is less then limit count
                        while True:
                            temp_videos = []
                            videos = scrapetube.get_channel(channel_url=channel['url'], limit=limit_count)
                            for video in videos:
                                video_id = video['videoId']
                                title = video['title']['runs'][0]['text']
                                temp_videos.append({'video_id': video_id, 'title': title, 'seen': False})
                            #Compares the temp list with the main 'CHANNELS' list and removes duplicates from temp list
                            for old_video in self.channel_list[name]:
                                for video in temp_videos:
                                    if old_video['video_id'] == video['video_id']:
                                        temp_videos.remove(video)
                            print(limit_count)
                            if limit_count == 50:
                                limit_count = 9999999999999
                                continue
                            if len(temp_videos) == limit_count:
                                limit_count += 20
                                continue
                            self.update_progress.emit(prog, name)
                            break
                        #Prints found videos and inserts temp list(new videos) to main 'CHANNELS' dictionary
                        if len(temp_videos) <= 0:
                            found='no'
                            completed_list.append((found, name))
                        else:
                            count = 0
                            for video in reversed(temp_videos):
                                self.channel_list[name].insert(0, video)
                                count += 1
                                found='yes'
                            completed_list.append((found, name, count))
        self.worker_complete.emit(completed_list, self.channel_list)

def scrape_channel(channel_name, channel_list):
    """CHecks if channel has videos"""
    #Gets index from the given channel
    for name in channel_list['channels']:
        if name['name'] == channel_name:
            url = name['url']
            break

    channel_list[channel_name] = []
    videos = scrapetube.get_channel(channel_url=url, limit=1)
    for video in videos:
        video_id = video['videoId']

