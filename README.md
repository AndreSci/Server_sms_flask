# Server_sms_flask
Для отправки смс нужно зарегестрироваться на сайте SMS.RU
добавить в settings.ini свой id с сайта в переменную USER_ID
установить нужный вам порт в settings.ini в переменную PORT
доступ к веб-версии чере local:8080\sendsms\
или через POST запросы с параметрами fphone = your_phone_number и ftext = your_text
ответом присылает json копию ответа с сайта SMS.RU
