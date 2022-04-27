# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_sms_sender.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1232, 720)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 720))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(718, 60))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setMinimumSize(QtCore.QSize(173, 0))
        self.frame_2.setMaximumSize(QtCore.QSize(173, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.title_lab = QtWidgets.QLabel(self.frame_2)
        self.title_lab.setGeometry(QtCore.QRect(10, 0, 171, 51))
        self.title_lab.setMinimumSize(QtCore.QSize(171, 0))
        self.title_lab.setMaximumSize(QtCore.QSize(173, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.title_lab.setFont(font)
        self.title_lab.setObjectName("title_lab")
        self.horizontalLayout_2.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label_status = QtWidgets.QLabel(self.frame_3)
        self.label_status.setGeometry(QtCore.QRect(10, 10, 371, 31))
        self.label_status.setObjectName("label_status")
        self.horizontalLayout_2.addWidget(self.frame_3)
        self.verticalLayout_2.addWidget(self.frame)
        self.frame_4 = QtWidgets.QFrame(self.centralwidget)
        self.frame_4.setMinimumSize(QtCore.QSize(718, 0))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.stack_Window = QtWidgets.QStackedWidget(self.frame_4)
        self.stack_Window.setObjectName("stack_Window")
        self.send_window = QtWidgets.QWidget()
        self.send_window.setObjectName("send_window")
        self.line_phone = QtWidgets.QLineEdit(self.send_window)
        self.line_phone.setGeometry(QtCore.QRect(110, 30, 481, 31))
        self.line_phone.setObjectName("line_phone")
        self.line_message = QtWidgets.QLineEdit(self.send_window)
        self.line_message.setGeometry(QtCore.QRect(110, 100, 481, 151))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.line_message.setFont(font)
        self.line_message.setText("")
        self.line_message.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.line_message.setObjectName("line_message")
        self.label_phone = QtWidgets.QLabel(self.send_window)
        self.label_phone.setGeometry(QtCore.QRect(30, 30, 61, 31))
        self.label_phone.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_phone.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_phone.setObjectName("label_phone")
        self.label_message = QtWidgets.QLabel(self.send_window)
        self.label_message.setGeometry(QtCore.QRect(30, 100, 61, 31))
        self.label_message.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_message.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_message.setObjectName("label_message")
        self.stack_Window.addWidget(self.send_window)
        self.log_window = QtWidgets.QWidget()
        self.log_window.setObjectName("log_window")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.log_window)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.text_logs = QtWidgets.QTextBrowser(self.log_window)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.text_logs.setFont(font)
        self.text_logs.setObjectName("text_logs")
        self.horizontalLayout.addWidget(self.text_logs)
        self.stack_Window.addWidget(self.log_window)
        self.horizontalLayout_3.addWidget(self.stack_Window)
        self.frame_6 = QtWidgets.QFrame(self.frame_4)
        self.frame_6.setMinimumSize(QtCore.QSize(120, 390))
        self.frame_6.setMaximumSize(QtCore.QSize(120, 16777215))
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_5 = QtWidgets.QFrame(self.frame_6)
        self.frame_5.setMinimumSize(QtCore.QSize(0, 193))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.start_but = QtWidgets.QPushButton(self.frame_5)
        self.start_but.setGeometry(QtCore.QRect(20, 10, 71, 51))
        self.start_but.setObjectName("start_but")
        self.clear_but = QtWidgets.QPushButton(self.frame_5)
        self.clear_but.setGeometry(QtCore.QRect(20, 70, 71, 51))
        self.clear_but.setObjectName("clear_but")
        self.check_but = QtWidgets.QPushButton(self.frame_5)
        self.check_but.setGeometry(QtCore.QRect(20, 130, 71, 51))
        self.check_but.setObjectName("check_but")
        self.verticalLayout.addWidget(self.frame_5)
        self.frame_7 = QtWidgets.QFrame(self.frame_6)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout.addWidget(self.frame_7)
        self.horizontalLayout_3.addWidget(self.frame_6)
        self.verticalLayout_2.addWidget(self.frame_4)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stack_Window.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title_lab.setText(_translate("MainWindow", "VIG sms sender"))
        self.label_status.setText(_translate("MainWindow", "status:"))
        self.line_phone.setText(_translate("MainWindow", "+79991112233"))
        self.label_phone.setText(_translate("MainWindow", "Phone"))
        self.label_message.setText(_translate("MainWindow", "Message"))
        self.start_but.setText(_translate("MainWindow", "Start"))
        self.clear_but.setText(_translate("MainWindow", "Clear"))
        self.check_but.setText(_translate("MainWindow", "Check"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
