from bot.utils.bot_functions import *
from bot.control.update import dp
from bot.services import filter_users_by_phone
from bot.services import string_service
from bot.services.language_service import get_word
from app.services.order_service import get_order_by_uuid_without_404, get_order_by_order_id_without_404
from app.services.postgresql_service import get_car_info, get_order_by_id
import json

def send_cheque(phone, order_id):
    if users := filter_users_by_phone(phone):
        user = users[0]
        order_obj = get_order_by_order_id_without_404(order_id)
        order = get_order_by_id(order_id)
        src = order[0] or ''
        dst = order[1] or ''
        starttime = order[2] or ''
        endtime = order[3] or ''
        executor_id = order[4] or ''
        amount = order[5] or ''
        distance = order[6] or ''
        standtime = order[7] or ''
        waittime = order[8] or ''
        street = order[9] or ''
        house = order[10] or ''
        dststreet = order[11] or ''
        dsthouse = order[12] or ''
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
        car_phone = car_info[6] or ''

        text = string_service.cheque_info(
            user.user_id, 
            src, dst, starttime, endtime, amount, distance,
            standtime, waittime, street, house, dststreet, dsthouse,
            autonum, color, brand, model, lastname, firstname, car_phone, taximeter_data
            )
        if order_obj:
            markup = InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    text=get_word('main menu', chat_id=user.user_id), 
                    callback_data='main_menu'
                    )
            ]])
        else:
            markup = None
        msg = send_newsletter(bot, user.user_id, text, reply_markup=markup)
        # save context user_data
        dp.user_data[user.user_id]['last_msg'] = msg
        dp.user_data[user.user_id]['last_markup'] = markup
        return True
    else:
        return False

def send_order_status(phone, data):
    status_code = int(data['status_code'])
    if users := filter_users_by_phone(phone):
        user = users[0]
        order = get_order_by_order_id_without_404(data['id'])
        markup = None
        if status_code == 80:
            text = get_word('your order is in moderation', chat_id=user.user_id)
            
        elif status_code == 95:
            text = get_word('your order is cancelled', chat_id=user.user_id)
            markup = InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    text=get_word('main menu', chat_id=user.user_id), 
                    callback_data='main_menu'
                    )
            ]])
        elif status_code == 10:
            text = string_service.car_info_string(
                user.user_id, data['remaining'], data['car_phone'], 
                data['car_firstname'],  data['brand'], data['model'], 
                data['color'], data['autonum']
            )
        elif status_code == 11:
            text = get_word('driver is here', chat_id=user.user_id)
        elif status_code == 4:
            text = get_word('order is in execution', chat_id=user.user_id)
            markup = reply_keyboard_remove()

        if not order:
            markup = None
        msg = send_newsletter(bot, user.user_id, text, reply_markup=markup)
        # save context user_data
        dp.user_data[user.user_id]['last_msg'] = msg
        dp.user_data[user.user_id]['last_markup'] = markup
        return True
    else:
        return False 