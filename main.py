import os
import telebot
from dotenv import load_dotenv
from time import sleep

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
    print(1)
    bot.send_message(message.chat.id, 'hello')


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as _ex:
        print(_ex)
        sleep(15)


