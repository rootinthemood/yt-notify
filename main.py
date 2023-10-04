import os, sys, json, re, platform, subprocess
from functions import write_json, init_database, check_unseen, check_watching, init_settings
from scrapevideos import UpdateChannel
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QGridLayout, QMenu, QMessageBox, QSystemTrayIcon, QStatusBar, QProgressBar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from videos_window import VideoWindow
from functools import partial
from add_channel_window import addChannelWindow
from settings_window import settingsWindow
from systray import SystemTrayIcon
import qdarktheme

PLATFORM = platform.system()
CHANNEL_JSON = os.path.abspath("./data/data.json")
CHANNELS = init_database(CHANNEL_JSON)
SETTINGS_LOCATION = os.path.abspath("./data/settings.ini")
SETTINGS = init_settings(SETTINGS_LOCATION)

VERSION = "1.1.3"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initialize_ui()

    def initialize_ui(self):
        self.setMinimumSize(300, 172)
        self.setWindowTitle("yt-notify")
        self.setWindowIcon(QIcon(os.path.abspath("images/icon.ico")))

        self.setup_main_window()
        self.create_actions()
        self.create_menu()

        self.hide()

    def setup_main_window(self):
        """Sets up the main Qt Window and populates it with a button for each channel"""
        #Make statusbar
        self.setStatusBar(QStatusBar())

        #Make progressbar and set it in statusbar
        self.progressBar = QProgressBar()
        self.statusBar().addPermanentWidget(self.progressBar)
        self.progressBar.setMaximumSize(200, 20)
        self.progressBar.setHidden(True)
        self.progressBar.setValue(0)

        self.main_grid = QGridLayout()

        #Set the central widget in MainWindow
        container = QWidget()
        container.setLayout(self.main_grid)
        self.setCentralWidget(container)

        #Create a channel button for each channel name
        column_int = 0
        row_int = 0
        for channel in CHANNELS['channels']:
            if channel == "channels":
                continue
            if column_int == 3:
                row_int += 1
                column_int = 0
            name = channel['name']

            #Creation of channel buttons
            self.chan_button = QPushButton(name, self)
            
            #sets text color for buttons
            unseen_vids = check_unseen(name, CHANNELS)
            watching_vids = check_watching(name, CHANNELS)

            if unseen_vids > 0 and watching_vids == 0:
                self.chan_button.setStyleSheet('color: red')
                self.chan_button.setStatusTip(f"Not Seen: {unseen_vids}")
            if unseen_vids > 0 and watching_vids > 0:
                self.chan_button.setStyleSheet('color: blueviolet')
                self.chan_button.setStatusTip(f"Not Seen: {unseen_vids}, Watching: {watching_vids}")
            if watching_vids > 0 and unseen_vids == 0:
                self.chan_button.setStyleSheet('color: blue')
                self.chan_button.setStatusTip(f"Not Seen: {unseen_vids}, Watching: {watching_vids}")
            if unseen_vids == 0 and watching_vids == 0:
                self.chan_button.setStyleSheet('color: green')
                self.chan_button.setStatusTip(f"Everything seen!")

            #Pust name in list because UpdateChannel wants a list of channel names
            name_lst = [name]

            #Creation of dropdown menu on channel button
            menu = QMenu()
            self.chan_button.setMenu(menu)
            video_menu = menu.addAction("Videos")
            open_channel = partial(self.open_video_window, name)
            video_menu.triggered.connect(open_channel)

            menu.addSeparator()

            update_menu = menu.addAction("Update Channel")
            update_channel = partial(self.update_all_clicked, name_lst)
            update_menu.triggered.connect(update_channel)

            remove_channel_menu = menu.addAction("Remove Channel")
            delete_channel = partial(self.remove_channel, name)
            remove_channel_menu.triggered.connect(delete_channel)

            #Puts channel buttons on the grid layout
            self.main_grid.addWidget(self.chan_button, row_int, column_int)
            column_int += 1

        #If no channel button is found draw some text
        if self.main_grid.count() == 0:
            self.header = QLabel("Add channels to list them here", self)
            self.main_grid.addWidget(self.header, 0, 0)

        #Align everything in grid layout to top
        self.main_grid.setAlignment(Qt.AlignmentFlag.AlignTop)

    def create_actions(self):
        """Create the application menu actions."""
        self.add_channel_button = QAction("&Add channel")
        self.add_channel_button.setShortcut("Ctrl+A")
        self.add_channel_button.setStatusTip("Add a youtube channel to follow")
        self.add_channel_button.triggered.connect(self.add_channel)

        self.update_channels = QAction("&Update all channels")
        self.update_channels.setShortcut("Ctrl+U")
        update = partial(self.update_all_clicked, "")
        self.update_channels.triggered.connect(update)

        self.quit_act = QAction("&Quit")
        self.quit_act.setShortcut("Ctrl+Q")
        self.quit_act.triggered.connect(sys.exit)

        self.settings = QAction("Settings")
        self.settings.triggered.connect(self.open_settings_window)
        self.about = QAction("About")
        self.about.triggered.connect(self.about_window)

    def create_menu(self):
        """Create the top menu bar"""
        self.menuBar().setNativeMenuBar(False)

        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(self.add_channel_button)
        file_menu.addAction(self.update_channels)
        file_menu.addAction(self.quit_act)

        file_menu2 = self.menuBar().addMenu("Help")
        file_menu2.addAction(self.settings)
        file_menu2.addAction(self.about)

    def open_settings_window(self):
        self.new_settings_window = settingsWindow(SETTINGS, SETTINGS_LOCATION)
        self.new_settings_window.show()
        self.new_settings_window.init_trigger.connect(self.re_init_settings)

    def open_video_window(self, name):
        """Opens the VideoWindow for a given channel name"""
        self.new_video_window = VideoWindow(CHANNELS, name, CHANNEL_JSON, SETTINGS)
        self.new_video_window.show()
        self.new_video_window.close_trigger.connect(self.handle_close_trigger)

    def add_channel(self):
        """Opens the addChannelWindow"""
        self.add_channel_window = addChannelWindow(CHANNELS, CHANNEL_JSON)
        self.add_channel_window.show()
        #connect the trigger to the signal of addChannelWindow
        self.add_channel_window.close_trigger.connect(self.handle_close_trigger)

    def remove_channel(self, name):
        """Asks if user wants to remove given channel"""
        for index, channel in enumerate(CHANNELS['channels']):
            if name == channel['name']:
                answer = QMessageBox.question(self,
                                              "Remove Channel?",
                                              f"Are you sure you want to remove {name}?",
                                              QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes)
                if answer == QMessageBox.StandardButton.Yes:
                    CHANNELS['channels'].pop(index)
                    CHANNELS.pop(name)
                    write_json(CHANNELS, CHANNEL_JSON)
                    init_database(CHANNEL_JSON)
                    self.setup_main_window()

    def error_message(self, message):
        QMessageBox.critical(self, "Error",
                            f"<p>" + message + "</p>",
                            QMessageBox.StandardButton.Ok)



    def about_window(self):
        """Draws About window"""
        QMessageBox.about(self, "About", f"""<p style=font-size:30px>yt-notify</p>
                                             <p style=text-align:right> version {VERSION}</p>
                                             <p style=text-align:right> GPL-3.0</p>
                                             <p style=text-align:right> rootinthemood</p>""")

    #Runs when Update All Channels is clicked
    def update_all_clicked(self, names):
        """Creates a worker for UpdateChannel for given channel names"""
        self.update_channels.setEnabled(False)
        systray.update.setEnabled(False)
        self.progressBar.setHidden(False)
        self.progressBar.setValue(0)
        if names == "":
            names = [name for name in CHANNELS if name != "channels"]
        self.worker = UpdateChannel(names, CHANNELS)
        self.worker.start()
        self.worker.finished.connect(self.update_all_clicked_finished)
        self.worker.update_progress.connect(self.update_all_clicked_progress)
        self.worker.worker_complete.connect(self.notify_on_complete)
        self.worker.scrape_error.connect(self.error_message)

    def update_all_clicked_progress(self, val, name):
        """Runs when progress is updated via update_all_clicked"""
        text  = f"{name} - {val}%"
        self.progressBar.setTextVisible(True)
        self.progressBar.setFormat(text)
        self.progressBar.setValue(val)

    def update_all_clicked_finished(self):
        """Runs when progress is finished via update_all_clicked"""
        self.progressBar.setHidden(True)
        self.progressBar.setValue(0)
        self.update_channels.setEnabled(True)
        systray.update.setEnabled(True)

    def handle_close_trigger(self):
        """Redraws the main Qt qindow"""
        self.setup_main_window()

    def notify_on_complete(self, lst, dct):
        """Gets a list of tuples with the amount of new videos and a dict with the 'n' total videos(CHANNELS) 
        from scrapevideos.py->UpdateChannel class. Writes the dict to database
        and sends a notification to the user with new videos found."""
        write_json(dct, CHANNEL_JSON)
        self.setup_main_window()
        total_channels = len(lst)
        count = 0
        text = ""
        for channel in lst:
            if channel[0] == 'no':
                count += 1
                if count == total_channels:
                    self.notify_platform("No new videos")
                    return
                continue
            text += f"{channel[1]} - {channel[2]} new video(s)\n" 
            continue
        self.notify_platform(text)

    def notify_platform(self, text):
        """Pushes notification to os with given text"""
        print(text)
        icon = os.path.abspath("images/icon.png")
        subprocess.Popen(['notify-send', '-u', 'critical', '-i', icon,'-a', 'yt-notify', ' ', text])

    def re_init_settings(self):
        global SETTINGS
        global SETTINGS_LOCATION
        SETTINGS_LOCATION = os.path.abspath("./data/settings.ini")
        SETTINGS = init_settings(SETTINGS_LOCATION)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = MainWindow()
    qdarktheme.setup_theme(SETTINGS[2])
    systray = SystemTrayIcon(QIcon("images/icon.ico"), window)
    sys_update_all = partial(window.update_all_clicked, "")
    systray.update_signal.connect(sys_update_all)
    systray.show()
    
    sys.exit(app.exec())
