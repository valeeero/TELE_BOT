import telebot
from phonenumbers import carrier, timezone, geocoder

import config
import markups
import button_names as btn
from telebot import types
import urlextract
import json
import values
import func
import phonenumbers

bot = telebot.TeleBot(config.TOK)
extractor = urlextract.URLExtract()
id_order = 1
kist = []
con = 0


@bot.message_handler(commands=['start'])
def main_manu(message):
    print(message.chat.type)
    bot.send_message(message.chat.id, f'Вітаємо, {message.from_user.first_name}! Це головне меню.',
                     parse_mode='html', reply_markup=markups.main_menu)


@bot.message_handler()
def chose_button(message):
    if message.chat.type == 'private':
        if message.text == btn.order:
            msg = bot.send_message(message.chat.id, f'Введіть {btn.url.lower()}',
                                   parse_mode='html', reply_markup=markups.back_to_menu)
            bot.register_next_step_handler(msg, order_size)
        elif message.text == btn.m_m:
            bot.send_chat_action(message.chat.id, action=main_manu(message))
        elif message.text == btn.contact:
            bot.send_message(message.chat.id, f'<b>Наші контакти!</b>\n'
                                              f'Телефони:\n'
                                              f'+380487777777 або +380488888888\n'
                                              f'Адресса:\n'
                                              f'вул. Балківська 199,\n'
                                              f'магазин "Драйв-Спорт"', parse_mode='html')
        else:
            print(message.text)


def order_size(message):
    if message.chat.type == 'private':
        if message.text == btn.m_m:
            bot.send_chat_action(message.chat.id, action=main_manu(message))
        elif func.find_url(message.text) == 0:
            values.list_url.append(message.text)
            msg = bot.send_message(message.chat.id,
                                   text=f'Введіть {btn.size.lower()}(якщо він є), або натисніть {btn.next_point}',
                                   parse_mode='html',
                                   reply_markup=markups.back_and_next)
            bot.register_next_step_handler(msg, order_color)
        elif func.find_url(message.text) == 1:
            msg = bot.send_message(message.chat.id,
                                   f'''
Це не є посилання нашого магазину. 
Приклад посилання "https://drive-sport.com.ua/goods/51516/971915". 
Введіть {btn.url.lower()}
'''
                                   , parse_mode='html')
            bot.register_next_step_handler(msg, order_size)


def order_color(message):
    if message.chat.type == 'private':
        if message.text == btn.next_point:
            values.list_size.append('-')
            msg = bot.send_message(message.chat.id,
                                   f'Введіть {btn.color.lower()}(якщо він є), або натисніть {btn.next_point}',
                                   parse_mode='html',
                                   reply_markup=markups.back_and_next)
            bot.register_next_step_handler(msg, chose_add_more_order)
        elif len(message.text) < 10:
            values.list_size.append(message.text)
            msg = bot.send_message(message.chat.id,
                                   f'Введіть {btn.color.lower()}(якщо він є), або натисніть {btn.next_point}',
                                   parse_mode='html',
                                   reply_markup=markups.back_and_next)
            bot.register_next_step_handler(msg, chose_add_more_order)
        elif message.text == btn.m_m:
            bot.send_chat_action(message.chat.id, action=main_manu(message))


def chose_add_more_order(message):
    if message.chat.type == 'private':
        if message.text == btn.m_m:
            bot.send_chat_action(message.chat.id, action=main_manu(message))
        elif message.text == btn.next_point:
            values.list_color.append('-')
            msg = bot.send_message(message.chat.id, f'Бажаєте додати ще одну позицію?', parse_mode='html',
                                   reply_markup=markups.yes_or_no)
            bot.register_next_step_handler(msg, otv)
        else:
            values.list_color.append(message.text)
            msg = bot.send_message(message.chat.id, f'Бажаєте додати ще одну позицію?', parse_mode='html',
                                   reply_markup=markups.yes_or_no)
            bot.register_next_step_handler(msg, otv)


def otv(message):
    if message.chat.type == 'private':
        if message.text == btn.yes:
            msg = bot.send_message(message.chat.id, f'Введіть {btn.url.lower()}', parse_mode='html',
                                   reply_markup=markups.back_to_menu)
            bot.register_next_step_handler(msg, order_size)
        elif message.text == btn.m_m:
            bot.send_chat_action(message.chat.id, action=main_manu(message))
        elif message.text == btn.no:
            url_to_tuple = []
            size_to_tuple = []
            color_to_tuple = []
            for i in values.list_url:
                url_to_tuple.append(i)
            for i in values.list_size:
                size_to_tuple.append(i)
            for i in values.list_color:
                color_to_tuple.append(i)
            values.client_order['id_order'] = con + 1
            values.client_order[message.from_user.username] = {
                f'{btn.url}': tuple(url_to_tuple),
                f'{btn.size}': tuple(size_to_tuple),
                f'{btn.color}': tuple(color_to_tuple)}
            with open('data.json', 'w') as file:
                json.dump(values.client_order, file)
                print("save file done")
            print(values.client_order)
            values.list_url.clear()
            values.list_size.clear()
            values.list_color.clear()
            msg = bot.send_message(message.chat.id, f'Тепер потрібно вказати ваші контакти для оформлення рахунку.'
                                                    f' Введіть ПІБ', parse_mode='html',
                                   reply_markup=markups.back_to_menu)
            bot.register_next_step_handler(msg, contact_name)


def contact_name(message):
    if message.chat.type == 'private':
        if message.text == btn.m_m:
            bot.send_chat_action(message.chat.id, action=main_manu(message))
        else:
            values.client_data['ПІБ'] = message.text
            msg = bot.send_message(message.chat.id,
                                   f'Введіть Ваш номер телефону в форматі +380-(**)-***-**-**, або натисніть кнопку "Поділитися контактом"',
                                   parse_mode='html',
                                   reply_markup=markups.back_to_menu)
            bot.register_next_step_handler(msg, contact_phone)


def contact_phone(message):
    if message.chat.type == 'private':
        print(message.text)
        if message.text == btn.m_m:
            bot.send_chat_action(message.chat.id, action=main_manu(message))
        else:
            try:
                print(phonenumbers.is_valid_number(message.text))
                print(carrier.name_for_number(message.text, "en"))
                print(timezone.time_zones_for_number(message.text))
                print(geocoder.description_for_number(message.text, 'en'))
            except:
                print("value is GOVNO")
            values.client_data['Телефон'] = message.text
            msg = bot.send_message(message.chat.id,
                                   f'Введіть місто (куди потрібно буде відправити товар), або оберіть з існуючих',
                                   parse_mode='html',
                                   reply_markup=markups.back_and_enter_city)
            bot.register_next_step_handler(msg, contact_city)


def contact_city(message):
    if message.chat.type == 'private':
        if message.text == btn.m_m:
            bot.send_chat_action(message.chat.id, action=main_manu(message))
        else:
            values.client_data['Місто'] = message.text
            msg = bot.send_message(message.chat.id,
                                   f'Введіть віділення Нової Пошти',
                                   parse_mode='html',
                                   reply_markup=markups.back_to_menu)
            bot.register_next_step_handler(msg, end_contact_add)


def end_contact_add(message):
    if message.chat.type == 'private':
        if message.text == btn.m_m:
            bot.send_chat_action(message.chat.id, action=main_manu(message))
        else:
            values.client_data['НП'] = message.text
            func.send_message(bot, message, "Дякуємо за замовлення!"
                                            f"Ваше замовлення {values.client_order[message.from_user.username]}")
            print(values.client_data)


bot.polling(none_stop=True, interval=0)
