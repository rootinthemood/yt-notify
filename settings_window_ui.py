# Form implementation generated from reading ui file 'settings_window.ui'
#
# Created by: PyQt6 UI code generator 6.3.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(553, 110)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setAutoFillBackground(False)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.mpv_args = QtWidgets.QLineEdit(Form)
        self.mpv_args.setText("")
        self.mpv_args.setObjectName("mpv_args")
        self.gridLayout.addWidget(self.mpv_args, 0, 1, 1, 1)
        self.vlc_args = QtWidgets.QLineEdit(Form)
        self.vlc_args.setText("")
        self.vlc_args.setObjectName("vlc_args")
        self.gridLayout.addWidget(self.vlc_args, 1, 1, 1, 1)
        self.mpv_label = QtWidgets.QLabel(Form)
        self.mpv_label.setObjectName("mpv_label")
        self.gridLayout.addWidget(self.mpv_label, 0, 0, 1, 1)
        self.vlc_label = QtWidgets.QLabel(Form)
        self.vlc_label.setObjectName("vlc_label")
        self.gridLayout.addWidget(self.vlc_label, 1, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Form)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.mpv_label.setText(_translate("Form", "mpv arguments:"))
        self.vlc_label.setText(_translate("Form", "VLC arguments:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
