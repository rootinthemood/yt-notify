from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit, QCheckBox, QTextEdit, QGridLayout, QMenu, QScrollArea, QVBoxLayout
from PyQt6.QtGui import QAction, QIcon, QFont
from PyQt6.QtCore import Qt, QSize
from functions import init_database


class VideoWindow(QMainWindow):

    def __init__(self, channel_list, channel_name):
        super().__init__()
        self.channel_list = channel_list
        self.channel_name = channel_name
        self.initializeUI()

    def initializeUI(self):
        self.setMinimumSize(300, 172)
        self.setMaximumSize(900, 780)
        self.setWindowTitle("yt-notify")
        self.setWindowIcon(QIcon("images/icon.ico"))

        self.setUpMainWindow()

    def setUpMainWindow(self):
        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.vbox = QVBoxLayout()
#        self.main_grid = QGridLayout()
        for index, channel in enumerate(self.channel_list[self.channel_name]):
            title = channel['title']
            self.label = QLabel(title, self)
            self.vbox.addWidget(self.label)
        self.widget.setLayout(self.vbox)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        self.setGeometry(600, 100, 1000, 900)
        self.setWindowTitle('Scroll Area Demonstration')
        self.show()

        return
        #scroll area properties
#            self.main_grid.setRowStretch(1, 1)
#            self.main_grid.addWidget(self.label, index, 0)
#        self.setLayout(self.main_grid)

#        column_int = 0
#        row_int = 0
#        self.main_grid = QGridLayout()
#
#        #Set the central widget(needed because of QMainWindow)
#
#        for channel in self.channel_list['channels']:
#            if channel == "channels":
#                continue
#            if column_int == 3:
#                row_int += 1
#                column_int = 0
#            name = channel['name']
#
#            self.chan_button = QPushButton(name, self)
#
#            self.main_grid.addWidget(self.chan_button, row_int, column_int)
#            column_int += 1
#        self.setLayout(self.main_grid)
