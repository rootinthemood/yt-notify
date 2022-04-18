import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit, QCheckBox, QTextEdit, QGridLayout, QMenu, QScrollArea, QVBoxLayout, QTreeWidgetItem
from PyQt6.QtGui import QAction, QIcon, QFont
from PyQt6.QtCore import Qt, QSize
from PyQt6 import QtCore
from functions import init_database
from video_window_ui import Ui_Form


class VideoWindow(QWidget):

    def __init__(self, channel_list, channel_name):
        super().__init__()
        self.channel_list = channel_list
        self.channel_name = channel_name
        self.initializeUI()

    def initializeUI(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("yt-notify")
        self.setWindowIcon(QIcon("images/icon.ico"))
        self.ui.label_title.setText(self.channel_name)
        short_title = ""
        for index, channel in enumerate(self.channel_list[self.channel_name]):
            title = channel['title']
            if len(title) > 57:
                short_title = title[0:52] + "..."
            elif len(title) <= 57:
                short_title = title[0:len(title)] +  (57 - len(title)) * " "
            else:
                short_title = title
            seen = str(channel['seen'])
            item = QTreeWidgetItem(self.ui.treeWidget, [short_title])
            item.setToolTip(0, title)

            if channel['seen'] == True:
                item.setCheckState(1, QtCore.Qt.CheckState.Checked)
            else:
                item.setCheckState(1, QtCore.Qt.CheckState.Unchecked)

        self.ui.treeWidget.resizeColumnToContents(0)
        self.resize(500, 729)

        self.ui.button_close.clicked.connect(self.close)

    def checkAll(self):
        pass

    def uncheckAll(self):
        pass

    def save(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = VideoWindow()
    main.show()
    sys.exit(app.exec_())
