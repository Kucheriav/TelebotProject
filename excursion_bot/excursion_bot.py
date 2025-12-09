import os
import telebot
from dotenv import load_dotenv
from time import sleep

from my_markup import *
from db_orm import *


load_dotenv()

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    print('Внимание: TELEGRAM_TOKEN не задан. Установите переменную окружения перед запуском.')
    exit()
else:
    bot = telebot.TeleBot(TOKEN)
    print('Bot object created')


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
    if call.data.startswith('У'):
        res = select_all_excursions()
        bot.send_message(chat_id=call.message.chat.id, text='Выбирай!', reply_markup=get_excursions_markup(res))
    elif call.data.startswith('exc_id'):
        id_ = int(call.data.split()[1])
        description = select_description_by_id(id_)
        bot.send_message(chat_id=call.message.chat.id, text=description)
        dates = select_dates_by_id(id_)
        if dates:
            bot.send_message(chat_id=call.message.chat.id, text='Записывайся на дату!', reply_markup=get_dates_markup(dates))
        else:
            bot.send_message(chat_id=call.message.chat.id,
                             text='Дат пока не объявлено, но вы можете записаться на другую экскурсию')
    elif call.data.startswith('date_id'):
        id_ = int(call.data.split()[1])
        insert_user_in_excursion(user_id, id_)
        bot.send_message(chat_id=call.message.chat.id,
                         text='Ура, вы записаны!')
        print(select_all_users())
    elif call.data.startswith('П'):
        data = select_user_excursion(user_id)
        data = '\n'.join([f'{x[0]}: {x[1].strftime('%d.%m.%Y')}' for x in data])
        bot.send_message(chat_id=call.message.chat.id, text=f'Вы записаны на:\n{data}')



while True:
    try:
        bot.polling(none_stop=True)
    except Exception as _ex:
        print(_ex)
        sleep(15)