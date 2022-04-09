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


@bot.message_handler(commands=['start'])
def main_manu(message):
    print(message.chat.type)
    bot.send_message(message.chat.id, f'Вітаємо, {message.from_user.first_name}! Це головне меню.',
                     parse_mode='html', reply_markup=markups.main_menu)
