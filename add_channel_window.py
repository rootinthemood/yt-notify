import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal
from functions import init_database, write_json, url_check
from add_channel_window_ui import Ui_add_channel
from scrapevideos import scrape_channel


class addChannelWindow(QWidget):
    #Make signal for closeEvent
    close_trigger = pyqtSignal()

    def __init__(self, channel_list, json_location):
        super().__init__()
        self.channel_list = channel_list
        self.json_location = json_location
        self.initializeUI()

    def closeEvent(self, event):
        """Overwrites the closeEvent and emits a signal on close"""
        super(addChannelWindow, self).closeEvent(event)
        event.accept()
        self.close_trigger.emit()

    def initializeUI(self):
        self.ui = Ui_add_channel()
        self.ui.setupUi(self)
        self.setWindowTitle("Add Channel")
        self.setWindowIcon(QIcon("images/icon.ico"))

        self.ui.add_button.clicked.connect(self.add)
        self.ui.cancel_button.clicked.connect(self.close)

    def add(self):
        self.name = self.ui.name_edit.text()
        self.url = self.ui.url_edit.text()

        for channel in self.channel_list['channels']:
            if not url_check(self.url):
                QMessageBox.warning(self, "Error",
                                    f"<p>Incorrect URL format</p>",
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
        except:
            QMessageBox.warning(self, "Error",
                                "Channel probably not found",
                                QMessageBox.StandardButton.Ok)
            for index, channel in enumerate(self.channel_list['channels']):
                if self.name == channel['name']:
                    self.channel_list['channels'].pop(index)
                    self.channel_list.pop(self.name)

        write_json(self.channel_list, self.json_location)
        init_database(self.json_location)
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = addChannelWindow()
    main.show()
    sys.exit(app.exec_())
