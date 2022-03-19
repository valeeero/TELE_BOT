import telebot
import config
import button_names as btn
from telebot import types
import urlextract

bot = telebot.TeleBot(config.TOK)
extractor = urlextract.URLExtract()

# Name for buttons
dict_values = {}


@bot.message_handler(commands=['start'])
def main_manu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    order_button = types.KeyboardButton(btn.order)
    contact_button = types.KeyboardButton(btn.contact)
    exist_button = types.KeyboardButton(btn.exist)
    complaints_button = types.KeyboardButton(btn.complaints)

    markup.add(order_button, contact_button, exist_button, complaints_button)
    bot.send_message(message.chat.id,
                     f'Вітаємо, {message.from_user.first_name}! Це головне меню.',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def enter(message):
    mess = message.text
    if mess == btn.order:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        mm = types.KeyboardButton(btn.m_m)
        markup.add(mm)
        msg = bot.send_message(message.chat.id, f'Введіть {btn.url.lower()}', parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(msg, size_order)
    elif mess == btn.contact:
        bot.send_message(message.chat.id, f'<b>Наші контакти!</b>\n'
                                          f'Телефони:\n'
                                          f'+380487777777 або +380488888888\n'
                                          f'Адресса:\n'
                                          f'вул. Балківська 199,\n'
                                          f'магазин "Драйв-Спорт"', parse_mode='html')
    # elif mess == btn.m_m:
    #     msg = bot.send_message(message.chat.id, f'Main manu', parse_mode='html')
    #     bot.register_next_step_handler(msg, main_manu)
    else:
        # if mess == btn.m_m:
        #     msg = bot.send_message(message.chat.id, f'Main manu', parse_mode='html')
        #     bot.register_next_step_handler(msg, main_manu)
        bot.register_next_step_handler(
            bot.send_message(message.chat.id, f'Виберіть одну з кнопок', parse_mode='html'), main_manu)


def size_order(message):
    if message.text == btn.m_m:
        msg = bot.send_message(message.chat.id, f'Main manu', parse_mode='html')
        bot.register_next_step_handler(msg, main_manu)
    elif len(extractor.find_urls(message.text)) > 0:
        dict_values[btn.url] = message.text
        msg = bot.send_message(message.chat.id, text=f'Введіть {btn.size.lower()}(якщо він є)', parse_mode='html')
        bot.register_next_step_handler(msg, color_order)
    else:
        msg = bot.send_message(message.chat.id,
                               f'Це не є посилання, будь ласка введіть {btn.url.lower()}'
                               , parse_mode='html')
        bot.register_next_step_handler(msg, size_order)


def color_order(message):
    dict_values[btn.size] = message.text
    msg = bot.send_message(message.chat.id, f'Введіть {btn.color.lower()}(якщо він є)', parse_mode='html')
    bot.register_next_step_handler(msg, req_to_order)
    # if message.text == btn.m_m:
    #     msg = bot.send_message(message.chat.id, f'Main manu', parse_mode='html')
    #     bot.register_next_step_handler(msg, main_manu)


def req_to_order(message):
    # if message.text.chat.type == 'private':
    dict_values[btn.color] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    yes_button = types.KeyboardButton(btn.yes)
    no_button = types.KeyboardButton(btn.no)
    markup.add(yes_button, no_button)

    msg = bot.send_message(message.chat.id, f'Бажаєте додати ще одну позицію?', parse_mode='html',
                           reply_markup=markup)
    bot.register_next_step_handler(msg, otv)


def otv(message):
    # if message.text.chat.type == 'private':
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back = types.KeyboardButton(btn.m_m)
    markup.add(back)
    if message.text == 'yes':
        msg = bot.send_message(message.chat.id, f'Введіть {btn.url.lower()}', parse_mode='html')
        bot.register_next_step_handler(msg, size_order)
    else:
        msg = bot.send_message(message.chat.id, f'Тепер потрібно вказати ваші контакти для оформлення рахунку.'
                                                f' Введіть ПІБ', parse_mode='html')
        bot.register_next_step_handler(msg, client_name)


def client_name(message):
    # if message.text.chat.type == 'private':
    dict_values['ПІБ'] = message.text
    msg = bot.send_message(message.chat.id, f'Введіть номер телефону', parse_mode='html')
    bot.register_next_step_handler(msg, client_phone)


def client_phone(message):
    # if message.text.chat.type == 'private':
    dict_values['Номер телефону'] = message.text
    msg = bot.send_message(message.chat.id, f'Введіть місто', parse_mode='html')
    bot.register_next_step_handler(msg, client_city)


def client_city(message):
    # if message.text.chat.type == 'private':
    dict_values['Місто'] = message.text
    msg = bot.send_message(message.chat.id, f'Введіть відділення НП', parse_mode='html')
    bot.register_next_step_handler(msg, client_np)


def client_np(message):
    # if message.text.chat.type == 'private':
    dict_values['НП'] = message.text
    msg = bot.send_message(message.chat.id, f'''Дякуємо за замовлення! У найближчий час наші працівники перевірять наявність товару та відправлять вам рахунок-фактуру на оплату.
            Ось ваше замовлення:
            Товар(посилання) - {dict_values[btn.url]}\n
            Розмір - {dict_values[btn.size]}\n
            Кольор - {dict_values[btn.color]}\n
            ПІБ - {dict_values['ПІБ']}\n
            Номер телефону - {dict_values['Номер телефону']}\n
            Місто - {dict_values['Місто']}\n
            Відділення НП - {dict_values['НП']}\n
                                                ''', parse_mode='html')
    bot.register_next_step_handler(msg, main_manu)
    print(dict_values)


# if mess.chat.type == 'private':


# def url_order(message):
#     # if message.text.chat.type == 'private':
#     if message.text == btn.order:
#         msg = bot.send_message(message.chat.id, f'Введіть {btn.url.lower()}', parse_mode='html')
#         bot.register_next_step_handler(msg, size_order)
#     else:
#         bot.register_next_step_handler(
#             bot.send_message(message.chat.id, f'Натисніть кнопку', parse_mode='html'),
#             url_order)


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
