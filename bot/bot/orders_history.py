from bot.bot import *
import json

def _to_the_get_year(update, context):
    bot_send_chat_action(update, context)
    bot_user = get_user_by_update(update)
    years = filter_years_of_client_orders(bot_user)
    reply_markup = order_years_keyboard(update, years)
    text = get_word('select year of order', update)
    msg=bot_send_message(update, context, text, reply_markup=reply_markup)
    context.user_data['last_msg'] = msg
    return GET_YEAR

def _to_the_get_month(update, context, year):
    bot_send_chat_action(update, context)
    bot_user = get_user_by_update(update)
    # get months of client orders and collect it in marup
    months = filter_months_of_client_orders(bot_user, year=year)
    markup = order_months_keyboard(update, months)
    # send message to bot
    text = get_word('select month of order', update).format(year)
    bot_delete_message(update, context)
    msg=bot_send_message(update, context, text, markup)
    context.user_data['last_msg'] = msg
    return GET_MONTH

def _to_the_get_day(update, context, year, month):
    bot_send_chat_action(update, context)
    bot_user = get_user_by_update(update)
    # get months of client orders and collect it in marup
    days = filter_days_of_client_orders(bot_user, year=year, month=month)
    markup = order_days_keyboard(update, days)
    # send message to bot
    text = get_word('select day of order', update).format(year, get_word(month_by_index(month), update))
    bot_delete_message(update, context)
    msg=bot_send_message(update, context, text, markup)
    context.user_data['last_msg'] = msg
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

    # uploading action
    bot_send_chat_action(update, context)
    bot_answer_callback_query(update, context, get_word('loading', update), show_alert=False)
    
    bot_user = get_user_by_update(update)
    # get day from callback data
    day = get_callback_query_data(update)
    # get orders
    orders = filter_orders_by_date(bot_user, day, month, year)
    # # send message to bot
    bot_delete_message(update, context)
    # send orders
    for order in orders:
        src = order[0] or ''
        dst = order[1] or ''
        starttime = order[2] or ''
        endtime = order[3] or ''
        executor_id = order[4] or ''
        amount = order[5] or ''
        distance = order[6] or ''
        standtime = order[7] or ''
        waittime = order[8] or ''
        street = src
        house = ''
        dststreet = ''
        dsthouse = ''
        try:
            taximeter_data = json.loads(order[13])
        except:
            taximeter_data = {}
        # get car info
        car_info = get_car_info(executor_id) or ['' for i in range(7)]
        autonum = car_info[0] or ''
        color = car_info[1] or ''
        brand = car_info[2] or ''
        model = car_info[3] or ''
        lastname = car_info[4] or ''
        firstname = car_info[5] or ''
        phone = car_info[6] or ''
        
        text = order_history_details_string(
            update,
            src, dst, starttime, endtime, amount, distance,
            standtime, waittime, street, house, dststreet, dsthouse,
            autonum, color, brand, model, lastname, firstname, phone, taximeter_data
        )
        bot_send_message(update, context, text)

    main_menu(update, context)
    return ConversationHandler.END
