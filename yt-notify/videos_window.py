import platform
from PyQt6.QtWidgets import QWidget, QTreeWidgetItem, QMenu, QMessageBox
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QProcess, pyqtSignal, Qt
from PyQt6 import QtCore, QtWidgets
from functions import write_json
from ui.video_window_ui import Ui_Form
import webbrowser
from shutil import which
import pyperclip as pc


class VideoWindow(QWidget):
    close_trigger = pyqtSignal()

    def __init__(self, channel_list, channel_name, json_location, settings, icon):
        super().__init__()
        self.channel_list = channel_list
        self.channel_name = channel_name
        self.json_location = json_location
        self.icon = icon
        self.initialize_ui()
        self.platform = platform.system()
        self.mpv_args = settings[0]
        self.vlc_args = settings[1]

    def initialize_ui(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle(self.channel_name)
        self.setWindowIcon(QIcon(str(self.icon)))
        self.ui.label_title.setText(self.channel_name)

        # Connect contextmenu to treewidget
        self.ui.treeWidget.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.ui.treeWidget.customContextMenuRequested.connect(self.menu_context_tree)

        self.ui.treeWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )

        self.ui.label_found.setHidden(True)
        self.ui.found_total.setHidden(True)

        total_vids = 0
        for channel in self.channel_list[self.channel_name]:
            video_id = channel["video_id"]
            title = channel["title"]
            total_vids += 1
            item = QTreeWidgetItem(self.ui.treeWidget, [title])
            item.setToolTip(0, title)
            item.setText(2, video_id)
            if channel["seen"]:
                item.setCheckState(1, QtCore.Qt.CheckState.Checked)
            elif channel["seen"] == "Watching":
                item.setCheckState(1, QtCore.Qt.CheckState.PartiallyChecked)
            else:
                item.setCheckState(1, QtCore.Qt.CheckState.Unchecked)

        self.ui.treeWidget.setColumnWidth(0, 400)
        self.ui.treeWidget.setColumnWidth(1, 10)
        self.ui.treeWidget.setColumnHidden(2, True)
        self.resize(500, 729)

        self.ui.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Save
        ).clicked.connect(self.save)
        self.ui.buttonBox.button(
            QtWidgets.QDialogButtonBox.StandardButton.Close
        ).clicked.connect(self.close)

        self.ui.button_check.clicked.connect(self.check_all)
        self.ui.button_uncheck.clicked.connect(self.uncheck_all)

        self.ui.total_vids.setText(f"{total_vids}")

        self.ui.le_search.returnPressed.connect(self.search)

    def check_all(self):
        """checks all checkbuttons"""
        root = self.ui.treeWidget.invisibleRootItem()
        assert root is not None

        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            item.setCheckState(1, QtCore.Qt.CheckState.Checked)

    def uncheck_all(self):
        """uncheck all checkbuttons"""
        root = self.ui.treeWidget.invisibleRootItem()
        assert root is not None

        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            item.setCheckState(1, QtCore.Qt.CheckState.Unchecked)

    def save(self):
        """Saves the checkbutton state to json"""
        root = self.ui.treeWidget.invisibleRootItem()
        assert root is not None
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            item.text(0)  # text at first (0) column
            video_id = item.text(2)
            state = item.checkState(1)
            for index, video in enumerate(self.channel_list[self.channel_name]):
                if video_id == video["video_id"]:
                    if state.value == 2:
                        self.channel_list[self.channel_name][index]["seen"] = True
                    elif state.value == 1:
                        self.channel_list[self.channel_name][index]["seen"] = "Watching"
                    else:
                        self.channel_list[self.channel_name][index]["seen"] = False
        write_json(self.channel_list, self.json_location)
        self.close_trigger.emit()

    def menu_context_tree(self, point):
        """Make a contextmenu per item in treewidget"""
        index = self.ui.treeWidget.indexAt(point)

        if not index.isValid():
            return

        item = self.ui.treeWidget.itemAt(point)
        assert item is not None
        video_id = item.text(2)  # The text of the node.
        yt_link = "https://www.youtube.com/watch?v=" + video_id

        # Make the menu
        menu = QMenu()
        self.open_browser = QAction("&Open in browser")
        self.open_browser.triggered.connect(
            lambda _, yt_link=yt_link: webbrowser.open_new_tab(yt_link)
            and item.setCheckState(1, QtCore.Qt.CheckState.PartiallyChecked)
        )
        menu.addAction(self.open_browser)

        if which("mpv"):
            mpv_args = self.mpv_args + " " + yt_link
            self.play_mpv = QAction("&Play with mpv")
            self.play_mpv.triggered.connect(
                lambda _, mpv_args=mpv_args: (
                    self.run_subprocess("mpv", mpv_args, item),  # Run the subprocess
                    )
            )
            menu.addAction(self.play_mpv)

        if which("vlc"):
            vlc_args = self.vlc_args + " " + yt_link
            self.play_vlc = QAction("&Play with vlc")
            self.play_vlc.triggered.connect(
                lambda _, vlc_args=vlc_args: (
                    self.run_subprocess("vlc", vlc_args, item),  # Run the subprocess
                    )
            )
            menu.addAction(self.play_vlc)


        self.copy_link = QAction("&Copy link")
        self.copy_link.triggered.connect(lambda _, yt_link=yt_link: pc.copy(yt_link))
        menu.addAction(self.copy_link)

        menu.exec(self.ui.treeWidget.mapToGlobal(point))


    def run_subprocess(self, program, args, item):
        program_location = which(program)
        if program_location is None:
            self.show_error("Program not found", "The specified program could not be found.")
            return

        try:
            process = QProcess(self)

            def handle_finished():
                if process.exitStatus() == QProcess.ExitStatus.NormalExit and process.exitCode() == 0:
                    item.setCheckState(1, Qt.CheckState.PartiallyChecked)
                else:
                    stdout = process.readAllStandardOutput().data().decode().strip()
                    stderr = process.readAllStandardError().data().decode().strip()

                    if stderr:
                        print("Error:", stderr)
                        self.show_error("Error", stderr)
                    elif stdout:
                        print("Standard Output:", stdout)
                        self.show_error("Error", stdout)
                    else:
                        self.show_error("Error", "Unknown error. No output captured.")

            # Connect the finished signal to the handle_finished function
            process.finished.connect(handle_finished)

            # Start the process with the specified program and arguments
            process.start(program_location, args.split())

            # Check if the process started successfully
            if not process.waitForStarted():
                raise Exception("Failed to start the process")

        except Exception as e:
            error_message = f"Unexpected Error: {str(e)}"
            print(error_message)
            self.show_error("Error", error_message)


    def show_error(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec()

    def search(self):
        search_text = self.ui.le_search.text()
        root = self.ui.treeWidget.invisibleRootItem()
        assert root is not None
        child_count = root.childCount()
        found_total = 0
        self.ui.label_found.setVisible(True)
        self.ui.found_total.setVisible(True)
        self.ui.treeWidget.setCurrentItem(root.child(-1))

        if search_text == "":
            self.ui.found_total.setText(str(found_total))
            return

        self.ui.treeWidget.setCurrentItem(root.child(-1))
        self.ui.treeWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.MultiSelection
        )

        for i in range(child_count):
            item = root.child(i)
            assert item is not None
            title = item.text(0)  # text at first (0) column
            item.text(2)
            item.checkState(1)

            if search_text in title.lower():
                self.ui.treeWidget.setCurrentItem(item)
                found_total += 1

        self.ui.found_total.setText(str(found_total))
        self.ui.treeWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )
