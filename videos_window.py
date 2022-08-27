import sys
import os
import platform
from PyQt6.QtWidgets import QWidget, QTreeWidgetItem, QMenu
from PyQt6.QtGui import QAction, QIcon 
from PyQt6.QtCore import pyqtSignal
from PyQt6 import QtCore
from functions import write_json
from video_window_ui import Ui_Form
import webbrowser
import subprocess
from shutil import which


class VideoWindow(QWidget):
    close_trigger = pyqtSignal()

    def __init__(self, channel_list, channel_name, json_location, settings):
        super().__init__()
        self.channel_list = channel_list
        self.channel_name = channel_name
        self.json_location = json_location
        self.initialize_ui()
        self.platform = platform.system()
        self.mpv_args = settings[0]
        self.vlc_args = settings[1]


    def initialize_ui(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle(self.channel_name)
        self.setWindowIcon(QIcon("images/icon.ico"))
        self.ui.label_title.setText(self.channel_name)

        #Connect contextmenu to treewidget
        self.ui.treeWidget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.treeWidget.customContextMenuRequested.connect(self.menu_context_tree)

        for index, channel in enumerate(self.channel_list[self.channel_name]):
            video_id = channel['video_id']
            title = channel['title']
            item = QTreeWidgetItem(self.ui.treeWidget, [title])
            item.setToolTip(0, title)
            item.setText(2, video_id)
            if channel['seen'] == True:
                item.setCheckState(1, QtCore.Qt.CheckState.Checked)
            elif channel['seen'] == "Watching":
                item.setCheckState(1, QtCore.Qt.CheckState.PartiallyChecked)
            else:
                item.setCheckState(1, QtCore.Qt.CheckState.Unchecked)

        self.ui.treeWidget.setColumnWidth(0, 400)
        self.ui.treeWidget.setColumnHidden(2, True)
        self.resize(500, 729)

        self.ui.button_close.clicked.connect(self.close)
        self.ui.button_save.clicked.connect(self.save)

        self.ui.button_check.clicked.connect(self.check_all)
        self.ui.button_uncheck.clicked.connect(self.uncheck_all)

    def check_all(self):
        """checks all checkbuttons"""
        root = self.ui.treeWidget.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            item.setCheckState(1, QtCore.Qt.CheckState.Checked)

    def uncheck_all(self):
        """uncheck all checkbuttons"""
        root = self.ui.treeWidget.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            item.setCheckState(1, QtCore.Qt.CheckState.Unchecked)

    def save(self):
        """Saves the checkbutton state to json"""
        root = self.ui.treeWidget.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            title = item.text(0) # text at first (0) column
            video_id = item.text(2)
            state = item.checkState(1)
            for index, video in enumerate(self.channel_list[self.channel_name]):
                if video_id == video['video_id']:
                    if state.value == 2:
                        self.channel_list[self.channel_name][index]['seen'] = True
                    elif state.value == 1:
                        self.channel_list[self.channel_name][index]['seen'] = "Watching"
                    else: 
                        self.channel_list[self.channel_name][index]['seen'] = False
        write_json(self.channel_list, self.json_location)
        self.close_trigger.emit()

    def menu_context_tree(self, point):
        """Make a contextmenu per item in treewidget"""
        index = self.ui.treeWidget.indexAt(point)

        if not index.isValid():
            return

        item = self.ui.treeWidget.itemAt(point)
        video_id = item.text(2)  # The text of the node.
        yt_link = "https://www.youtube.com/watch?v=" + video_id

        #Make the menu
        menu = QMenu()
        self.open_browser = QAction("&Open in browser")
        self.open_browser.triggered.connect(lambda e, yt_link=yt_link: webbrowser.open_new_tab(yt_link)) and item.setCheckState(1, QtCore.Qt.CheckState.PartiallyChecked)
        action = menu.addAction(self.open_browser)

        if which('mpv'):
            mpv_args = which('mpv') + " " + self.mpv_args + " " + yt_link
            self.play_mpv = QAction("&Play with mpv")
            self.play_mpv.triggered.connect(lambda e, mpv_args=mpv_args: subprocess.Popen([mpv_args], shell=True) and item.setCheckState(1, QtCore.Qt.CheckState.PartiallyChecked))
            action = menu.addAction(self.play_mpv)

        if which('vlc'):
            vlc_args = which('vlc') + " " + self.vlc_args + " " + yt_link
            self.play_vlc = QAction("&Play with VLC")
            self.play_vlc.triggered.connect(lambda e, vlc_args=vlc_args: subprocess.Popen([vlc_args], shell=True) and item.setCheckState(1, QtCore.Qt.CheckState.PartiallyChecked))
            action = menu.addAction(self.play_vlc)

        menu.exec(self.ui.treeWidget.mapToGlobal(point))
