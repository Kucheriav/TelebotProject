import os
from time import sleep

import telebot
from dotenv import load_dotenv
from telebot import types

from drafts_user_data import *

load_dotenv()
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    print('Внимание: TELEGRAM_TOKEN не задан. Установите переменную окружения перед запуском.')
    exit()
else:
    bot = telebot.TeleBot(TOKEN)
    print('Bot object created')

from typing import Dict

user_data_dict: Dict[int, UserDataDC] = {}

from drafts_markup import *
@bot.message_handler(commands=['start', 's'])
def start(message):
    user_data_dict[message.from_user.id] = UserDataDC(user_id=message.from_user.id)
    bot.send_message(message.chat.id,'Выбери свой город', reply_markup=city_markup)
    user_data_dict[message.from_user.id].state = State.ASK_CITY


@bot.message_handler(commands=['cancel'])
def cancel(message):
    hide_keyboard = types.ReplyKeyboardRemove()
    if message.from_user.id in user_data_dict:
        user_data_dict[message.from_user.id].state = State.NONE
        bot.send_message(message.chat.id, 'Сессия отменена.', reply_markup=hide_keyboard)
        bot.send_message(message.chat.id, 'Выбери свой город', reply_markup=city_markup)
    else:
        bot.send_message(message.chat.id, 'Нажми старт', reply_markup=hide_keyboard)


@bot.message_handler(func=lambda m: True)
def router(message):
    user_id = message.from_user.id
    user_data = user_data_dict.get(user_id,UserDataDC(state=State.NONE))
    if user_data.state == State.NONE:
        bot.send_message(message.chat.id, 'Нажми старт')
    elif user_data.state == State.ASK_CITY:
        city = message.text
        user_data_dict[user_id].city = city
        bot.send_message(message.chat.id, f'{city}! Какой прекрасный город!')
        bot.send_message(message.chat.id, 'Чтобы ты хотел узнать про этот город?', reply_markup=details_markup)
        user_data_dict[user_id].state = State.ASK_DETAILS
    elif user_data.state == State.ASK_DETAILS:
        print(message.data)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    user_data = user_data_dict.get(user_id, UserDataDC(state=State.NONE))
    if user_data.state == State.NONE:
        bot.send_message(chat_id=call.message.chat.id, text='Нажми старт')
    if user_data.state == State.ASK_DETAILS:
        # bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Нажмите позже!")
        bot.send_message(chat_id=call.message.chat.id,  text="АГА")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="АГА АГА АГА АГА",
            reply_markup=None
        )


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as _ex:
        print(_ex)
        sleep(15)