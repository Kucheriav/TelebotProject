from telebot import types
from db_orm import ExcursionDate, ExcursionName
import datetime
start_buttons = [types.InlineKeyboardButton(text=x, callback_data=x[0]) for x in ['Узнать и записаться', 'Посмотреть свои записи']]
start_markup = types.InlineKeyboardMarkup()
start_markup.add(*start_buttons)


def get_excursions_markup(data: list[ExcursionName]):
    exc_buttons = [types.InlineKeyboardButton(text=x.name, callback_data=f'exc_id {x.id}') for x in data]
    exc_markup = types.InlineKeyboardMarkup()
    exc_markup.add(*exc_buttons)
    return exc_markup

def get_dates_markup(dates: list[ExcursionDate]):
    print(dates)
    date_buttons = [types.InlineKeyboardButton(text=x.date.strftime('%d.%m.%Y'), callback_data=f'date_id {x.id}') for x in dates]
    date_markup = types.InlineKeyboardMarkup()
    date_markup.add(*date_buttons)
    return date_markup

if __name__ == '__main__':
    print('sdasdasdsadasdasd')