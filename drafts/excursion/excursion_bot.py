import os
from csv import excel

import telebot
from dotenv import load_dotenv
from time import sleep
from typing import Dict

from my_markup import *
from user_data import *
from db_functions import *


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
    bot.send_message(message.chat.id, 'Привет! Хочешь узнать про экскурсии и записатся или посмотреть свои записи?', reply_markup=start_markup)

@bot.message_handler(commands=['cancel'])
def cancel(message):
    pass


@bot.message_handler(func=lambda m: True)
def router(message):
    pass

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    if call.data == 'У':
        res = select_all_excursions(DB_NAME)
        exc_buttons = [types.InlineKeyboardButton(text=x[1], callback_data=f'exc_id {x[0]}') for x in res]
        exc_markup = types.InlineKeyboardMarkup()
        exc_markup.add(*exc_buttons)
        bot.send_message(chat_id=call.message.chat.id, text='Выбирай!', reply_markup=exc_markup)
    elif call.data.startswith('exc_id '):
        id_ = int(call.data.split('exc_id ')[1])
        description = select_description_by_id(DB_NAME, id_)
        bot.send_message(chat_id=call.message.chat.id, text=description)
        dates = list(filter(lambda x: len(x[1]) > 0, select_dates_by_id(DB_NAME, id_)))
        if dates:
            date_buttons = [types.InlineKeyboardButton(text=x[1], callback_data=f'date_id {x[0]}') for x in dates]
            date_markup = types.InlineKeyboardMarkup()
            date_markup.add(*date_buttons)
            bot.send_message(chat_id=call.message.chat.id, text='Записывайся на дату!', reply_markup=date_markup)
        else:
            bot.send_message(chat_id=call.message.chat.id, text='Дат пока не объявлено, но вы можете записаться на другую экскурсию')
    elif call.data.startswith('date_id '):
        date_id = int(call.data.split('date_id ')[1])
        insert_user_in_excursion(DB_NAME, user_id, date_id)
        print(select_all_users(DB_NAME))




while True:
    try:
        bot.polling(none_stop=True)
    except Exception as _ex:
        print(_ex)
        sleep(15)