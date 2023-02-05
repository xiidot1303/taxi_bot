from bot.bot import *

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

def order_history(update, context):
    bot_user = get_user_by_update(update)
    years = filter_years_of_client_orders(bot_user)
    if years: 
        reply_markup = order_years_keyboard(update, years)
        text = get_word('select year of order', update)
        msg = bot_send_message(update, context, text, reply_markup=reply_keyboard_remove())
        bot_delete_message(update, context, msg.message_id)
        bot_send_message(update, context, text, reply_markup=reply_markup)
        return GET_YEAR
    else:
        text = get_word('not available orders yet', update)
        update_message_reply_text(update, text)
        main_menu(update, context)
