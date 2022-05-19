# Form implementation generated from reading ui file 'settings_window.ui'
#
# Created by: PyQt6 UI code generator 6.3.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_settings_dialog(object):
    def setupUi(self, settings_dialog):
        settings_dialog.setObjectName("settings_dialog")
        settings_dialog.resize(400, 300)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(settings_dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.auto_seen_checkb = QtWidgets.QCheckBox(settings_dialog)
        self.auto_seen_checkb.setObjectName("auto_seen_checkb")
        self.verticalLayout_2.addWidget(self.auto_seen_checkb, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(settings_dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Apply|QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(settings_dialog)
        QtCore.QMetaObject.connectSlotsByName(settings_dialog)

    def retranslateUi(self, settings_dialog):
        _translate = QtCore.QCoreApplication.translate
        settings_dialog.setWindowTitle(_translate("settings_dialog", "Settings"))
        self.auto_seen_checkb.setText(_translate("settings_dialog", "Auto seen on play/open video"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    settings_dialog = QtWidgets.QDialog()
    ui = Ui_settings_dialog()
    ui.setupUi(settings_dialog)
    settings_dialog.show()
    sys.exit(app.exec())