import telebot
from telebot import types
from datetime import datetime, timedelta
from functions import*
from values import*
from threading import Timer
import config
from config import listener
from commercial import commercial_text


bot = telebot.TeleBot(config.bot_key)
crypto_data = {}
coinmarketcap_data = {}
users_buttons_info = {}
users_buttons_delete = {}
users_data = {}
users_path = {}


# создаём словари значений и проверяем сигналы по БД
def create_and_check_data():
    global crypto_data
    crypto_data = get_crypto_data()

    global coinmarketcap_data
    coinmarketcap_data = get_cmc_json()

    cur_time = datetime.now().timetuple()
    next_time = datetime(cur_time[0], cur_time[1], cur_time[2], cur_time[3], cur_time[4], 0) + timedelta(minutes=TIME_VALUE)
    diff_time = (next_time - datetime.now()).total_seconds()
    create_and_check_data_timer = Timer(diff_time, create_and_check_data)
    create_and_check_data_timer.start()


create_and_check_data()


# добавляем дополнительные кнопки создания цели, создания пользовательской кнопки, сравнения и всей инфоромации
def send_with_optional_buttons(recipient, response, path, create_user_but=False, show_all=False, comparison=False):

    t = get_text(recipient)
    keyboard = types.InlineKeyboardMarkup(row_width=6)
    keyboard_buttons = []

    back_button = types.InlineKeyboardButton(text=t[". back"], callback_data="back")
    create_target_button = types.InlineKeyboardButton(text=t[". create_target"], callback_data=path+" create_target")
    keyboard_buttons.append(back_button)
    keyboard_buttons.append(create_target_button)

    if create_user_but is True:
        user_but_button = types.InlineKeyboardButton(text=t[". create_button"], callback_data=path+" create_user_but")
        keyboard_buttons.append(user_but_button)

    if comparison is True:
        comparison_button = types.InlineKeyboardButton(text=t[". comparison"], callback_data=path+" comparison")
        keyboard_buttons.append(comparison_button)

    if show_all is True:
        show_all_button = types.InlineKeyboardButton(text=t[". show_all"], callback_data=path+" all")
        keyboard_buttons.append(show_all_button)

    info_button = types.InlineKeyboardButton(text=t[". info"], callback_data="info")
    keyboard_buttons.append(info_button)

    if len(keyboard_buttons) == 6:
        keyboard.add(keyboard_buttons[0], keyboard_buttons[1], keyboard_buttons[2], keyboard_buttons[3],
                     keyboard_buttons[4], keyboard_buttons[5])
    elif len(keyboard_buttons) == 5:
        keyboard.add(keyboard_buttons[0], keyboard_buttons[1], keyboard_buttons[2], keyboard_buttons[3],
                     keyboard_buttons[4])
    else:
        keyboard.add(keyboard_buttons[0], keyboard_buttons[1], keyboard_buttons[2], keyboard_buttons[3])

    send(recipient, response, reply_markup=keyboard, to_listener=True)  # commercial=True


# удаляем кнопки
def delete_buttons(chat_id):
    try:
        messages_id = users_buttons_delete[chat_id]
        for number_mes_id in range(len(messages_id)):
            bot.delete_message(chat_id, messages_id[number_mes_id])
        users_buttons_delete[chat_id].clear()
    except KeyError:
        pass


# выводим кнопки
def create_buttons(recipient, keyboard_text, buttons_list, callback_data, current_button_number=0, back_button=False,
                   back_button_call_data="back", del_button=False, callback_data_index=None):
    if callback_data_index is None:
        callback_data_index = buttons_list

    t = get_text(recipient)

    keyboard = types.InlineKeyboardMarkup()

    if back_button is True:
        back_button = types.InlineKeyboardButton(text=t[". back"], callback_data=back_button_call_data)
        keyboard.add(back_button)

    if len(buttons_list[current_button_number:]) > MAX_BUTTONS:
        create_buttons_info = {"keyboard_text": t["more"],
                               "buttons_list": buttons_list,
                               "callback_data": callback_data,
                               "current_button_number": current_button_number + MAX_BUTTONS,
                               "back_button": back_button,
                               "back_button_call_data": back_button_call_data,
                               "del_button": del_button,
                               "callback_data_index": callback_data_index}

        users_buttons_info[recipient] = create_buttons_info

        last_button_number = current_button_number + MAX_BUTTONS
    else:
        last_button_number = len(buttons_list)

    for button_number in range(current_button_number, last_button_number):
        button = types.InlineKeyboardButton(text=buttons_list[button_number],
                                            callback_data=callback_data + " " + callback_data_index[button_number])

        if last_button_number - button_number == 1:
            if last_button_number % 2 == 0:
                keyboard.add(button1, button)
            else:
                keyboard.add(button)
        elif button_number % 2 == 0:
            button1 = button
        else:
            keyboard.add(button1, button)

    if len(buttons_list[current_button_number:]) > MAX_BUTTONS:
        show_more_button = types.InlineKeyboardButton(text=t[". show_more"], callback_data="show_more")
        keyboard.add(show_more_button)

    if del_button is True:
        del_button = types.InlineKeyboardButton(text=t[". del_but"], callback_data="del_button " + callback_data)
        keyboard.add(del_button)

    message_id = send(recipient, keyboard_text, reply_markup=keyboard, to_listener=True)

    try:
        users_buttons_delete[recipient].append(message_id.message_id)
    except KeyError:
        users_buttons_delete[recipient] = [message_id.message_id, ]


# информируем о чем-то пользователя
def inform(recipient, text_inform, more_text="", callback_data="ok", cancel=False):
    t = get_text(recipient)
    keyboard = types.InlineKeyboardMarkup()
    ok_button = types.InlineKeyboardButton(text=t[". ok"], callback_data=callback_data)

    if cancel is True:
        cancel_button = types.InlineKeyboardButton(text=t[". cancel"], callback_data="cancel")
        keyboard.add(cancel_button, ok_button)
    else:
        keyboard.add(ok_button)

    message_id = send(recipient, t[text_inform]+more_text, reply_markup=keyboard, to_listener=True)  # commercial=True
    users_buttons_delete[recipient] = [message_id.message_id, ]


# выводим список кнопок на показ или удаление
def operate_user_buttons(recipient, delete_user_button=False):
    t = get_text(recipient)
    rows = get_user_button(recipient)

    callback_data_index = []
    buttons_list = []
    if rows == ():
        inform(recipient, "! no_buttons")
        return

    if delete_user_button is False:
        keyboard_text = t[". your_but"]
        callback_data = ""
        del_button = True
        back_button = False
        back_button_call_data = None
        for row in rows:
            buttons_list.append(row[3])
            callback_data_index.append(str(row[2]))
    else:
        keyboard_text = t[". select_but_to_del"]
        callback_data = "del_user_but?"
        del_button = False
        back_button = True
        back_button_call_data = "my"
        for row in rows:
            buttons_list.append(row[3])
            callback_data_index.append(str(row[0]) + " " + row[3])

    create_buttons(recipient, keyboard_text, buttons_list, callback_data, del_button=del_button,
                   back_button=back_button, callback_data_index=callback_data_index,
                   back_button_call_data=back_button_call_data)


# делаем обёртку для для bot.send_message со вставкой рекламы и дублированием отправки информации listener`у
def send(chat_id, text, disable_web_page_preview=True, reply_to_message_id=None, reply_markup=None,
         disable_notification=None, to_listener=False, commercial=None):

    if to_listener is True:
        try:
            message = users_data[chat_id]
            answer_to_listener = "lang:<b>" + str(message.language_code) + "</b>| @" + str(message.username) \
                                 + " | <b>" + str(message.first_name) + " " + str(message.last_name) \
                                 + "</b> | id<b>" + str(message.id) + "</b>| send in chat<b>" + str(chat_id) \
                                 + "</b>\n\U000025AB" + text
        except KeyError:
            answer_to_listener = str(chat_id) + ": " + text

        bot.send_message(listener, answer_to_listener, parse_mode='HTML')

    if commercial is not None:
        text = text + commercial_text()

    return bot.send_message(chat_id, text, disable_web_page_preview=disable_web_page_preview,
                            reply_to_message_id=reply_to_message_id, reply_markup=reply_markup, parse_mode='HTML',
                            disable_notification=disable_notification)


# обрабатываем путь-команду
def path_processing(entry, recipient):
    t = get_text(recipient)
    users_path[recipient] = entry

    if entry[0] == " " and entry[1] == "/":
        path = entry[2:].split()
    elif entry[0] == "/" or entry[0] == " ":
        path = entry[1:].split()
    else:
        path = entry.split()

    print(path)

    if path[0] == "my":
        operate_user_buttons(recipient, delete_user_button=False)
    elif path[0] == "crypto":
        if len(path) == 1:
            markets = list(crypto_data)
            buttons_list = sorted(markets)
            callback_data = " ".join(path)
            create_buttons(recipient, "<i>... crypto</i>\n" + t["? market"], buttons_list, callback_data)

        elif len(path) == 2:
            currencies = crypto_data[path[1]]
            buttons_list = crypto_sort(currencies, coinmarketcap_data)
            callback_data = " ".join(path)
            create_buttons(recipient, "<i>... " + path[1] + "</i>\n" + t["? cur"], buttons_list, callback_data,
                           back_button=True)

        elif len(path) == 3:
            currencies = list(crypto_data[path[1]][path[2]])
            buttons_list = sorted(currencies)
            callback_data = " ".join(path)
            create_buttons(recipient, "<i>... " + path[2] + "</i>\n" + t["? 2 cur"], buttons_list, callback_data,
                           back_button=True)

        elif len(path) == 4:
            response = crypto_main_response(crypto_data, path, t)
            send_with_optional_buttons(recipient, response, entry, create_user_but=True,
                                       show_all=True, comparison=True)

        elif len(path) == 5:
            if path[4] == "all":
                response = crypto_more_response(crypto_data, path, t)
                send_with_optional_buttons(recipient, response, entry, create_user_but=True,
                                           show_all=False, comparison=True)
            elif path[4] == "create_user_but":
                inform_text = create_user_button(recipient, entry, crypto_data[path[1]][path[2]][path[3]]["name"])
                inform(recipient, inform_text)

        elif len(path) == 6:
            if path[5] == "create_user_but":
                inform_text = create_user_button(recipient, entry, crypto_data[path[1]][path[2]][path[3]]["name"])
                inform(recipient, inform_text)

    elif path[0] == "del_user_but?":
        response = "  <b>" + path[2] + path[3] + "</b>\n" + t["? sure"]
        inform(recipient, "delete", response, callback_data="del_user_but! " + path[1], cancel=True)
    elif path[0] == "del_user_but!":
        del_user_button(recipient, path[1])
        operate_user_buttons(recipient, delete_user_button=True)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    recipient = message.from_user.id
    delete_buttons(recipient)
    users_data[recipient] = message.from_user
    get_text(user_id=recipient, lang=message.from_user.language_code)
    path_processing(message.text.lower(), recipient)


@bot.callback_query_handler(func=lambda call: call.data == 'show_more')
def show_more_inline(call):
    try:
        recipient = call.message.chat.id
        create_buttons(recipient,
                       users_buttons_info[recipient]["keyboard_text"],
                       users_buttons_info[recipient]["buttons_list"],
                       users_buttons_info[recipient]["callback_data"],
                       users_buttons_info[recipient]["current_button_number"],
                       users_buttons_info[recipient]["back_button"],
                       users_buttons_info[recipient]["back_button_call_data"],
                       users_buttons_info[recipient]["del_button"],
                       users_buttons_info[recipient]["callback_data_index"])
    except KeyError:
        pass


@bot.callback_query_handler(func=lambda call: call.data == 'back')
def back_inline(call):
    recipient = call.message.chat.id
    try:
        user_path = users_path[recipient].split()
        user_path.pop()
        delete_buttons(recipient)
        path_processing(" ".join(user_path), recipient)
    except KeyError:
        pass


@bot.callback_query_handler(func=lambda call: call.data == 'info')
def info_inline(call):
    recipient = call.message.chat.id
    inform(recipient, "... info")


@bot.callback_query_handler(func=lambda call: call.data == 'ok')
def ok_inline(call):
    recipient = call.message.chat.id
    delete_buttons(recipient)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    recipient = call.message.chat.id
    if call.data == "cancel ":
        print("pass")
        pass
    elif call.data == "del_button ":
        delete_buttons(recipient)
        operate_user_buttons(recipient, delete_user_button=True)

    else:
        delete_buttons(recipient)
        path_processing(call.data, recipient)


bot.polling(none_stop=True, interval=0)

