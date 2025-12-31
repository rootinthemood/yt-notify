from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal
from PyQt6 import QtWidgets
from functions import init_database, write_json, url_check
from ui.add_channel_window_ui import Ui_add_channel
from scrapevideos import scrape_channel


class addChannelWindow(QWidget):
    #Make signal for closeEvent
    close_trigger = pyqtSignal()

    def __init__(self, channel_list, json_location):
        super().__init__()
        self.channel_list = channel_list
        self.json_location = json_location
        self.initialize_ui()

    def close_event(self, event):
        """Overwrites the closeEvent and emits a signal on close"""
        super(addChannelWindow, self).closeEvent(event)
        event.accept()
        self.close_trigger.emit()

    def initialize_ui(self):
        self.ui = Ui_add_channel()
        self.ui.setupUi(self)
        self.setWindowTitle("Add Channel")
        self.setWindowIcon(QIcon("images/icon.ico"))

        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).clicked.connect(self.add)
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).clicked.connect(self.close)

    def add(self):
        self.name = self.ui.name_edit.text()
        self.url = self.ui.url_edit.text()

        for channel in self.channel_list['channels']:
            if not url_check(self.url):
                QMessageBox.warning(self, "Error",
                                    "<p>Incorrect URL format</p>",
                                    QMessageBox.StandardButton.Ok)
                return False
            elif self.name == channel['name']:
                QMessageBox.warning(self, "Error",
                                    f"<p>{self.name} already in database</p>",
                                    QMessageBox.StandardButton.Ok)
                return False
            elif self.url == channel['url']:
                QMessageBox.warning(self, "Error",
                                    "URL already in database",
                                    QMessageBox.StandardButton.Ok)
                return False

        self.channel_list['channels'].append({'name': self.name, 'url': self.url})
        self.channel_list[self.name] = []
        try:
            scrape_channel(self.name, self.channel_list)
        except Exception as error:
            error_txt = "type: {0}, error: {1}".format(type(error).__name__, error)
            print(error_txt)
            QMessageBox.warning(self, "Error",
                                error_txt,
                                QMessageBox.StandardButton.Ok)
            for index, channel in enumerate(self.channel_list['channels']):
                if self.name == channel['name']:
                    self.channel_list['channels'].pop(index)
                    self.channel_list.pop(self.name)

        write_json(self.channel_list, self.json_location)
        init_database(self.json_location)
        self.close_trigger.emit()
        self.close()
