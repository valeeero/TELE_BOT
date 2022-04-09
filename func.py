def clear_list(args):
    for i in args:
        i.clear()


def send_message(bot, message, text):
    msg = bot.send_message(message.chat.id, f'{text}',
                           parse_mode='html')
    return msg


def send_message_with_markup(bot, message, text, markup):
    msg = bot.send_message(message.chat.id, f'{text}',
                           parse_mode='html', reply_markup=markup)
    return msg


def find_url(text):
    if text.find('https://drive-sport.com.ua/') == 0 or text.find('drive-sport.com.ua') == 0:
        return 0

    else:
        return 1
