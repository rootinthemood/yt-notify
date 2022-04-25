import scrapetube
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit, QCheckBox, QTextEdit, QGridLayout, QMenu, QMessageBox, QSystemTrayIcon
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from time import sleep

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

class UpdateChannel(QWidget):
    trigger_update = pyqtSignal(str)

    def __init__(self, channel_name, channel_list):
        super().__init__()
        self.channel_name = channel_name
        self.channel_list = channel_list

    def update_channel(self):
        
        """Scrapes the last 'n' videos from a channel and compares them to
        the already saved videos and then updates the main video dictionary"""
        #Scrapes the last 'n' videos from a given channel and appends them to a temp list
        for channel in self.channel_list['channels']:
            if isinstance(self.channel_name, list):
                for name in self.channel_name:
                    if name == channel['name']:
                        self.trigger_update.emit(name)
                        sleep(1)
            if self.channel_name == channel['name']:
                name = channel['name']
                self.trigger_update.emit(name)

#                limit_count = 10
#                #Keeps scraping videos until the new videos found is less then limit count
#                while True:
#                    temp_videos = []
##                    print(limit_count)
#                    videos = scrapetube.get_channel(channel_url=channel['url'], limit=limit_count)
#                    for video in videos:
#                        video_id = video['videoId']
#                        title = video['title']['runs'][0]['text']
#                        temp_videos.append({'video_id': video_id, 'title': title, 'seen': False})
#                    #Compares the temp list with the main 'CHANNELS' list and removes duplicates from temp list
#                    for old_video in channel_list[channel_name]:
#                        for video in temp_videos:
#                            if old_video['video_id'] == video['video_id']:
#                                temp_videos.remove(video)
#                    if len(temp_videos) == limit_count:
#                        limit_count += 20
#                        continue
#                    break
#                #Prints found videos and inserts temp list(new videos) to main 'CHANNELS' dictionary
#                if len(temp_videos) <= 0:
#                    found='no'
#                    return found, channel_name
#                else:
#                    count = 0
#                    for video in reversed(temp_videos):
#                        channel_list[channel_name].insert(0, video)
#                        count += 1
#                        found='yes'
#                return found, channel_name, count

#    def update_all_channels(self, channel_list):
#        updates = []
#        for channel in channel_list:
#            print(channel)
#            if channel == "channels":
#                continue
#            update = self.update_channel(channel, self.channel_list)
#            updates.append(update)
#        return updates

#    def update_all_channels(self, channel_list):
#        updates = []
#        new_channels = [channel for channel in channel_list if channel != "channels"]
#        update1 = UpdateChannel(channel, channel_list)
#        update = update1.update_channel()
#        print(channel)
#        updates.append(update)
#    return updates
