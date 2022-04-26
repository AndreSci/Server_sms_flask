from flask import Flask, render_template, request, make_response
from PyQt5 import QtCore, QtGui, QtWidgets
import configparser
import datetime
import requests
import os
import sys
import threading
import multiprocessing
import asyncio

# pyuic5 -x gui_sms_sender.ui -o gui_sms_sender.py
# auto-py-to-exe
# ---------------------------------------------------------------------------
app = Flask(__name__)  # создаем сервер flask   -----------------------------
# ---------------------------------------------------------------------------


PATH_LOG = ''
HOST = '0.0.0.0'
PORT = 8000
BALANCE_SMS_SERVICE = 0
number_black = "+79991115544"
TAKE_BALANCE_URL = ""
SERVICE_NAME = ""
ID_USER = ""
REQ_JSON = {}
URL_UP = '/sendsms/'


# сервисные функции ---------------------------------------------------------
def loggers(text):
    global PATH_LOG

    if not os.path.exists(PATH_LOG):
        os.makedirs(PATH_LOG)

    today = datetime.datetime.today()

    for_file_name = str(today.strftime("%Y-%m-%d"))

    with open(f'{PATH_LOG}{for_file_name}-LOG.log', 'a', encoding='utf-8') as file:
        # mess = str(today.strftime("%Y-%m-%d-%H.%M.%S")) + "\t" + text + "\n"
        mess = str(today.strftime("%H.%M.%S")) + "\t" + text + "\n"
        print(mess)
        file.write(mess)
# ---------------------------------------------------------------------------


def take_balance():
    global BALANCE_SMS_SERVICE
    global SERVICE_NAME
    global TAKE_BALANCE_URL

    try:
        req = requests.get(TAKE_BALANCE_URL)
        j_info = req.json()
        BALANCE_SMS_SERVICE = j_info["balance"]
        loggers(f"SUCCESS\t{take_balance.__name__}\ttake balance from {SERVICE_NAME} = {BALANCE_SMS_SERVICE}")  # log
    except ImportError:
        loggers(f"ERROR\t{take_balance.__name__}\ttake balance from {SERVICE_NAME}")  # log


def take_settings():
    global PORT
    global TAKE_BALANCE_URL
    global ID_USER
    global PATH_LOG

    # загружаем файл settings.ini
    if not os.path.isfile("settings.ini"):
        loggers(f"ERROR\t{take_settings.__name__}\tfile settings.ini not found")
        raise FileExistsError

    config_set = configparser.ConfigParser()
    config_set.read("settings.ini")

    ID_USER = config_set["GENERAL"]["USER_ID"]
    PATH_LOG = config_set["GENERAL"]["PATH_LOG"]
    PORT = config_set["GENERAL"]["PORT"]

    # создаем глобальную переменную содержащую url для запроса баланса
    TAKE_BALANCE_URL = f"https://sms.ru/my/balance?api_id={ID_USER}&json=1"


# --------------------------------------------------------------------------
# тело обработки запросов http ---------------------------------------------
# --------------------------------------------------------------------------

def send_sms(phone_num, text):
    global ID_USER
    global REQ_JSON

    req = requests.get(f"https://sms.ru/sms/send?api_id={ID_USER}&to={phone_num}&msg={text}&json=1")
    REQ_JSON = req.json()
    # парсер номеров на случай если будет не один номер в отправке
    if REQ_JSON["status"] == "OK":
        for it in REQ_JSON["sms"]:
            if REQ_JSON["sms"][it]["status"] == "ERROR":
                return "ERROR"
        return "SUCCESS"
    else:
        return "ERROR"


@app.route(URL_UP, methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        # it_url_param = False
        # Если запрос произведет с ImmutableMultiDict([])
        phone_num = request.form.get('fphone')
        text = request.form.get('ftext')

        # Если запрос произведен с параметрами в ссылке
        if not phone_num:
            phone_num = request.args.get('fphone')
            text = request.args.get('ftext')
            # it_url_param = True

        status_m = send_sms(phone_num, text)

        loggers(f"{status_m}\t{index.__name__}\tsend to {phone_num}\ttext: {text}")  # log

        return REQ_JSON

        # if it_url_param: return REQ_JSON else: return render_template("index.html", event_app=status_m)

    elif request.method == "GET":
        if os.path.isfile("./templates/index.html"):
            loggers(f"SUCCESS\t{index.__name__}\tsend - index.html")  # log
            return render_template("index.html")    # открываем страницу отправки сообщения
        else:
            loggers(f"ERROR\t{index.__name__}\tfile index.html not found")
            return make_response(f"<h2>Error: 400, fail open file index.html</h2>")
    else:
        loggers(f"ERROR\t{index.__name__}\twrong address: {request.method}, {request.full_path}")  # log
        return make_response("<h2>Error: {0}</h2>".format(400))   # открываем страницу отправки сообщения

# --------------------------------------------------------------------------


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 720)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 720))
        MainWindow.setMaximumSize(QtCore.QSize(1000, 720))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.change_but = QtWidgets.QPushButton(self.centralwidget)
        self.change_but.setGeometry(QtCore.QRect(890, 120, 71, 51))
        self.change_but.setObjectName("change_but")
        self.hide_but = QtWidgets.QPushButton(self.centralwidget)
        self.hide_but.setGeometry(QtCore.QRect(890, 180, 71, 51))
        self.hide_but.setObjectName("hide_but")
        self.stop_but = QtWidgets.QPushButton(self.centralwidget)
        self.stop_but.setGeometry(QtCore.QRect(880, 620, 71, 51))
        self.stop_but.setObjectName("stop_but")
        self.stack_Window = QtWidgets.QStackedWidget(self.centralwidget)
        self.stack_Window.setGeometry(QtCore.QRect(20, 60, 821, 631))
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
        self.label_status = QtWidgets.QLabel(self.send_window)
        self.label_status.setGeometry(QtCore.QRect(30, 590, 371, 31))
        self.label_status.setObjectName("label_status")
        self.stack_Window.addWidget(self.send_window)
        self.log_window = QtWidgets.QWidget()
        self.log_window.setObjectName("log_window")
        self.scrollArea = QtWidgets.QScrollArea(self.log_window)
        self.scrollArea.setGeometry(QtCore.QRect(10, 0, 101, 631))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 99, 629))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.log_window)
        self.scrollArea_2.setGeometry(QtCore.QRect(110, 0, 711, 631))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 709, 629))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.stack_Window.addWidget(self.log_window)
        self.title_lab = QtWidgets.QLabel(self.centralwidget)
        self.title_lab.setGeometry(QtCore.QRect(20, 10, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.title_lab.setFont(font)
        self.title_lab.setObjectName("title_lab")
        self.start_but = QtWidgets.QPushButton(self.centralwidget)
        self.start_but.setGeometry(QtCore.QRect(890, 60, 71, 51))
        self.start_but.setObjectName("start_but")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stack_Window.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.change_but.setText(_translate("MainWindow", "Change"))
        self.hide_but.setText(_translate("MainWindow", "Hide"))
        self.stop_but.setText(_translate("MainWindow", "Stop"))
        self.line_phone.setText(_translate("MainWindow", "+79991112233"))
        self.label_phone.setText(_translate("MainWindow", "Phone"))
        self.label_message.setText(_translate("MainWindow", "Message"))
        self.label_status.setText(_translate("MainWindow", "status:"))
        self.title_lab.setText(_translate("MainWindow", "VIG sms sender"))
        self.start_but.setText(_translate("MainWindow", "Start"))


# ----------------------------------------------------------------------------

def thread_flask():
    print("Hallo i'm Flask")
    app.run(debug=False, host=HOST, port=int(PORT))


class threadPyqt():
    def __init__(self):
        super().__init__()
        print("Hallo i'm PyQt")
        self.app_ui = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.thread_for_flask = threading.Thread(target=thread_flask, name="VIG_sms_server")

        self.ui.hide_but.clicked.connect(self.hide_gui)

        # self.ui.change_but.clicked.connect(self.change_log_send)
        self.ui.change_but.clicked.connect(self.check_flask)

        self.ui.stop_but.clicked.connect(self.close_flask)
        self.ui.start_but.clicked.connect(self.run_flask)

    def show(self):
        self.MainWindow.show()

    def change_log_send(self):
        pass

    def hide_gui(self):
        pass

    def exit(self):
        sys.exit(self.app_ui.exec_())

    def thread_flask(self):
        app.run(debug=False, host=HOST, port=int(PORT))

    def run_flask(self):
        self.thread_for_flask.start()

    def check_flask(self):
        self.ui.label_status.setText(f"status: Thread flask is {self.thread_for_flask.is_alive()}")

    def close_flask(self):
        pass


if __name__ == "__main__":
    # подгружаем данные из файла settings
    take_settings()
    # получаем наш баланс
    gui = threadPyqt()
    gui.show()

    gui.exit()
    # запускаем сервер flask
