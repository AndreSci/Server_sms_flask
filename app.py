from flask import Flask, render_template, request, make_response
import configparser
import datetime
import requests
import os


app = Flask(__name__)  # создаем сервер flask

PATH_LOG = ''
HOST = '0.0.0.0'
PORT = 8000
BALANCE_SMS_SERVICE = 0
number_black = "+79991115544"
name_phone = "Andrew"
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

    config_set = configparser.ConfigParser()
    config_set.read("settings.ini")
    ID_USER = config_set["GENERAL"]["USER_ID"]
    PATH_LOG = config_set["GENERAL"]["PATH_LOG"]

    # создаем глобальную переменную содержащую url для запроса баланса
    TAKE_BALANCE_URL = "https://sms.ru/my/balance?api_id={0}&json=1".format(ID_USER)
    PORT = config_set["GENERAL"]["PORT"]

# тело обработки запросов http ------------------------------------------------------------


# https://sms.ru/sms/send?api_id=24EE3A41-98A6-A84F-13FF-85F6204E142A&to=79661140411,74993221627&msg=hello+world&json=1
# {'status': 'OK', 'status_code': 100, 'sms': {
# '79661140411': {'status': 'OK', 'status_code': 100, 'sms_id': '202216-1000005', 'cost': '0.00'}
# },
# 'balance': 112.1}
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
        loggers(f"SUCCESS\t{index.__name__}\tsend - index.html")  # log
        return render_template("index.html")    # открываем страницу отправки сообщения
    else:
        loggers(f"ERROR\t{index.__name__}\twrong address: {request.method}, {request.full_path}")  # log
        return make_response("<h2>Error: {0}</h2>".format(400))   # открываем страницу отправки сообщения

# -----------------------------------------------------------------------------------------


if __name__ == "__main__":
    # подгружаем данные из файла settings
    take_settings()
    # получаем наш баланс
    take_balance()
    # запускаем сервер flask
    app.run(debug=True, host=HOST, port=int(PORT))
