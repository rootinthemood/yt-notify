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
        self.action.triggered.connect(self.showParent)
        menu.addAction(self.action)

        self.update = QAction("Update all channels")
        self.update.triggered.connect(self.updateAll)
        menu.addAction(self.update)

#        # Add a Quit option to the menu.
        self.quit = QAction("Quit")
        self.quit.triggered.connect(self.exitAll)
        menu.addAction(self.quit)


#        # Add the menu to the tray
        self.setContextMenu(menu)
        self.setVisible(True)
        self.setToolTip("yt-notify")

    def exitAll(self):
        sys.exit()

    def showParent(self):
        self.parent().show()

    def updateAll(self):
        self.update_signal.emit(True)
        
