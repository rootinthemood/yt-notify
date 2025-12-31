import sys, os
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal
from functions import save_settings
from ui.settings_window_ui import Ui_Form
from PyQt6 import QtCore, QtWidgets
import qdarktheme

class settingsWindow(QWidget):
    init_trigger = pyqtSignal()

    def __init__(self, settings, settings_location):
        super().__init__()
        self.mpv_args = settings[0]
        self.vlc_args = settings[1]
        self.darkmode_args = settings[2]
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

        self.ui.dark_combo.addItems(qdarktheme.get_themes())
        index = self.ui.dark_combo.findText(self.darkmode_args, QtCore.Qt.MatchFlag.MatchFixedString)
        if index >= 0:
            self.ui.dark_combo.setCurrentIndex(index)
        self.ui.dark_combo.currentTextChanged.connect(qdarktheme.setup_theme)

        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).clicked.connect(self.close)
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Save).clicked.connect(self.save)

    def save(self):

        mpv_args = self.ui.mpv_args.text()
        vlc_args = self.ui.vlc_args.text()
        darkmode_args = self.ui.dark_combo.currentText()
        save_settings(mpv_args, vlc_args, darkmode_args, self.settings_location)
        self.init_trigger.emit()
        self.close()
