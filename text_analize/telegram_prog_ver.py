import telebot
import time
import mystem_bot_module

TOKEN = ''

bot = telebot.TeleBot(TOKEN)
bot.remove_webhook()


@bot.message_handler(commands=['start'])
def welcome_cmd(message):
    bot.send_message(message.chat.id, 'Привет!\n'
                                      'Я бот, которвй отвечает предложением, в котором все слова заменены на '
                                      'какие-то случайные другие слова той же части речи и с теми же грамматическими'
                                      ' характеристиками.\n'
                                      'Проверьте, что в одной папке с ботом находится база данных "lemmas_plus.db"'
                                      ' и  модуль "mystem_bot_module.py"')
    print('Command /start complete')
    time.sleep(5)


@bot.message_handler(content_types=['text'])
def create_reply(message):
    text = message.text
    bot.send_message(message.chat.id, 'Работа программы займет некоторое время. Не пишите новые сообзения,'
                                      ' пока процесс не закончится. Если я замечу несколько возможных разборов'
                                      ' одного слова, то в скобках укажу выбранную мной форму.')
    reply = mystem_bot_module.mystem_bot_module(text)
    print(reply)
    bot.send_message(message.chat.id, reply)
    time.sleep(5)

if __name__ == '__main__':
    bot.polling(none_stop=True)
