import telebot
import config
import button_names as btn
from telebot import types

bot = telebot.TeleBot(config.TOK)


# Name for buttons


@bot.message_handler(commands=['start'])
def website(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    order_button = types.KeyboardButton(btn.order)
    contact_button = types.KeyboardButton(btn.contact)
    exist_button = types.KeyboardButton(btn.exist)
    complaints_button = types.KeyboardButton(btn.complaints)

    markup.add(order_button, contact_button, exist_button, complaints_button)
    msg = bot.send_message(message.chat.id,
                           f'Вітаємо, {message.from_user.first_name}! Це головне меню.',
                           reply_markup=markup)
    bot.register_next_step_handler(msg, url_order)


def url_order(message):
    if message.text == btn.order:
        msg = bot.send_message(message.chat.id, f'Введіть {btn.url.lower()}', parse_mode='html')
        bot.register_next_step_handler(msg, size_order)


def size_order(message):
    msg = bot.send_message(message.chat.id, f'Введіть {btn.size.lower()}(якщо він є)', parse_mode='html')
    bot.register_next_step_handler(msg, color_order)


def color_order(message):
    msg = bot.send_message(message.chat.id, f'Введіть {btn.color.lower()}(якщо він є)', parse_mode='html')
    bot.register_next_step_handler(msg, req_to_order)


def req_to_order(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    yes_button = types.KeyboardButton(btn.yes)
    no_button = types.KeyboardButton(btn.no)
    markup.add(yes_button, no_button)

    msg = bot.send_message(message.chat.id, f'Бажаєте додати ще одну позицію?', parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(msg, otv)


def otv(message):
    if message.text == 'yes':
        msg = bot.send_message(message.chat.id, f'Введіть {btn.url.lower()}', parse_mode='html')
        bot.register_next_step_handler(msg, size_order)
    else:
        pass


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    mess = message.text
    if message.chat.type == 'private':
        # if mess == btn.order:
        #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        #     url_product = types.KeyboardButton(btn.url)
        #     # size_product = types.KeyboardButton('Розмір')
        #     # color_product = types.KeyboardButton('Колір')
        #     back = types.KeyboardButton(btn.main_manu)
        #
        #     markup.add(url_product, back)
        #
        #     bot.send_message(message.chat.id, btn.order, reply_markup=markup)
        # if mess == btn.url:
        #     bot.send_message(message.chat.id, f'Введіть {btn.url.lower()}', parse_mode='html')
        # elif "https://drive-sport.com.ua" in mess:
        #     bot.send_message(message.chat.id, 'https://drive-sport.com.ua', parse_mode='html')
        if mess == btn.contact:

            bot.send_message(message.chat.id, f'<b>Наші контакти!</b>\n'
                                              f'Телефони:\n'
                                              f'+380487777777 або +380488888888\n'
                                              f'Адресса:\n'
                                              f'вул. Балківська 199,\n'
                                              f'магазин "Драйв-Спорт"', parse_mode='html')
        elif mess == btn.main_manu:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            order_button = types.KeyboardButton(btn.order)
            contact_button = types.KeyboardButton(btn.contact)
            exist_button = types.KeyboardButton(btn.exist)
            complaints_button = types.KeyboardButton(btn.complaints)
            markup.add(order_button, contact_button, exist_button, complaints_button)

            bot.send_message(message.chat.id, btn.main_manu, reply_markup=markup)


#
#         table(client/product),
#         id=None,
#         full_name=None, phone_number=None, city=None, np_point=None,
#          client_id=None, number_order=None, size=None, color=None, url=None
#

# create_object('client', 4, 'Melnik Anastasia Vladimirovna', '+380505005050', 'Odessa', '90')

# @bot.message_handler()
# def get_user_text(message):
#     mess = message.text
#     if mess == 'Замовити':
#         bot.send_message(message.chat.id, f'<b>Для замовлення товару потрібно:</b>\n'
#                                           f'1. Скопіюйте ссилку на товар який хочете замовити\n'
#                                           f'2. Вкажіть розмір (якщо він є)\n'
#                                           f'3. Вкажіть колір (якщо він є)',
#                          parse_mode='html')
#
#     elif mess == 'id':
#         bot.send_message(message.chat.id, f'Your id: {message.from_user.id}', parse_mode='html')


# @bot.message_handler(commands=['order'])
# def order(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     url_product = types.KeyboardButton('Ссилка на товар')
#     size_product = types.KeyboardButton('Розмір')
#     color_product = types.KeyboardButton('Колір')
#
#     markup.add(url_product, size_product, color_product)
#     bot.send_message(message.chat.id, 'Замовлення', reply_markup=markup)


bot.polling(none_stop=True)
