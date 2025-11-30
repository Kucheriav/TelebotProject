from telebot import types


city_buttons = [types.KeyboardButton(x) for x in ['Калуга', 'Таруса', 'Боровск']]
city_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
city_markup.add(*city_buttons)

details_buttons = [types.InlineKeyboardButton(text=x, callback_data=x) for x in ['Кафе', 'Музеи', 'Парки']]
details_markup = types.InlineKeyboardMarkup()
details_markup.add(*details_buttons)


if __name__ == '__main__':
    print('sdasdasdsadasdasd')