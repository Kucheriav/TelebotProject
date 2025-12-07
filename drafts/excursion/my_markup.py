from telebot import types


start_buttons = [types.InlineKeyboardButton(text=x, callback_data=x[0]) for x in ['Узнать и записаться', 'Посмотреть свои записи']]
start_markup = types.InlineKeyboardMarkup()
start_markup.add(*start_buttons)

details_buttons = [types.InlineKeyboardButton(text=x, callback_data=x) for x in ['Кафе', 'Музеи', 'Парки']]
details_markup = types.InlineKeyboardMarkup()
details_markup.add(*details_buttons)


if __name__ == '__main__':
    print('sdasdasdsadasdasd')