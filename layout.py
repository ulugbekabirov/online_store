from aiogram import types
import emoji
radio_button = emoji.emojize(':radio_button:')
white_circle = emoji.emojize(':white_circle:')
menu_keyboard = ["О нас","Наш адрес","Связь с нами","Заказать матрас","Прайс лист"]
density_keyboard = ["Средняя","Максимальная", "Назад", "Главное меню"]
material_keyboard = ["Синтетика","Жаккард", "Назад", "Главное меню"]
size_keyboard = ["Односпалные","Полуторные","Двуспальные", "Назад", "Главное меню"]


class KeyboardBuilder():
	
    def __init__(self, buttons, one_time = False, width = 3):
        self.keyboard = types.ReplyKeyboardMarkup(row_width = width,resize_keyboard=True, one_time_keyboard = one_time)
        for button in buttons:
        	self.keyboard.insert(types.KeyboardButton(text=button))

    

