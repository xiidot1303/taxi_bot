from telegram import Bot, InputTextMessageContent
from telegram.ext import Dispatcher, ConversationHandler, PicklePersistence, BasePersistence
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    filters,
    CallbackQueryHandler,
    InlineQueryHandler,
    TypeHandler,
    BaseFilter
)

from bot.resources.strings import lang_dict
from bot.resources.conversationList import *
from bot.bot import (
    main, login, orders_history, settings
)


login_handler = ConversationHandler(
    entry_points=[CommandHandler("start", main.start)],
    states={
        SELECT_LANG: [MessageHandler(Filters.text(lang_dict["uz_ru"]), login.select_lang)],
        GET_NAME: [MessageHandler(Filters.text, login.get_name)],
        GET_CONTACT: [MessageHandler(Filters.all, login.get_contact)],
    },
    fallbacks=[],
    name="login",
    persistent=True,

)

settings_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text(lang_dict["settings"]), main.settings)],
    states={
        ALL_SETTINGS: [MessageHandler(Filters.text, settings.all_settings)],
        LANG_SETTINGS: [
            CallbackQueryHandler(settings.lang_settings),
            CommandHandler("start", settings.lang_settings),
        ],
        PHONE_SETTINGS: [MessageHandler(Filters.all, settings.phone_settings)],
        NAME_SETTINGS: [MessageHandler(Filters.text, settings.name_settings)],
    },
    fallbacks=[],
    name="settings",
    persistent=True,
  
)

order_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text([lang_dict["let order"]]), main.order)],
    states={
        
    },
    fallbacks=[],
    name='order',
    persistent=True,
)

order_history_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text(lang_dict["order history"]), main.order_history)],
    states={
        GET_YEAR: [
            CallbackQueryHandler(orders_history.get_year_query),
            CommandHandler("start", orders_history.get_year_query)
        ],
        GET_MONTH: [
            CallbackQueryHandler(orders_history.get_month_query),
            CommandHandler("start", orders_history.get_month_query)
        ],
        GET_DAY: [
            CallbackQueryHandler(orders_history.get_day_query),
            CommandHandler("start", orders_history.get_day_query)
        ],
    },
    fallbacks=[],
    name="order_history",
    persistent=True,
)