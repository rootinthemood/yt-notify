#!/usr/bin/python
import os, sys, json, re, platform
from functions import write_json, init_database, get_max_button_length, check_unseen, url_check
from scrapevideos import scrape_channel, scrape_all_channels ,update_channel, update_all_channels
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit, QCheckBox, QTextEdit, QGridLayout, QMenu, QMessageBox
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QFont
from videos_window import VideoWindow
from functools import partial
from add_channel_window import addChannelWindow

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
        self.show()

    def createActions(self):
        """Create the application menu actions."""
        self.update_channels = QAction("&Update all channels")
        self.update_channels.setShortcut("Ctrl+U")

        self.add_channel_button = QAction("&Add channel")
        self.add_channel_button.setShortcut("Ctrl+A")
        self.add_channel_button.triggered.connect(self.add_channel)

        self.quit_act = QAction("&Quit")
        self.quit_act.setShortcut("Ctrl+Q")
        self.quit_act.triggered.connect(self.close)


        self.about = QAction("About")

    def createMenu(self):
        """Create the menu bar"""
        self.menuBar().setNativeMenuBar(False)

        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(self.update_channels)
        file_menu.addAction(self.add_channel_button)
        file_menu.addAction(self.quit_act)

        file_menu2 = self.menuBar().addMenu("Help")
        file_menu2.addAction(self.about)

    def setUpMainWindow(self):
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


            menu = QMenu()
            self.chan_button.setMenu(menu)
            video_menu = menu.addAction("Videos")
            open_channel = partial(self.openVideoWindow, name)
            video_menu.triggered.connect(open_channel)

            menu.addSeparator()
            menu.addAction("Update Channel")

            remove_channel_menu = menu.addAction("Remove Channel")
            delete_channel = partial(self.remove_channel, name)
            remove_channel_menu.triggered.connect(delete_channel)


            self.main_grid.addWidget(self.chan_button, row_int, column_int)
            column_int += 1

        if self.main_grid.count() == 0:
            self.header = QLabel("Add channels to list them here", self)
            self.header.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.main_grid.addWidget(self.header, 0, 0)

    def openVideoWindow(self, name):
        self.new_video_window = VideoWindow(CHANNELS, name, CHANNEL_JSON)
        self.new_video_window.show()

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
                    write_json(CHANNELS, CHANNEL_JSON)
                    init_database(CHANNEL_JSON)
                    self.setUpMainWindow()

    def add_channel(self):
        value = self.add_channel_window = addChannelWindow(CHANNELS, CHANNEL_JSON)
        value.show()
        if value:
            self.setUpMainWindow()
        






if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
