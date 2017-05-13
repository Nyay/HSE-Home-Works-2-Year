import telebot
import re
import urllib.request as ur
import requests
import conf
import random
import flask

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN_GURI)
bot = telebot.TeleBot(conf.TOKEN_GURI, threaded=False)
bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

weather_key = conf.WUNDERGROUND_KEY
added_cities = conf.ADDED_CITIES


def FtoC(text):
    try:
        Fr = int(text)
        Cl = (Fr - 32) / 2 + (Fr - 32) / 20
        return round(Cl, 1)
    except ValueError:
        result = re.search('(.*?)\.', text)
        Fr = int(result.group(1))
        Cl = (Fr - 32) / 2 + (Fr - 32) / 20
        return round(Cl, 1)


def html_search(code, reg, mid):
    try:
        url = 'https://www.wunderground.com' + code
        page = ur.urlopen(url)
        html_code = page.read().decode('UTF-8')
        item = re.search(reg, html_code)
        item = item.group(1)
        return item
    except AttributeError:
        bot.send_message(mid, 'Кто-то хочет меня обмануть :X')


def week2(d, period):
    d_exit = {}
    d_days = {'Monday': 'Понедельник',
              'Tuesday': 'Вторник',
              'Wednesday': 'Среда',
              'Thursday': 'Четверг',
              'Friday': 'Пятница',
              'Saturday': 'Суббота',
              'Sunday': 'Воскресенье'}
    d_month = {'January': 'Января',
               'February': 'Февраля',
               'March': 'Марта',
               'April': 'Апреля',
               'May': 'Мая',
               'June': 'Июня',
               'July': 'Июля',
               'August': 'Августа',
               'September': 'Сентября',
               'October': 'Октября',
               'November': 'Ноября',
               'December': 'Декабря'}
    d_exit['day'] = d_days[d['forecast']['simpleforecast']['forecastday'][period]['date']['weekday']]
    d_exit['month'] = d_month[d['forecast']['simpleforecast']['forecastday'][period]['date']['monthname']]
    d_exit['num'] = d['forecast']['simpleforecast']['forecastday'][period]['date']['day']
    d_exit['lc'] = d['forecast']['simpleforecast']['forecastday'][period]['low']['celsius']
    d_exit['hc'] = d['forecast']['simpleforecast']['forecastday'][period]['high']['celsius']
    d_exit['year'] = d['forecast']['simpleforecast']['forecastday'][period]['date']['year']
    d_exit['qpf'] = d['forecast']['simpleforecast']['forecastday'][period]['qpf_allday']['mm']
    return d_exit


@bot.message_handler(commands=['start'])
def welcome_cmd(message):
    bot.send_message(message.chat.id, 'Привет!\nМеня зовут Guri!\n'
                                      'Я молодой бот, который пока знает мало команд...\n'
                                      'И иногда косячит в орфографии...\n'
                                      'Но я очень стараюсь! >:3\n'
                                      'Ты скорее всего пришел попробовать узнать погоду...\n'
                                      'Тогда пропиши /help , чтобы узнать как все рабоатет ^^\n'
                                      'Если возникунт вопросы, пиши моему создателю @sorry_im_neet')
    print('Command /start complete')


@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(message.chat.id, 'Вот список известных мне (пока) команд:\n'
                                      '\n'
                                      '/weather Город - Погода в указанном городе на этот день.\n'
                                      'Название города нужно написать через пробел на английском языке.\n'
                                      'Пример запроса: "/weather Sochi"\n'
                                      'Просто "/weather" – погода будет показана для Москвы.\n'
                                      'Иногда, сайт с которым я работаю не распознает города. Такое быват.\n'
                                      'В таком случае, напиши моему создателю и он добавит этот город вручную.\n'
                                      '\n/count_words Текст – я посчитаю количество слов в тексте после команды.\n'
                                      'Пример запроса: "/count_words Привет, как дела?"\n'
                                      '\n/weather3 Город – Погода в указанном городе на три дня.\n'
                                      'Название города нужно написать через пробел на английском языке.\n'
                                      'Пример запроса: "/weather3 Sochi"\n'
                                      'Просто "/weather3" – погода будет показана для Москвы.\n')
    print('Command /help complete')


@bot.message_handler(commands=['weather'])
def weather_cmd(message):
    try:
        city = message.text
        mssg = city.split()
        city = mssg[1]
        print(city)
    except IndexError:
        bot.send_message(message.chat.id, 'Погода будет показана для Москвы')
        city = 'moscow'
    link_zmw = 'http://autocomplete.wunderground.com/aq?query=' + city
    print(link_zmw)
    response_zmw = requests.get(link_zmw)
    result_zmw = response_zmw.json()
    if city in added_cities:
        zmw = added_cities[city]
        location = city
    else:
        try:
            zmw = result_zmw['RESULTS'][0]['l']
            location = result_zmw['RESULTS'][0]['name']
        except IndexError:
            bot.send_message(message.chat.id, 'Не смогла найти город, напиши @sorry_im_neet, Чтобы он его добавил.')
    try:
        weather_now = html_search(zmw, '"temperature": (.*?),', message.chat.id)
        weather_now = FtoC(weather_now)
        feel_weather = html_search(zmw, '"feelslike": (.*?),', message.chat.id)
        feel_weather = FtoC(feel_weather)
        date = html_search(zmw, '"pretty": "(.*?)"', message.chat.id)
        link_forecast = 'http://api.wunderground.com/api/' + weather_key + '/forecast' + zmw + '.json'
        response_forecast = requests.get(link_forecast)
        result_forecast = response_forecast.json()
        forecast_max = str(result_forecast['forecast']['simpleforecast']['forecastday'][0]['high']['celsius'])
        forecast_min = str(result_forecast['forecast']['simpleforecast']['forecastday'][0]['low']['celsius'])
        wind_dir = str(result_forecast['forecast']['simpleforecast']['forecastday'][0]['avewind']['dir'])
        wind_speed = str(round(result_forecast['forecast']['simpleforecast']['forecastday'][0]['avewind']['kph']*1000/3600, 1))
        ex = str(result_forecast['forecast']['simpleforecast']['forecastday'][0]['qpf_allday']['mm'])
        reply = 'Weather in: ' + location + '\nfor(local time): ' + str(date) + '\nCertain temp: ' + str(weather_now) + 'C\nFeels like: ' + str(feel_weather) + 'C\nMax temp: ' + forecast_max + 'C\nMin temp: ' + forecast_min + 'C\nExpected rainfall: ' + ex + 'mm\nWind speed: ' + wind_speed + 'ms\nWind direction: ' + wind_dir
        bot.send_message(message.chat.id, reply)
    except UnboundLocalError:
        bot.send_message(message.chat.id, 'Ууууупс... Что-то пошло не так... Попробуй еще раз.')
    except KeyError:
        bot.send_message(message.chat.id, 'И это мне не нравится...')
    print('Command /weather complete')


@bot.message_handler(commands=['weather3'])
def threedaysweather(message):
    try:
        city = message.text
        mssg = city.split()
        city = mssg[1]
    except IndexError:
        bot.send_message(message.chat.id, 'Погода будет показана для Москвы')
        city = 'moscow'
    link_zmw = 'http://autocomplete.wunderground.com/aq?query=' + city
    response_zmw = requests.get(link_zmw)
    result_zmw = response_zmw.json()
    if city in added_cities:
        zmw = added_cities[city]
        location = city
    else:
        try:
            zmw = result_zmw['RESULTS'][0]['l']
            location = result_zmw['RESULTS'][0]['name']
        except IndexError:
            bot.send_message(message.chat.id, 'Не смогла найти город, напиши @sorry_im_neet, Чтобы он его добавил.')
    try:
        link_forecast = 'http://api.wunderground.com/api/' + weather_key + '/forecast' + zmw + '.json'
        response_forecast = requests.get(link_forecast)
        result_forecast = response_forecast.json()
        period_1 = week2(result_forecast, 1)
        day_1 = 'Прогноз на три дня в ' + location + '\n\n' + str(period_1['day']) + ' ' + str(period_1['num']) + ' ' + str(period_1['month']) + ' ' + str(period_1['year']) + '\nМакс. температура: ' + str(period_1['hc']) + 'C\nМин. температура: ' + str(period_1['lc']) + 'C\nОжидаемые осадки: ' + str(period_1['qpf']) + 'мм\n\n'
        period_2 = week2(result_forecast, 2)
        day_2 = str(period_2['day']) + ' ' + str(period_2['num']) + ' ' + str(period_2['month']) + ' ' + str(period_2['year']) + '\nМакс. температура: ' + str(period_2['hc']) + 'C\nМин. температура: ' + str(period_2['lc']) + 'C\nОжидаемые осадки: ' + str(period_2['qpf']) + 'мм\n\n'
        period_3 = week2(result_forecast, 3)
        day_3 = str(period_3['day']) + ' ' + str(period_3['num']) + ' ' + str(period_3['month']) + ' ' + str(period_3['year']) + '\nМакс. температура: ' + str(period_3['hc']) + 'C\nМин. температура: ' + str(period_3['lc']) + 'C\nОжидаемые осадки: ' + str(period_3['qpf']) + 'мм\n\n'
        reply = day_1 + day_2 + day_3
        bot.send_message(message.chat.id, reply)
    except UnboundLocalError:
        bot.send_message(message.chat.id, 'Ууууупс... Что-то пошло не так... Попробуй еще раз.')
    except KeyError:
        bot.send_message(message.chat.id, 'И это мне не нравится...')
    print('Command /weather3 complete')


@bot.message_handler(commands=['count_words'])
def count_words(message):
    text = message.text
    text = re.sub('[,.!?;:@#$%^&)(*]', ' ', text)
    text = text.split()
    number = len(text) - 1
    bot.send_message(message.chat.id, 'В вашем предложении ' + str(number) + ' слов!... Вроде... :3')


@bot.message_handler(content_types=['text'])
def say_hello(message):
    replies = ['Hi!', 'Ciao!', 'Tuturuuu', 'Охаё', 'Konnichiwa!', 'Hisashiburi desu!', 'Moshi-moshi...', 'Yahhoo']
    entries = ['hello', 'Hello', 'Hey', 'hey', 'Хей', 'хей', 'Прив', 'прив']
    text = message.text
    for variant in entries:
        if text.startswith(variant):
            reply = random.choice(replies)
            bot.send_message(message.chat.id, str(reply))
            print('Command /say_hello сработала')


@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
