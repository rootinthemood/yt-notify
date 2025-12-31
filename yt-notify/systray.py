import sys
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSignal

class SystemTrayIcon(QSystemTrayIcon):
    update_signal = pyqtSignal(bool)

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        self.action = QAction("Show", parent=self)
        self.action.triggered.connect(self.show_parent)
        menu.addAction(self.action)

        self.update = QAction("Update all channels")
        self.update.triggered.connect(self.update_all)
        menu.addAction(self.update)

        # Add a Quit option to the menu.
        self.quit = QAction("Quit")
        self.quit.triggered.connect(self.exit_all)
        menu.addAction(self.quit)

        # Add the menu to the tray
        self.setContextMenu(menu)
        self.setVisible(True)
        self.setToolTip("yt-notify")

        # Connect the activated signal to handle left-click
        self.activated.connect(self.handle_tray_click)

    def handle_tray_click(self, reason):
        # Check if the tray icon was left-clicked
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.parent().isVisible():
                self.parent().hide()
            else:
                self.show_parent()

    def exit_all(self):
        sys.exit()

    def show_parent(self):
        self.parent().show()

    def update_all(self):
        self.update_signal.emit(True)
        
