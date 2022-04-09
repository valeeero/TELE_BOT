import button_names as btn
from telebot import types

# -Main Menu

order_button = types.KeyboardButton(btn.order)
contact_button = types.KeyboardButton(btn.contact)
exist_button = types.KeyboardButton(btn.exist)
complaints_button = types.KeyboardButton(btn.complaints)
main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(order_button, contact_button, exist_button,
                                                                             complaints_button)

# -Back to main menu

back_to_menu_button = types.KeyboardButton(btn.m_m)
back_to_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(back_to_menu_button)

# -Back to main menu + phone number

phone_number = types.KeyboardButton(btn.phone, request_contact=True)
back_and_phone = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(back_to_menu_button, phone_number)

# -Back to main menu + enter city

city = ['Одеса', 'Київ', 'Дніпро', 'Суми', 'Харків', 'Львов', 'Івано-франківськ', 'Кривий ріг', 'Вінниця']
back_and_enter_city = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(*city, back_to_menu_button)

# -Back to main menu + continue

next_point = types.KeyboardButton(btn.next_point)
back_and_next = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(next_point, back_to_menu_button)

# -Yes or no

yes_no = [btn.yes, btn.no]
yes_or_no = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                      row_width=2,
                                      one_time_keyboard=True).add(*yes_no, back_to_menu_button)
