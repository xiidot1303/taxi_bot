from bot.utils import *
from bot.utils.bot_functions import *
from bot.utils.keyboards import *
from bot.resources.strings import lang_dict
from bot.services import *
from bot.services.language_service import *
from app.services.order_service import *
from app.services.address_service import *
from app.services.api_service import *
from bot.services.string_service import *
from bot.resources.conversationList import *
from app.utils import month_by_index

def main_menu(update, context):
    try:
        a = update.callback_query.id
        update = update.callback_query
    except:
        www = 0  # do nothing

    bot = context.bot
    keyboard = [
        [get_word('let order', update)],
        [get_word('order history', update)],
        [get_word('settings', update)],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    bot.send_message(
        update.message.chat.id,
        get_word("main menu", update),
        reply_markup=reply_markup,
    )
    check_username(update)

def make_button_settings(update, context):
    try:
        a = update.callback_query.id
        update = update.callback_query
    except:
        www = 0  # do nothing
    bot = context.bot

    bot.send_message(
        update.message.chat.id,
        get_word("settings desc", update),
        reply_markup=ReplyKeyboardMarkup(keyboard=settings_keyboard(update), resize_keyboard=True),
    )

def is_group(update):
    if update.message.chat.type == 'group' or update.message.chat.type == 'supergroup':
        return True
    return False


def save_and_get_photo(update, context):
    bot = context.bot
    photo_id = bot.getFile(update.message.photo[-1].file_id)
    *args, file_name = str(photo_id.file_path).split('/')
    d_photo = photo_id.download('files/photos/{}'.format(file_name))
    return str(d_photo).replace('files/', '')



# DECORATORS

def is_start_registr(func):
    def func_arguments(*args, **kwargs):
        bot = args[1].bot
        try:
            lalal = args[0].message.text
            update = args[0]
            data = ""
        except:
            update = args[0].callback_query
            data = update.data
        id = update.message.chat.id
        if update.message.text == "/start":
            update.message.reply_text(
                lang_dict['hello'],
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[["UZ 🇺🇿", "RU 🇷🇺"]], resize_keyboard=True
                ),
            )
            return SELECT_LANG

        else:
            return func(*args, **kwargs)

    return func_arguments


def is_start(func):  # This deco break registration if user send /start.
    def func_arguments(*args, **kwargs):
        context = args[1]
        bot = context.bot
        try:
            lalal = args[0].message.text
            update = args[0]
            data = ""
        except Exception:
            try:
                update = args[0].callback_query
                data = update.data
            except:
                return func(*args, **kwargs)
                
        id = update.message.chat.id
        if (
            update.message.text == "/start"
            or data == "main_menu"
            or update.message.text == get_word("main menu", update)
        ):
            if data == 'main_menu':
                bot_delete_message(update, context)
            # some func
            remove_inline_keyboards_from_last_msg(update, context)
            main_menu(args[0], args[1])
            return ConversationHandler.END
        else:
            return func(*args, **kwargs)

    return func_arguments


def ignore_start(func):  
    def func_arguments(*args, **kwargs):
        context = args[1]
        bot = context.bot
        try:
            lalal = args[0].message.text
            update = args[0]
            data = ""
        except Exception:
            try:
                update = args[0].callback_query
                data = update.data
            except:
                return func(*args, **kwargs)
                
        id = update.message.chat.id
        if (
            update.message.text == "/start"
            or update.message.text == get_word("main menu", update)
        ):
            
            # some func
            bot_delete_message(update, context)
            return
        elif data == "main_menu":
            bot_delete_message(update, context)
            main_menu(args[0], args[1])
            return ConversationHandler.END
        else:
            return func(*args, **kwargs)

    return func_arguments
