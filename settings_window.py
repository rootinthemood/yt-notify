import sys
import os
from PyQt6.QtWidgets import QWidget, QTreeWidgetItem, QMenu, QDialogButtonBox, QDialog
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import pyqtSignal
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from functions import write_json
from settings_window_ui import Ui_settings_dialog

class SettingsWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.ui = Ui_settings_dialog()
#        test = self.ui.buttonBox.StandardButton.Cancel
#        self.ui.buttonBox.button(QDialog.)
        
         
#        self.ui.buttonBox.accepted.connect(self.settings_apply)
#        self.ui.buttonBox.rejected.connect(self.settings_cancel)
#        self.ui.buttonBox(QDialogButtonBox.StandardButton.Cancel).clicked.connect(self.settings_cancel)

    def settings_apply(self):
        pass

    def settings_cancel(self):
        self.close()
