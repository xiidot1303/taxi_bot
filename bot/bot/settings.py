from bot.bot import *

@is_start
def all_settings(update, context):
    msg = update.message.text
    bot = context.bot

    if msg == get_word("change lang", update):
        current_lang = get_user_by_update(update).lang
        if current_lang == "uz":
            uz_text = "UZ \U0001F1FA\U0001F1FF   ✅"
            ru_text = "RU \U0001F1F7\U0001F1FA"
        else:
            uz_text = "UZ \U0001F1FA\U0001F1FF"
            ru_text = "RU \U0001F1F7\U0001F1FA    ✅"
        i_uz = InlineKeyboardButton(text=uz_text, callback_data="set_lang_uz")
        i_ru = InlineKeyboardButton(text=ru_text, callback_data="set_lang_ru")
        i_back = InlineKeyboardButton(
            get_word("back", update), callback_data="back_settings"
        )
        del_msg = update.message.reply_text(
            get_word("select lang", update),
            reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
        )
        bot.delete_message(update.message.chat.id, del_msg.message_id)
        bot.send_message(
            update.message.chat.id,
            get_word("select lang", update),
            reply_markup=InlineKeyboardMarkup([[i_uz], [i_ru], [i_back]]),
        )
        return LANG_SETTINGS

    elif msg == get_word("change phone number", update):
        user = get_user_by_update(update)
        text = (
            get_word("your phone number", update).replace("<>", user.phone or '')
            + "\n\n"
            + get_word("send new phone number", update)
        )
        i_contact = KeyboardButton(
            text=get_word("leave number", update), request_contact=True
        )
        i_back = KeyboardButton(text=get_word("back", update))
        update.message.reply_text(
            text,
            reply_markup=ReplyKeyboardMarkup(
                [[i_contact], [i_back]], resize_keyboard=True
            ),
            parse_mode=ParseMode.HTML,
        )
        return PHONE_SETTINGS
    elif msg == get_word("change name", update):
        user = get_user_by_update(update)
        text = (
            get_word("your name", update)
            + user.name
            + "\n\n"
            + get_word("send new name", update)
        )
        update.message.reply_text(
            text,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[get_word("back", update)]], resize_keyboard=True
            ),
            parse_mode=ParseMode.HTML,
        )
        return NAME_SETTINGS

    elif msg == get_word("change city", update):
        user = get_user_by_update(update)
        current_city = user.city.title if user.city else ''
        text = (
            get_word("current city", update)
            + current_city
            + "\n\n"
            + get_word("select city", update)
        )
        buttons = [
            [city.title] for city in cities_all()
        ]
        buttons.append([get_word("back", update)])
        update.message.reply_text(
            text,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=buttons, resize_keyboard=True
            ),
            parse_mode=ParseMode.HTML,
        )
        return CITY_SETTINGS


#  lang settings
@is_start
def lang_settings(update, context):
    update = update.callback_query
    bot = context.bot
    data = str(update.data)
    user = get_object_by_user_id(user_id=update.message.chat.id)
    if data == "set_lang_uz":
        user.lang = "uz"
        user.save()
    elif data == "set_lang_ru":
        user.lang = "ru"
        user.save()
    elif data == "back_settings":
        bot.delete_message(update.message.chat.id, update.message.message_id)
        make_button_settings(update, context)
        return ALL_SETTINGS
    current_lang = user.lang
    if current_lang == "uz":
        uz_text = "UZ \U0001F1FA\U0001F1FF   ✅"
        ru_text = "RU \U0001F1F7\U0001F1FA"
    else:
        uz_text = "UZ \U0001F1FA\U0001F1FF"
        ru_text = "RU \U0001F1F7\U0001F1FA    ✅"

    i_uz = InlineKeyboardButton(text=uz_text, callback_data="set_lang_uz")
    i_ru = InlineKeyboardButton(text=ru_text, callback_data="set_lang_ru")
    i_back = InlineKeyboardButton(
        get_word("back", update), callback_data="back_settings"
    )
    update.edit_message_text(
        get_word("select lang", update),
        reply_markup=InlineKeyboardMarkup([[i_uz], [i_ru], [i_back]]),
    )


# phone settings
@is_start
def phone_settings(update, context):
    if update.message.contact == None or not update.message.contact:
        msg = update.message.text
        if msg == get_word("back", update):
            make_button_settings(update, context)
            return ALL_SETTINGS
        phone_number = update.message.text
        phone_number = is_phonenumber_correct(phone_number)
        if not phone_number:
            update.message.reply_text(get_word("number is incorrect", update))
            return
    else:
        phone_number = update.message.contact.phone_number

    # check that phone is available or no
    is_available = Bot_user.objects.filter(phone=phone_number)
    if is_available:
        update.message.reply_text(get_word("number is logged", update))
        return PHONE_SETTINGS
    obj = get_object_by_user_id(user_id=update.message.chat.id)
    obj.phone = phone_number
    obj.save()
    update.message.reply_text(get_word("changed your phone number", update))
    make_button_settings(update, context)
    return ALL_SETTINGS


# name settings
@is_start
def name_settings(update, context):
    msg = update.message.text
    if msg == get_word("back", update):
        make_button_settings(update, context)
        return ALL_SETTINGS
    new_name = msg
    obj = get_user_by_update(update)
    obj.name = new_name
    obj.save()
    update.message.reply_text(get_word("changed your name", update))
    make_button_settings(update, context)
    return ALL_SETTINGS

# city settings
@is_start
def city_settings(update, context):
    msg = update.message.text
    if msg == get_word("back", update):
        make_button_settings(update, context)
        return ALL_SETTINGS
    new_city = msg
    obj = get_user_by_update(update)
    city = get_city_by_title(new_city)
    # check city is available
    if not city:
        update_message_reply_text(update, get_word('incorrect city', update))
        return
    obj.city = city
    obj.save()
    update.message.reply_text(get_word("changed your city", update))
    make_button_settings(update, context)
    return ALL_SETTINGS
