import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit, QCheckBox, QTextEdit, QGridLayout, QMenu, QScrollArea, QVBoxLayout, QTreeWidgetItem
from PyQt6.QtGui import QAction, QIcon, QFont
from PyQt6.QtCore import Qt, QSize
from PyQt6 import QtCore
from functions import init_database, write_json
from video_window_ui import Ui_Form


class VideoWindow(QWidget):

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

        short_title = ""
        for index, channel in enumerate(self.channel_list[self.channel_name]):
            video_id = channel['video_id']
            title = channel['title']
            if len(title) > 57:
                short_title = title[0:52] + "..."
            elif len(title) <= 57:
                short_title = title[0:len(title)] +  (57 - len(title)) * " "
            else:
                short_title = title
            item = QTreeWidgetItem(self.ui.treeWidget, [short_title])
            item.setToolTip(0, title)
            item.setText(2, video_id)

            if channel['seen'] == True:
                item.setCheckState(1, QtCore.Qt.CheckState.Checked)
            else:
                item.setCheckState(1, QtCore.Qt.CheckState.Unchecked)


        self.ui.treeWidget.setColumnHidden(2, True)
        self.ui.treeWidget.resizeColumnToContents(0)
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
        print(self.channel_list[self.channel_name])



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = VideoWindow()
    main.show()
    sys.exit(app.exec_())
