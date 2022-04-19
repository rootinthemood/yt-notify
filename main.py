#!/usr/bin/python
import os, sys, json, re, platform
from functions import write_json, init_database, get_max_button_length, check_unseen, url_check
from scrapevideos import scrape_channel, scrape_all_channels ,update_channel, update_all_channels
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit, QCheckBox, QTextEdit, QGridLayout, QMenu
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QFont
from videos_window import VideoWindow
from functools import partial

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
        self.quit_act = QAction("&Quit")
        self.quit_act.setShortcut("Ctrl+Q")
        self.quit_act.triggered.connect(self.close)

        self.update_channels = QAction("&Update all channels")
        self.update_channels.setShortcut("Ctrl+U")

        self.about = QAction("About")

    def createMenu(self):
        """Create the menu bar"""
        self.menuBar().setNativeMenuBar(False)

        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(self.quit_act)
        file_menu.addAction(self.update_channels)

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

            menu.addAction("Update Channel")
            menu.addSeparator()
            menu.addAction("Remove channel")

            self.main_grid.addWidget(self.chan_button, row_int, column_int)
            column_int += 1

    def openVideoWindow(self, name):
        self.new_video_window = VideoWindow(CHANNELS, name, CHANNEL_JSON)
        self.new_video_window.show()
            





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
