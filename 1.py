import requests
import telebot
import pyowm
import datetime

TOKEN = '768137199:AAGXWne0nA34opJaUnF9gHH2vvCml9IK_Pc'
bot = telebot.TeleBot(TOKEN)
owm = pyowm.OWM('287d106e82e8ee499118c16c688e1752', language = "ru")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Бот позволяет узнать погоду по названию города")

@bot.message_handler(content_types=['text'])
def send_message(message):

    gorod = message.text 
    s_city = gorod
    city_id = 0
    appid = "287d106e82e8ee499118c16c688e1752"
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                     params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]

        bot.send_message(message.chat.id, cities)
        city_id = data['list'][0]['id']

        observation = owm.weather_at_place(s_city)
        w = observation.get_weather()
        temp = w.get_temperature('celsius') ["temp"]
        wind = w.get_wind()   ["speed"]
        humidity = w.get_humidity()
        time = w.get_reference_time()
        value = datetime.datetime.fromtimestamp(time)

        answer =  "В городе " + message.text + " следующие погодные условия: " + "\n"
        answer += "Температура: " + str( temp) + " C" + "\n"
        answer += "Скорость ветра: " + str( wind) + " м/с" + "\n"
        answer += "Влажность: " + str( humidity) + " относительных едениц" + "\n"
        answer += "Сейчас на улице: " + w.get_detailed_status() + "\n"
        answer += "Данные на  " + str(value) 

        bot.send_message(message.chat.id, answer)
    except Exception as e:
        Error = "Я думаю, " + "'" +str(message.text) + "'" + " не является городом {*_*}"
        bot.send_message(message.chat.id, Error)
        pass

bot.polling()