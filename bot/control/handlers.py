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
    main, login, orders_history, settings, order, search
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
    entry_points=[MessageHandler(Filters.text(lang_dict["let order"]), main.ordering)],
    states={
        GET_POINT_A: [
            CallbackQueryHandler(order.get_point_a_query),
            CommandHandler("start", order.get_point_a),
            MessageHandler(Filters.text, order.get_point_a),
            MessageHandler(Filters.location, order.get_point_a),
            ],
        GET_POINT_A_HOUSE: [MessageHandler(Filters.text, order.get_point_a_house)],
        GET_POINT_B: [
            CallbackQueryHandler(order.get_point_b_query),
            CommandHandler("start", order.get_point_b),
            MessageHandler(Filters.text, order.get_point_b),
            MessageHandler(Filters.location, order.get_point_b),
            ],
        GET_POINT_B_HOUSE: [MessageHandler(Filters.text, order.get_point_b_house)],
        CONFIRM_ORDER: [MessageHandler(Filters.text, order.confirm_order)],
        ORDER_PROCESS: [
            CallbackQueryHandler(order.order_process),
            MessageHandler(Filters.text, order.order_process)
        ],
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

search_handler = InlineQueryHandler(search.get_inline_query)
bonus_handler = MessageHandler(Filters.text(lang_dict['balance']), main.bonus)