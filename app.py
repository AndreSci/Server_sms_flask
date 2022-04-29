from flask import Flask, render_template, request, make_response
from PyQt5 import QtCore, QtGui, QtWidgets
import configparser
import datetime
import requests
import os
import sys
import threading
import json
from multiprocessing import Process


# pyuic5 -x gui_sms_sender_ru.ui -o gui_sms_sender2.py
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
LOW_BALANCE = 1
ADD_LOG = ''
PHONE_NUMBER = "+79991112233"

FLAG_MIN_BAL = True  # True разрешает отправку сообщения


# сервисные функции ---------------------------------------------------------
def loggers(text, status=0):
    """ описание переменной status \n
        0 = SUCCESS \n
        1 = ERROR \n
        2 = EVENT \n
    """
    global PATH_LOG
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
        mess = str(today.strftime("%Y-%m-%d-%H.%M.%S")) + "\t" + text + "\n"
        # mess = str(today.strftime("%H.%M.%S")) + "\t" + text + "\n"
        print(mess)
        file.write(mess)
        ADD_LOG.add_log(f"<font color=\"{color_s}\">{mess}")
# ---------------------------------------------------------------------------


def low_balance(balance):
    """
    Функция проверяет остаток баланса и отправляет 1 раз в
    день предупреждение если баланс ниже заданного значения
    """
    global LOW_BALANCE
    global FLAG_MIN_BAL
    global SERVICE_NAME

    if int(balance) < int(LOW_BALANCE):
        today = datetime.datetime.today()
        json_mess = {"day": today.date().day, "month": today.date().month, "time": today.hour}
        loggers(f"EVENT\t{low_balance.__name__}\t LOW BALANCE {SERVICE_NAME}", 2)  # log

        def send_worn():
            global REQ_JSON
            """ Отправляет сообщение на номер владельца сервиса """
            text = f"Низкий уровень баланса: {balance} на сервисе {SERVICE_NAME}"
            req = requests.get(f"https://sms.ru/sms/send?api_id={ID_USER}&to={PHONE_NUMBER}&msg={text}&json=1")
            REQ_JSON = req.json()

        with open(f"./balance_worn.log", 'w') as file:
            json.dump(json_mess, file)

        file_date = dict()
        with open(f"./balance_worn.log", 'r') as file:
            file_date = json.load(file)

        if file_date["month"] != json_mess["month"]:
            send_worn()  # функция отправки сообщения о низком балансе
            with open(f"./balance_worn.log", 'w') as file:
                json.dump(json_mess, file)
        elif file_date["day"] != json_mess["day"]:
            send_worn()  # функция отправки сообщения о низком балансе
            with open(f"./balance_worn.log", 'w') as file:
                json.dump(json_mess, file)
        elif json_mess["time"] >= 10 and FLAG_MIN_BAL:
            if json_mess["time"] <= 19:
                send_worn()  # функция отправки сообщения о низком балансе
                FLAG_MIN_BAL = False
                with open(f"./balance_worn.log", 'w') as file:
                    json.dump(json_mess, file)
        else:
            loggers(f"EVENT\t{low_balance.__name__}\t The alert has already been sent to {PHONE_NUMBER}", 2)  # log
    else:
        FLAG_MIN_BAL = True


def take_balance():
    global BALANCE_SMS_SERVICE
    global SERVICE_NAME
    global TAKE_BALANCE_URL
    global LOW_BALANCE
    try:
        req = requests.get(TAKE_BALANCE_URL)
        j_info = req.json()
        BALANCE_SMS_SERVICE = j_info["balance"]
        loggers(f"EVENT\t{take_balance.__name__}\t Последний баланс {SERVICE_NAME} "  # last update balance
                f"= {BALANCE_SMS_SERVICE}", 2)  # log

        low_balance(BALANCE_SMS_SERVICE)  # Запускаем проверку на минимальный остаток

    except ImportError:
        loggers(f"ERROR\t{take_balance.__name__}\t can't update balance {SERVICE_NAME}", 1)  # log


def take_settings():
    global PORT
    global TAKE_BALANCE_URL
    global ID_USER
    global PATH_LOG
    global SERVICE_NAME
    global LOW_BALANCE
    global PHONE_NUMBER

    # загружаем файл settings.ini
    if not os.path.isfile("settings.ini"):
        loggers(f"ERROR\t{take_settings.__name__}\tfile settings.ini not found.", 1)
        raise FileExistsError

    config_set = configparser.ConfigParser()
    config_set.read("settings.ini")

    ID_USER = config_set["GENERAL"]["USER_ID"]
    PATH_LOG = config_set["GENERAL"]["PATH_LOG"]
    PORT = config_set["GENERAL"]["PORT"]
    SERVICE_NAME = config_set["GENERAL"]["SERVICE_NAME"]
    LOW_BALANCE = config_set["GENERAL"]["LOW_BALANCE"]
    PHONE_NUMBER = config_set["GENERAL"]["PHONE_NUMBER"]

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
    global REQ_JSON
    json_replay = {"RESULT": "SUCCESS", "DESC": "None", "DATA": "None"}

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
            json_replay["RESULT"] = "ERROR"
            json_replay["DESC"] = f"Error from answer {SERVICE_NAME}"
            log_status = 1

        loggers(f"{status_m}\t{index.__name__}\t Send to number {phone_num}\t text: {text}", log_status)  # log

        json_replay["DATA"] = REQ_JSON
        return json_replay

        # if it_url_param: return REQ_JSON else: return render_template("index.html", event_app=status_m)

    elif request.method == "GET":
        print(request.host)
        if os.path.isfile("./templates/index.html"):
            loggers(f"EVENT\t{index.__name__}\t send to client - index.html", 2)  # log
            return render_template("index.html")    # открываем страницу отправки сообщения
        else:
            loggers(f"ERROR\t{index.__name__}\t file index.html not found.", 1)
            return make_response(f"<h2>Error: 400, fail open file index.html</h2>")
    else:
        loggers(f"ERROR\t{index.__name__}\t Wrong address: {request.method}, {request.full_path}", 1)  # log
        return make_response("<h2>Error: {0}</h2>".format(400))   # открываем страницу отправки сообщения

# --------------------------------------------------------------------------


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 720)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 720))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(-1, 9, -1, -1)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(718, 45))
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
        self.start_but = QtWidgets.QPushButton(self.frame_2)
        self.start_but.setGeometry(QtCore.QRect(10, 0, 65, 39))
        self.start_but.setMinimumSize(QtCore.QSize(65, 39))
        self.start_but.setObjectName("start_but")
        self.horizontalLayout_2.addWidget(self.frame_2)
        self.frame_9 = QtWidgets.QFrame(self.frame)
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.clear_but = QtWidgets.QPushButton(self.frame_9)
        self.clear_but.setGeometry(QtCore.QRect(10, 0, 65, 39))
        self.clear_but.setMinimumSize(QtCore.QSize(65, 39))
        self.clear_but.setObjectName("clear_but")
        self.check_but = QtWidgets.QPushButton(self.frame_9)
        self.check_but.setGeometry(QtCore.QRect(80, 0, 65, 39))
        self.check_but.setMinimumSize(QtCore.QSize(65, 39))
        self.check_but.setObjectName("check_but")
        self.horizontalLayout_2.addWidget(self.frame_9)
        self.frame_8 = QtWidgets.QFrame(self.frame)
        self.frame_8.setMinimumSize(QtCore.QSize(120, 0))
        self.frame_8.setMaximumSize(QtCore.QSize(120, 16777215))
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_2.addWidget(self.frame_8)
        self.verticalLayout_2.addWidget(self.frame)
        self.stack_Window = QtWidgets.QStackedWidget(self.centralwidget)
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
        self.verticalLayout = QtWidgets.QVBoxLayout(self.log_window)
        self.verticalLayout.setObjectName("verticalLayout")
        self.text_logs = QtWidgets.QTextBrowser(self.log_window)
        self.text_logs.setMinimumSize(QtCore.QSize(715, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.text_logs.setFont(font)
        self.text_logs.setObjectName("text_logs")
        self.verticalLayout.addWidget(self.text_logs)
        self.stack_Window.addWidget(self.log_window)
        self.verticalLayout_2.addWidget(self.stack_Window)
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 35))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_status = QtWidgets.QLabel(self.frame_3)
        self.label_status.setObjectName("label_status")
        self.horizontalLayout_4.addWidget(self.label_status)
        self.verticalLayout_2.addWidget(self.frame_3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stack_Window.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.start_but.setText(_translate("MainWindow", "Start"))
        self.clear_but.setText(_translate("MainWindow", "Clear"))
        self.check_but.setText(_translate("MainWindow", "Check"))
        self.line_phone.setText(_translate("MainWindow", "+79991112233"))
        self.label_phone.setText(_translate("MainWindow", "Phone"))
        self.label_message.setText(_translate("MainWindow", "Message"))
        self.label_status.setText(_translate("MainWindow", "status:"))


# ----------------------------------------------------------------------------


class MainWindow(QtWidgets.QMainWindow):
    """ Запуск сервера Фласк происходит в функйии thread_flask() """
    def thread_flask(self):
        print("Hallo i'm Flask")
        app.run(debug=False, host=HOST, port=int(PORT))

    tray_icon = None

    def __init__(self):
        super().__init__()
        print("Hallo i'm PyQt")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.thread_for_flask = threading.Thread(target=self.thread_flask, name="VIG_sms_server")

        self.setWindowTitle("VIG_sms_server")

        # tray_icon -------------------------------------------------
        self.tray_icon = QtWidgets.QSystemTrayIcon()
        # Create the icon
        icon = QtGui.QIcon("icon.png")
        self.tray_icon.setIcon(icon)  # self.style().standardIcon(QtWidgets.QStyle.SP_ComputerIcon))
        self.tray_icon.setToolTip("VIG sms sender")

        show_action = QtWidgets.QAction("Show", self)
        quit_action = QtWidgets.QAction("Exit", self)
        hide_action = QtWidgets.QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self.close_server)  # QtWidgets.qApp.quit)

        tray_menu = QtWidgets.QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        # -----------------------------------------------------------

        self.ui.check_but.clicked.connect(self.check_flask)

        # self.ui.change_but.clicked.connect(self.change_log_send)
        self.ui.clear_but.clicked.connect(self.clear_logs)

        self.ui.start_but.clicked.connect(self.run_flask)

    def close_server(self):
        if self.thread_for_flask.is_alive():  # проверяет наличие потока с сервером
            self.run_flask()  # повторный запуск вызывает остановку сервера, закрытие потока и программы
        else:
            sys.exit()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage("VIG_sms_sender", "App was min to Tray", QtWidgets.QSystemTrayIcon.Information, 10)

    def add_log(self, text_log):
        self.ui.text_logs.append(str(text_log))

    def clear_logs(self):
        self.ui.text_logs.clear()

    def run_flask(self):
        self.ui.start_but.setText("Exit")
        self.thread_for_flask.start()
        if self.thread_for_flask.is_alive():
            loggers(f"SUCCESS\tclass threadPyqt\tSTART SERVER")  # log
            self.ui.label_status.setText(f"status: Server status is {self.thread_for_flask.is_alive()}")
        else:
            loggers(f"ERROR\tclass threadPyqt\tSTART SERVER", 1)  # log

    def check_flask(self):
        self.ui.label_status.setText(f"status: Server status is {self.thread_for_flask.is_alive()}")
        take_balance()


if __name__ == "__main__":
    # подгружаем данные из файла settings
    take_settings()
    # получаем наш баланс
    app_gui = QtWidgets.QApplication(sys.argv)
    gui = MainWindow()

    ADD_LOG = gui  # делаем класс глобальным для получение доступа из других функция в методы класса

    gui.show()
    sys.exit(app_gui.exec())
    # запускаем сервер flask
