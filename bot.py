from config import *
import logging
from aiogram import Bot, Dispatcher, executor, types
import text 
from db import RedisStates
from layout import *
import utils

db = RedisStates(host=host_name,port =port_number ,db=db_number)
bot = Bot(token=token_name)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)





@dp.message_handler(commands = ["start"])
async def start(message: types.Message):
    db.setState(message.from_user.id, States.State_One.value)
    markup = KeyboardBuilder(menu_keyboard)
    await message.answer("Добро пожаловать", reply_markup=markup.keyboard) 


@dp.message_handler(lambda message: message.text == "О нас")
async def send_welcome(message: types.Message):
    await message.reply(text.about_us,parse_mode="Markdown")



@dp.message_handler(lambda message: message.text == "Наш адрес")
async def send_adress(message: types.Message):
    await message.reply(text.adress,parse_mode="Markdown")
    await bot.send_location(message.from_user.id, 41.397597,69.185315)


@dp.message_handler(lambda message: message.text == "Связь с нами")
async def send_contact(message: types.Message):
    await bot.send_photo(message.from_user.id,utils.contact_us)
    await message.reply(text.contact_us)


@dp.message_handler(lambda message: message.text == "Прайс лист")
async def send_price(message: types.Message):
    await message.reply(text.price_list)

@dp.message_handler(lambda message: message.text == "Заказать матрас",lambda message: db.getState(message.from_user.id)==States.State_One.value)
async def StateOne(message: types.Message):
    db.setState(message.from_user.id,States.State_Two.value)
    markup = KeyboardBuilder(density_keyboard, width = 2)
    await bot.send_photo(message.from_user.id, utils.preview, caption = text.preview)
    await message.answer(text.choose_density,reply_markup=markup.keyboard)
    

@dp.message_handler(lambda message: db.getState(message.from_user.id)==States.State_Two.value,content_types=types.ContentTypes.TEXT)
async def StateTwo(message: types.Message):
    if message.text in ["Средняя","Максимальная"]:
        db.setDensity(message.from_user.id, message.text)
        markup = KeyboardBuilder(material_keyboard, width=2)
        db.setState(message.from_user.id,States.State_Three.value)
        await message.answer("Выберите обивку:")
        await message.answer(text.choose_material,reply_markup=markup.keyboard)
    elif message.text=="Назад" or message.text=="Главное меню":
        db.setState(message.from_user.id, States.State_One.value)
        markup = KeyboardBuilder(menu_keyboard)
        await message.answer("Добро пожаловать",reply_markup=markup.keyboard) 
    else:
        await message.reply("Непонятно! Используй клавиатуру")
        return 

    

@dp.message_handler(lambda message: db.getState(message.from_user.id)==States.State_Three.value,content_types=types.ContentTypes.TEXT)
async def StateThree(message: types.Message):
    if message.text == "Жаккард":
        for id, photo in utils.jaccard.items():
            inline_button = types.InlineKeyboardButton("Выбрать", callback_data='{}'.format(id))
            markup = types.InlineKeyboardMarkup().add(inline_button)
            await bot.send_photo(message.from_user.id, photo, reply_markup = markup)        
    elif message.text == "Синтетика":
        for id, photo in utils.sintetica.items():
            inline_button = types.InlineKeyboardButton("Выбрать", callback_data='{}'.format(id))
            markup = types.InlineKeyboardMarkup().add(inline_button)
            await bot.send_photo(message.from_user.id, photo, reply_markup = markup)
    elif message.text=="Главное меню":
        db.setState(message.from_user.id, States.State_One.value)
        markup = KeyboardBuilder(menu_keyboard)
        await message.answer("Добро пожаловать",reply_markup=markup.keyboard) 
    elif message.text=="Назад":
        db.setState(message.from_user.id,States.State_Two.value)
        markup = KeyboardBuilder(density_keyboard, width = 2)
        await bot.send_photo(message.from_user.id, utils.preview, caption = text.preview)
        await message.answer(text.choose_density,reply_markup=markup.keyboard)
    else:
        await message.reply("Непонятно! Используй клавиатуру")
        return 


@dp.callback_query_handler(lambda call: db.getState(call.from_user.id)==States.State_Three.value and call.data.startswith('sint'))
async def ChooseImageFromInline(call: types.CallbackQuery):
    db.setImage(call.from_user.id, call.data)
    db.setMaterial(call.from_user.id, "Синтетика")
    await bot.answer_callback_query(call.id,"Выбрано")
    markup = KeyboardBuilder(size_keyboard,one_time = True)
    db.setState(call.from_user.id,States.State_Four.value)
    await bot.send_message(call.from_user.id, "Выберите размер",reply_markup=markup.keyboard)


@dp.callback_query_handler(lambda call: db.getState(call.from_user.id)==States.State_Three.value and call.data.startswith('jacc'))
async def ChooseImageFromInline(call: types.CallbackQuery):
    db.setImage(call.from_user.id, call.data)
    db.setMaterial(call.from_user.id, "Жаккард")
    await bot.answer_callback_query(call.id, "Выбрано")
    markup = KeyboardBuilder(size_keyboard, one_time = True)
    db.setState(call.from_user.id,States.State_Four.value)
    await bot.send_message(call.from_user.id, "Выберите размер",reply_markup=markup.keyboard)


@dp.message_handler(lambda message: db.getState(message.from_user.id)==States.State_Four.value,content_types=types.ContentTypes.TEXT)
async def StateFour(message: types.Message):
    if message.text == "Двуспальные":
        markup = types.InlineKeyboardMarkup()
        for button in utils.double_size:
            inline_button = types.InlineKeyboardButton(text = button, callback_data=button)
            markup.add(inline_button)

        await message.answer("Доступные Двуспальные размеры:",reply_markup = markup)

    elif message.text == "Односпалные":
        markup = types.InlineKeyboardMarkup()
        for button in utils.single_size:
            inline_button = types.InlineKeyboardButton(text = button, callback_data=button)
            markup.add(inline_button)

        await message.answer("Доступные Односпалные размеры:",reply_markup = markup)

    elif message.text == "Полуторные":
        markup = types.InlineKeyboardMarkup()
        for button in utils.medium_size:
            inline_button = types.InlineKeyboardButton(text = button, callback_data=button)
            markup.add(inline_button)

        await message.answer("Доступные Полуторные размеры",reply_markup = markup)

    elif message.text == "Главное меню":
        db.setState(message.from_user.id, States.State_One.value)
        markup = KeyboardBuilder(menu_keyboard)
        await message.answer("Добро пожаловать",reply_markup=markup.keyboard) 
    elif message.text == "Назад":
        db.setState(message.from_user.id, States.State_Three.value)
        markup = KeyboardBuilder(material_keyboard,width =2)
        await message.answer("Выберите обивку:",reply_markup=markup.keyboard)
    else:
        await message.reply("Непонятно! Используй клавиатуру")
        return 

    

@dp.callback_query_handler(lambda call: db.getState(call.from_user.id)==States.State_Four.value)
async def ChooseDimentions(call: types.CallbackQuery):
    if call.data in utils.single_size:
        db.setSize(call.from_user.id, "Односпалные")
        db.setDimentions(call.from_user.id,call.data)
       
    elif call.data in utils.medium_size:
        db.setSize(call.from_user.id, "Полуторные")
        db.setDimentions(call.from_user.id,call.data)

    elif call.data in utils.double_size:
        db.setSize(call.from_user.id, "Двуспальные")
        db.setDimentions(call.from_user.id,call.data)
    else:
        await bot.answer_callback_query(call.id, "Неверный ввод")
        return

    db.setState(call.from_user.id,States.State_Five.value)
    await bot.answer_callback_query(call.id, "Выбрано")  
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text="Да",callback_data = "Yes"),
                                        types.InlineKeyboardButton(text="Нет",callback_data = "No"))
    await bot.send_message(call.from_user.id, 
                    text.order_info.format(db.getDensity(call.from_user.id),
                                            db.getMaterial(call.from_user.id),
                                            db.getSize(call.from_user.id),
                                            db.getDimentions(call.from_user.id)),
                    reply_markup=markup)


@dp.callback_query_handler(lambda call: db.getState(call.from_user.id)==States.State_Five.value)
async def StateFive(call:types.CallbackQuery):
    if call.data == "Yes":
        db.setState(call.from_user.id, States.State_Six.value)
        await bot.answer_callback_query(call.id,text.make_order,show_alert = True)
        button1 = types.KeyboardButton("Отправить свои контакты",request_contact=True)
        button2 = types.KeyboardButton("Отмена")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,row_width = 1).add(button1,button2)
        await bot.send_message(call.from_user.id,text.make_order,reply_markup = markup)
    elif call.data == "No":
        await bot.answer_callback_query(call.id) 
        db.setState(call.from_user.id, States.State_One.value)
        markup = KeyboardBuilder(menu_keyboard)
        await bot.send_message(call.from_user.id,"Заказ отменен",reply_markup=markup.keyboard) 

    else:
        await bot.answer_callback_query(call.id,"Ответьте на заказ") 


@dp.message_handler(lambda message: db.getState(message.from_user.id)==States.State_Six.value,content_types=types.ContentTypes.TEXT)
async def StateSix(message: types.message):
    if message.text == "Отмена":
        db.setState(message.from_user.id, States.State_One.value)
        markup = KeyboardBuilder(menu_keyboard)
        await message.answer("Начнем занаво!",reply_markup=markup.keyboard) 
    else:
        await message.reply("Непонятно! Используй клавиатуру")
        return 



@dp.message_handler(lambda message: db.getState(message.from_user.id)==States.State_Six.value,content_types=types.ContentTypes.CONTACT)
async def ContactHandler(message: types.Message):
    await message.reply("Мы с вами свяжемся!")
    db.setState(message.from_user.id, States.State_One.value)
    markup = KeyboardBuilder(menu_keyboard)
    await message.answer("Переходим в главное меню!",reply_markup=markup.keyboard)
    for admin in admin_list:
        await bot.send_message(admin,text.admin_order_info.format(db.getDensity(message.from_user.id),
                                            db.getMaterial(message.from_user.id),
                                            db.getSize(message.from_user.id),
                                            db.getDimentions(message.from_user.id),
                                            message.contact.first_name,
                                            message.contact.phone_number))




@dp.message_handler(lambda message: message.text == "Главное меню")
async def MainMenu(message: types.Message):
    db.setState(message.from_user.id, States.State_One.value)
    markup = KeyboardBuilder(menu_keyboard)
    await message.answer("Добро пожаловать в Главное меню",reply_markup=markup.keyboard) 





@dp.callback_query_handler(lambda call: True)
async def defaultQueryHandler(call):
    await bot.answer_callback_query(call.id)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

