from bot.bot import *

def _to_the_get_year(update, context):
    bot_user = get_user_by_update(update)
    years = filter_years_of_client_orders(bot_user)
    reply_markup = order_years_keyboard(update, years)
    text = get_word('select year of order', update)
    bot_send_message(update, context, text, reply_markup=reply_markup)
    return GET_YEAR

def _to_the_get_month(update, context, year):
    bot_user = get_user_by_update(update)
    # get months of client orders and collect it in marup
    months = filter_months_of_client_orders(bot_user, year=year)
    markup = order_months_keyboard(update, months)
    # send message to bot
    text = get_word('select month of order', update)
    bot_delete_message(update, context)
    bot_send_message(update, context, text, markup)
    return GET_MONTH

def _to_the_get_day(update, context, year, month):
    bot_user = get_user_by_update(update)
    # get months of client orders and collect it in marup
    days = filter_days_of_client_orders(bot_user, year=year, month=month)
    markup = order_days_keyboard(update, days)
    # send message to bot
    text = get_word('select day of order', update)
    bot_delete_message(update, context)
    bot_send_message(update, context, text, markup)
    return GET_DAY

@is_start
def get_year_query(update, context):
    update = update.callback_query
    # check, is data back
    if update.data == 'back':
        bot_delete_message(update, context)
        main_menu(update, context)
        return ConversationHandler.END

    # get year from callback data
    year = get_callback_query_data(update)
    # set year to user data
    context.user_data['year'] = year
    
    return _to_the_get_month(update, context, year)

@is_start
def get_month_query(update, context):
    update = update.callback_query
    # check, is data back
    if update.data == 'back':
        bot_delete_message(update, context)
        return _to_the_get_year(update, context)

    # get month from callback data
    month = get_callback_query_data(update)
    # get year from user_data
    year = context.user_data['year']
    # set month to user data
    context.user_data['month'] = month
    return _to_the_get_day(update, context, year, month)

@is_start
def get_day_query(update, context):
    update = update.callback_query
    # get year and month from user_data
    year = context.user_data['year']
    month = context.user_data['month']
    # check, is data back
    if update.data == 'back':
        return _to_the_get_month(update, context, year)

    bot_user = get_user_by_update(update)
    # get day from callback data
    day = get_callback_query_data(update)
    # get orders
    orders = filter_orders_by_date(bot_user, day, month, year)

    # # send message to bot
    bot_answer_callback_query(update, context, str(day))
    bot_delete_message(update, context)
    main_menu(update, context)
    return ConversationHandler.END
