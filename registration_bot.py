import os
import telebot
from dotenv import load_dotenv
from time import sleep
from enum import Enum, auto

class State(Enum):
    NONE = auto()
    ASK_NAME = auto()
    ASK_AGE = auto()
    FINISHED = auto()

load_dotenv()
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    print('Внимание: TELEGRAM_TOKEN не задан. Установите переменную окружения перед запуском.')
    exit()
else:
    bot = telebot.TeleBot(TOKEN)
    print('Bot object created')

#user_id: {'name: ____, 'age': ____, 'state': _____}
user_data = {}
@bot.message_handler(commands=['start', 's'])
def start(message):
    user_data[message.from_user.id] = {}
    user_data[message.from_user.id]['state'] = State.ASK_NAME
    bot.send_message(message.chat.id, 'Давайте зарегистрируемся. Как вас зовут?')

@bot.message_handler(commands=['cancel'])
def cancel(message):
    if message.from_user.id in user_data:
        user_data[message.from_user.id].clear()
        user_data[message.from_user.id]['state'] = State.NONE
        bot.send_message(message.chat.id, 'Сессия отменена.')
    else:
        bot.send_message(message.chat.id, 'Нажми старт')


@bot.message_handler(func=lambda m: True)
def router(message):
    user_id = message.from_user.id
    data = user_data.get(user_id, {'state': State.NONE})
    if data['state'] == State.NONE:
        bot.send_message(message.chat.id, 'Нажми старт')
    elif data['state'] == State.ASK_NAME:
        user_data[message.from_user.id]['name'] = message.text
        user_data[message.from_user.id]['state'] = State.ASK_AGE
        bot.send_message(message.chat.id, 'Ваш возраст?')
    elif data['state'] == State.ASK_AGE:
        if message.text.isdigit():
            user_data[message.from_user.id]['age'] = int(message.text)
            user_data[message.from_user.id]['state'] = State.FINISHED
            bot.send_message(message.chat.id, 'Congrats!!!')
        else:
            bot.send_message(message.chat.id, 'Введите только число')


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as _ex:
        print(_ex)
        sleep(15)