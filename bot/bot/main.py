from bot.bot import *
from bot.bot.order import to_the_get_point_a as _to_the_get_point_a

def start(update, context):
    if is_group(update):
        return 

    if is_registered(update.message.chat.id):
        # some functions
        main_menu(update, context)
    else:
        hello_text = lang_dict['hello']
        update.message.reply_text(
            hello_text,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[["UZ 🇺🇿", "RU 🇷🇺"]], resize_keyboard=True, one_time_keyboard=True
            ),
        )
        return SELECT_LANG


def settings(update, context):
    make_button_settings(update, context)
    return ALL_SETTINGS

def ordering(update, context):
    bot_user = get_object_by_update(update)
    if bot_user.blocked:
        update_message_reply_text(update, get_word('you are blocked', update))
        return
    context.user_data['next'] = CONFIRM_ORDER
    context.user_data['dst'] = ''
    context.user_data['dst_street'] = ''
    context.user_data['dst_house'] = ''
    context.user_data['src_house'] = ''
    return _to_the_get_point_a(update, context)

def order_history(update, context):
    bot_user = get_user_by_update(update)
    years = filter_years_of_client_orders(bot_user)
    if years: 
        reply_markup = order_years_keyboard(update, years)
        text = get_word('select year of order', update)
        msg = bot_send_message(update, context, text, reply_markup=reply_keyboard_remove())
        bot_delete_message(update, context, msg.message_id)
        msg=bot_send_message(update, context, text, reply_markup=reply_markup)
        context.user_data['last_msg'] = msg
        return GET_YEAR
    else:
        text = get_word('not available orders yet', update)
        update_message_reply_text(update, text)
        main_menu(update, context)

def bonus(update, context):
    phone = get_object_by_update(update).phone
    balance = client_bonus_count(phone)
    text = get_word('your balance', update).format(balance)
    update_message_reply_text(update, text)

def leave_feedback(update, context):
    text = get_word('write your feedback', update)
    markup = reply_keyboard_markup([[get_word('main menu', update)]])
    msg = update_message_reply_text(update, text, markup)
    set_last_msg_and_markup(context, msg, markup)
    return GET_FEEDBACK