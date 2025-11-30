import os
import telebot
from dotenv import load_dotenv
from time import sleep
from typing import Dict

from my_markup import *
from user_data import *
from info_reader import *

load_dotenv()
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    print('Внимание: TELEGRAM_TOKEN не задан. Установите переменную окружения перед запуском.')
    exit()
else:
    bot = telebot.TeleBot(TOKEN)
    print('Bot object created')

user_data_dict: Dict[int, UserData] = {}
@bot.message_handler(commands=['start', 's'])
def start(message):
    user_data_dict[message.from_user.id] = UserData(user_id=message.from_user.id, state=State.ASK_CITY)
    bot.send_message(message.chat.id, 'Привет! Выбери свой город', reply_markup=city_markup)

@bot.message_handler(commands=['cancel'])
def cancel(message):
    hide_keyboard = types.ReplyKeyboardRemove()
    if message.from_user.id in user_data_dict:
        user_data_dict[message.from_user.id].state = State.NONE
        bot.send_message(message.chat.id, 'Сессия отменена.',reply_markup=hide_keyboard)
    else:
        bot.send_message(message.chat.id, 'Нажми старт', reply_markup=hide_keyboard)


@bot.message_handler(func=lambda m: True)
def router(message):
    user_id = message.from_user.id
    user_data = user_data_dict.get(user_id, UserData(state=State.NONE))
    if user_data.state == State.NONE:
        bot.send_message(message.chat.id, 'Нажми старт')
    elif user_data.state == State.ASK_CITY:
        city  = message.text.capitalize()
        bot.send_message(message.chat.id, f'{city}! Классный город!')
        user_data_dict[user_id].state = State.ASK_DETAILS
        user_data_dict[user_id].city = city
        bot.send_message(message.chat.id, 'Что бы ты хотел узнать про этот город?', reply_markup=details_markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    user_data = user_data_dict.get(user_id, UserData(state=State.NONE))
    if user_data.state == State.NONE:
        bot.send_message(call.chat.id, 'Нажми старт')
    elif user_data.state == State.ASK_DETAILS:
        this_info = all_info[user_data.city][call.data]
        bot.send_message(chat_id=call.message.chat.id, text=this_info)


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as _ex:
        print(_ex)
        sleep(15)