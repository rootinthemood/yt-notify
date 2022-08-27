import sys, os
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal
from functions import init_database, write_json, url_check, save_settings
from settings_window_ui import Ui_Form
from scrapevideos import scrape_channel
from PyQt6 import QtCore, QtGui, QtWidgets

class settingsWindow(QWidget):
    init_trigger = pyqtSignal()

    def __init__(self, settings, settings_location):
        super().__init__()
        self.mpv_args = settings[0]
        self.vlc_args = settings[1]
        self.settings_location = settings_location
        self.initialize_ui()

    def initialize_ui(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("settings")
        self.setWindowIcon(QIcon("images/icon.ico"))
        self.ui.mpv_args.setPlaceholderText('--ytdl-format="bestvideo[height<=1080]+bestaudio/best"')
        self.ui.vlc_args.setPlaceholderText("--preferred-resolution 1080")
        self.ui.vlc_args.setText(self.vlc_args)
        self.ui.mpv_args.setText(self.mpv_args)
        self.ui.vlc_args.setText(self.vlc_args)

        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).clicked.connect(self.close)
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Save).clicked.connect(self.save)

    def save(self):

        mpv_args = self.ui.mpv_args.text()
        vlc_args = self.ui.vlc_args.text()
        save_settings(mpv_args, vlc_args, self.settings_location)
        self.init_trigger.emit()
        self.close()
