import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit, QCheckBox, QTextEdit, QGridLayout, QMenu, QScrollArea, QVBoxLayout, QTreeWidgetItem
from PyQt6.QtGui import QAction, QIcon, QFont
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6 import QtCore
from functions import init_database, write_json
from video_window_ui import Ui_Form
from functools import partial
import webbrowser


class VideoWindow(QWidget):
    trigger = pyqtSignal()

    def __init__(self, channel_list, channel_name, json_location):
        super().__init__()
        self.channel_list = channel_list
        self.channel_name = channel_name
        self.json_location = json_location
        self.initializeUI()

    def initializeUI(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("yt-notify")
        self.setWindowIcon(QIcon("images/icon.ico"))
        self.ui.label_title.setText(self.channel_name)

        #Connect contextmenu to treewidget
        self.ui.treeWidget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.treeWidget.customContextMenuRequested.connect(self.menuContextTree)

        for index, channel in enumerate(self.channel_list[self.channel_name]):
            video_id = channel['video_id']
            title = channel['title']
            item = QTreeWidgetItem(self.ui.treeWidget, [title])
            item.setToolTip(0, title)
            item.setText(2, video_id)

            if channel['seen'] == True:
                item.setCheckState(1, QtCore.Qt.CheckState.Checked)
            else:
                item.setCheckState(1, QtCore.Qt.CheckState.Unchecked)



        self.ui.treeWidget.setColumnWidth(0, 400)
        self.ui.treeWidget.setColumnHidden(2, True)
#        self.ui.treeWidget.resizeColumnToContents(0)
        self.resize(500, 729)

        self.ui.button_close.clicked.connect(self.close)
        self.ui.button_save.clicked.connect(self.save)

        self.ui.button_check.clicked.connect(self.checkAll)
        self.ui.button_uncheck.clicked.connect(self.uncheckAll)


    def checkAll(self):
        root = self.ui.treeWidget.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            item.setCheckState(1, QtCore.Qt.CheckState.Checked)

    def uncheckAll(self):
        root = self.ui.treeWidget.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            item.setCheckState(1, QtCore.Qt.CheckState.Unchecked)

    def save(self):
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
                    elif state.value == 0:
                        self.channel_list[self.channel_name][index]['seen'] = False
        write_json(self.channel_list, self.json_location)
        self.trigger.emit()

    #Make a contextmenu per item in treewidget
    def menuContextTree(self, point):
        # Infos about the node selected.
        index = self.ui.treeWidget.indexAt(point)

        if not index.isValid():
            return

        item = self.ui.treeWidget.itemAt(point)
        video_id = item.text(2)  # The text of the node.
        yt_link = "https://www.youtube.com/watch?v=" + video_id

        # We build the menu.
        menu = QMenu()
        self.play_mpv = QAction("&Play with mpv")
        self.play_mpv.triggered.connect(lambda e, yt_link=yt_link: os.system(f"mpv {yt_link}"))
        self.play_vlc = QAction("&Play with VLC")
        self.play_vlc.triggered.connect(lambda e, yt_link=yt_link: os.system(f'vlc "{yt_link}"'))
        self.open_browser = QAction("&Open in browser")
        self.open_browser.triggered.connect(lambda e, yt_link=yt_link: webbrowser.open_new_tab(yt_link))

        action = menu.addAction(self.play_mpv)
        action = menu.addAction(self.play_vlc)
        action = menu.addAction(self.open_browser)
#        menu.addSeparator()
#        action_1 = menu.addAction("Choix 1")
#        action_2 = menu.addAction("Choix 2")
#        action_3 = menu.addAction("Choix 3")

        menu.exec(self.ui.treeWidget.mapToGlobal(point))




if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = VideoWindow()
    main.show()
    sys.exit(app.exec_())
