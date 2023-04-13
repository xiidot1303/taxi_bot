from bot.bot import *


def _to_the_select_lang(update):
    update_message_reply_text(
        update,
        "Bot tilini tanlang\n\nВыберите язык бота",
        reply_markup=reply_keyboard_markup([lang_dict['uz_ru']]),
        
    )   
    return SELECT_LANG

def _to_the_get_name(update):
    update_message_reply_text(
        update=update,
        text=get_word("type name", update),
        reply_markup=reply_keyboard_markup([[get_word("back", update)]]),
    )
    return GET_NAME

def _to_the_get_contact(update):
    i_contact = KeyboardButton(
        text=get_word("leave number", update), request_contact=True
    )
    update_message_reply_text(
        update,
        get_word("send number", update),
        reply_markup=reply_keyboard_markup(
            [[i_contact], [get_word("back", update)]]
        ),
    )
    return GET_CONTACT

def _to_the_get_city(update, context):
    buttons = [
        [city.title] for city in cities_all()
    ]
    markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    text = get_word('select city', update)
    msg = update_message_reply_text(update, text, markup)
    set_last_msg_and_markup(context, msg, markup)
    return GET_CITY

@is_start_registr
def select_lang(update, context):
    text = update.message.text
    if "UZ" in text:
        lang = "uz"
    elif "RU" in text:
        lang = "ru"
    else:
        return _to_the_select_lang(update)

    get_or_create(user_id=update.message.chat.id)
    obj = get_object_by_user_id(user_id=update.message.chat.id)
    obj.lang = lang
    obj.save()

    return _to_the_get_name(update)


@is_start_registr
def get_name(update, context):
    if update.message.text == get_word("back", update):
        return _to_the_select_lang(update)

    obj = get_object_by_user_id(user_id=update.message.chat.id)
    obj.name = update.message.text
    obj.username = update.message.chat.username
    obj.firstname = update.message.chat.first_name
    obj.save()

    return _to_the_get_contact(update)


@is_start_registr
def get_contact(update, context):
    if update.message.text == get_word("back", update):
        return _to_the_get_name(update)

    if update.message.contact == None or not update.message.contact:
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
        return GET_CONTACT
    obj = get_object_by_user_id(user_id=update.message.chat.id)
    obj.phone = phone_number
    obj.save()
    return _to_the_get_city(update, context)

@ignore_start
def get_city(update, context):
    # get city name from message
    city_title = update.message.text
    # get bot user
    bot_user = get_object_by_update(update)
    # get city obj by title
    city = get_city_by_title(city_title)
    # check city is available
    if not city:
        update_message_reply_text(update, get_word('incorrect city', update))
        return
    # set bot user city
    bot_user.city = city
    bot_user.save()
    # go to main menu
    main_menu(update, context)
    return ConversationHandler.END