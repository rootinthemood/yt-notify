#!/usr/bin/python
import os, sys, json, re, platform
from functions import write_json, init_database, get_max_button_length, check_unseen, url_check
from scrapevideos import scrape_channel, scrape_all_channels, UpdateChannel
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit, QCheckBox, QTextEdit, QGridLayout, QMenu, QMessageBox, QSystemTrayIcon, QStatusBar, QProgressBar
from PyQt6.QtCore import Qt, QSize, QThread
from PyQt6.QtGui import QAction, QIcon, QFont
from videos_window import VideoWindow
from functools import partial
from add_channel_window import addChannelWindow
from systray import SystemTrayIcon
from pynotifier import Notification

PLATFORM = platform.system()
CHANNEL_JSON = "./data/data.json"
CHANNELS = init_database(CHANNEL_JSON)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setMinimumSize(300, 172)
        self.setWindowTitle("yt-notify")
        self.setWindowIcon(QIcon("images/icon.ico"))


        self.setUpMainWindow()
        self.createActions()
        self.createMenu()
#        self.notify_platform()



        self.show()

#    def update_channel(self, names):
#        #Testing signals/trigger for updateting channels in statusbar
#        if names == "":
#            names = [name for name in CHANNELS if name != "channels"]
#        self.updateChannel = UpdateChannel(names, CHANNELS)
#        self.updateChannel.trigger_update.connect(self.update_event)
#        self.updateChannel.update_channel()

    def update_all_systray(self):
        self.update_all_clicked("")


    #Runs when Update All Channels is clicked
    def update_all_clicked(self, names):
        self.progressBar.setHidden(False)
        self.progressBar.setValue(0)
        if names == "":
            names = [name for name in CHANNELS if name != "channels"]
        self.worker = UpdateChannel(names, CHANNELS)
        self.worker.start()
        self.worker.finished.connect(self.update_all_clicked_finished)
        self.worker.update_progress.connect(self.update_all_clicked_progress)
        self.worker.worker_complete.connect(self.notify_on_complete)

    #Gets a list of tuples with the amount of new videos and a dict with the total videos(CHANNELS) 
    #from scrapevideos.py->UpdateChannel class. Writes the dict to database
    #and sends a notification to the user with new videos found. 
    def notify_on_complete(self, lst, dct):
        write_json(dct, CHANNEL_JSON)
        self.setUpMainWindow()
        total_channels = len(lst)
        count = 0
        text = ""
        for channel in lst:
            if channel[0] == 'no':
                count += 1
                if count == total_channels:
                    self.notify_platform("No new videos")
#                    QMessageBox.information(self, "Done!", "No new videos")
                    return
                continue
            text += f"{channel[1]} - {channel[2]} new video(s)\n" 
            continue
        self.notify_platform(text)
#        QMessageBox.information(self, "Done!", text)


    #Function that runs when progress is updated via update_all_clicked
    def update_all_clicked_progress(self, val):
        self.progressBar.setValue(val)

    #Function that runs when progress is finished via update_all_clicked
    def update_all_clicked_finished(self):
        self.progressBar.setHidden(True)
        self.progressBar.setValue(0)
        print("finished")

#    def update_event(self, name):
#        self.setStatusTip(f"Updating: {name}")
#        print(f"Updating: {name}")

    def createActions(self):
        """Create the application menu actions."""
        self.add_channel_button = QAction("&Add channel")
        self.add_channel_button.setShortcut("Ctrl+A")
        self.add_channel_button.setStatusTip("Add a youtube channel to follow")
        self.add_channel_button.triggered.connect(self.add_channel)

        self.update_channels = QAction("&Update all channels")
#        self.update_channels.setStatusTip("Updates al channels one by one")
        self.update_channels.setShortcut("Ctrl+U")
        update = partial(self.update_all_clicked, "")
#        update = partial(UpdateChannel.update_channel, channel_list=CHANNELS)
        self.update_channels.triggered.connect(update)
#        self.update_channels.triggered.connect(update)


        self.quit_act = QAction("&Quit")
        self.quit_act.setShortcut("Ctrl+Q")
        self.quit_act.triggered.connect(sys.exit)


        self.about = QAction("About")

    def createMenu(self):
        """Create the menu bar"""
        self.menuBar().setNativeMenuBar(False)

        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(self.add_channel_button)
        file_menu.addAction(self.update_channels)
        file_menu.addAction(self.quit_act)

        file_menu2 = self.menuBar().addMenu("Help")
        file_menu2.addAction(self.about)

    def setUpMainWindow(self):
        #Make statusbar
        self.setStatusBar(QStatusBar())

        self.progressBar = QProgressBar()
        self.statusBar().addPermanentWidget(self.progressBar)
        self.progressBar.setMaximumSize(200, 20)
        self.progressBar.setHidden(True)
        self.progressBar.setValue(0)


        column_int = 0
        row_int = 0
        self.main_grid = QGridLayout()

        #Set the central widget(needed because of QMainWindow)
        container = QWidget()
        container.setLayout(self.main_grid)
        self.setCentralWidget(container)


        for channel in CHANNELS['channels']:
            if channel == "channels":
                continue
            if column_int == 3:
                row_int += 1
                column_int = 0
            name = channel['name']

            self.chan_button = QPushButton(name, self)
            
            #sets text color for buttons
            unseen_vids = check_unseen(name, CHANNELS)
            if unseen_vids > 0:
                self.chan_button.setStyleSheet('color: red')
                self.chan_button.setStatusTip(f"Unwatched videos: {unseen_vids}")
            else:
                self.chan_button.setStyleSheet('color: green')
                self.chan_button.setStatusTip(f"Unwatched videos: {unseen_vids}")


            menu = QMenu()
            self.chan_button.setMenu(menu)
            video_menu = menu.addAction("Videos")
            open_channel = partial(self.openVideoWindow, name)
            video_menu.triggered.connect(open_channel)

            menu.addSeparator()
            update_menu = menu.addAction("Update Channel")
            update_channel = partial(self.update_all_clicked, name)
            update_menu.triggered.connect(update_channel)

            remove_channel_menu = menu.addAction("Remove Channel")
            delete_channel = partial(self.remove_channel, name)
            remove_channel_menu.triggered.connect(delete_channel)


            self.main_grid.addWidget(self.chan_button, row_int, column_int)
            column_int += 1


        if self.main_grid.count() == 0:
            self.header = QLabel("Add channels to list them here", self)
            self.main_grid.addWidget(self.header, 0, 0)

        self.main_grid.setAlignment(Qt.AlignmentFlag.AlignTop)

    def openVideoWindow(self, name):
        self.new_video_window = VideoWindow(CHANNELS, name, CHANNEL_JSON)
        self.new_video_window.show()
        self.new_video_window.trigger.connect(self.handle_trigger)

    def remove_channel(self, name):
        for index, channel in enumerate(CHANNELS['channels']):
            if name == channel['name']:
                answer = QMessageBox.question(self,
                                              "Remove Channel?",
                                              f"Are you sure you want to remove {name}?",
                                              QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes)
                if answer == QMessageBox.StandardButton.Yes:
                    CHANNELS['channels'].pop(index)
                    CHANNELS.pop(name)
                    write_json(CHANNELS, CHANNEL_JSON)()
                    init_database(CHANNEL_JSON)
                    self.setUpMainWindow()

    def add_channel(self):
        self.add_channel_window = addChannelWindow(CHANNELS, CHANNEL_JSON)
        self.add_channel_window.show()
        #connect the trigger to the signal of addChannelWindow
        self.add_channel_window.trigger.connect(self.handle_trigger)

    def handle_trigger(self):
        self.setUpMainWindow()

    def notify_platform(self, text):
        icon = "images/icon.ico"
        if PLATFORM == "Linux":
            icon = "images/icon.png"
        Notification(title="Title",
                     description=text,
                     icon_path=icon,
                     duration=5,
                     urgency="normal").send()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = MainWindow()

    systray = SystemTrayIcon(QIcon("images/icon.ico"), window)
    sys_update_all = partial(window.update_all_clicked, "")
    systray.update_signal.connect(sys_update_all)
    systray.show()

    sys.exit(app.exec())
