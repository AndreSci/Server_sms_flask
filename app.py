from flask import Flask, render_template, request, make_response
from PyQt5 import QtCore, QtGui, QtWidgets
import configparser
import datetime
import requests
import os
import sys
import threading
from multiprocessing import Process


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

ADD_LOG = ''


# сервисные функции ---------------------------------------------------------
def loggers(text, status=0):
    """ status
        0 = SUCCESS
        1 = ERROR
        2 = EVENT
    """
    global PATH_LOG
    global GUI_ADD_LOGS
    global ADD_LOG

    if not os.path.exists(PATH_LOG):
        os.makedirs(PATH_LOG)

    today = datetime.datetime.today()

    for_file_name = str(today.strftime("%Y-%m-%d"))

    color_s = "black"
    if status == 1:
        color_s = "red"
    elif status == 2:
        color_s = "blue"

    with open(f'{PATH_LOG}{for_file_name}-LOG.log', 'a', encoding='utf-8') as file:
        # mess = str(today.strftime("%Y-%m-%d-%H.%M.%S")) + "\t" + text + "\n"
        mess = str(today.strftime("%H.%M.%S")) + "\t" + text + "\n"
        print(mess)
        file.write(mess)
        ADD_LOG.add_log(f"<font color=\"{color_s}\">{mess}")
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
        loggers(f"ERROR\t{take_balance.__name__}\ttake balance from {SERVICE_NAME}", 1)  # log


def take_settings():
    global PORT
    global TAKE_BALANCE_URL
    global ID_USER
    global PATH_LOG

    # загружаем файл settings.ini
    if not os.path.isfile("settings.ini"):
        loggers(f"ERROR\t{take_settings.__name__}\tfile settings.ini not found", 1)
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
        log_status = 0
        if status_m == "ERROR":
            log_status = 1

        loggers(f"{status_m}\t{index.__name__}\tsend to {phone_num}\ttext: {text}", log_status)  # log

        return REQ_JSON

        # if it_url_param: return REQ_JSON else: return render_template("index.html", event_app=status_m)

    elif request.method == "GET":
        print(request.host)
        if os.path.isfile("./templates/index.html"):
            loggers(f"EVENT\t{index.__name__}\tsend - index.html", 2)  # log
            return render_template("index.html")    # открываем страницу отправки сообщения
        else:
            loggers(f"ERROR\t{index.__name__}\tfile index.html not found", 1)
            return make_response(f"<h2>Error: 400, fail open file index.html</h2>")
    else:
        loggers(f"ERROR\t{index.__name__}\twrong address: {request.method}, {request.full_path}", 1)  # log
        return make_response("<h2>Error: {0}</h2>".format(400))   # открываем страницу отправки сообщения

# --------------------------------------------------------------------------


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


# ----------------------------------------------------------------------------


class threadPyqt():
    """ Запуск сервера Фласк происходит в функйии thread_flask() """
    def thread_flask(self):
        print("Hallo i'm Flask")
        app.run(debug=False, host=HOST, port=int(PORT))

    def __init__(self):
        super().__init__()
        print("Hallo i'm PyQt")
        self.app_ui = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.thread_for_flask = threading.Thread(target=self.thread_flask, name="VIG_sms_server")

        self.MainWindow.setWindowTitle("VIG_sms_server")

        self.ui.check_but.clicked.connect(self.check_flask)

        # self.ui.change_but.clicked.connect(self.change_log_send)
        self.ui.clear_but.clicked.connect(self.clear_logs)

        self.ui.start_but.clicked.connect(self.run_flask)

    def show(self):
        self.MainWindow.show()

    def add_log(self, text_log):
        self.ui.text_logs.append(str(text_log))

    def clear_logs(self):
        self.ui.text_logs.clear()

    def exit(self):
        sys.exit(self.app_ui.exec_())

    def run_flask(self):
        self.ui.start_but.setText("Exit")
        self.thread_for_flask.start()
        self.ui.label_status.setText(f"status: Server status is {self.thread_for_flask.is_alive()}")

    def check_flask(self):
        self.ui.label_status.setText(f"status: Server status is {self.thread_for_flask.is_alive()}")
        take_balance()


if __name__ == "__main__":
    # подгружаем данные из файла settings
    take_settings()
    # получаем наш баланс

    gui = threadPyqt()

    ADD_LOG = gui  # делаем класс глобальным для получение доступа из других функция в методы класса

    gui.show()
    gui.exit()
    # запускаем сервер flask
