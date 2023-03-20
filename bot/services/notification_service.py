from bot.utils.bot_functions import *
from bot.services import filter_users_by_phone
from bot.services import string_service
from bot.services.language_service import get_word
from app.services.order_service import get_order_by_uuid_without_404

def send_cheque(phone, car_phone, car_firstname, brand, model, color, autonum, amount, uuid):
    if users := filter_users_by_phone(phone):
        user = users[0]
        order = get_order_by_uuid_without_404(uuid)
        text = string_service.cheque_info(user.user_id, car_phone, car_firstname, brand, model, color, autonum, amount)
        if order:
            markup = InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    text=get_word('main menu', chat_id=user.user_id), 
                    callback_data='main_menu'
                    )
            ]])
        else:
            markup = None
        send_newsletter(user.user_id, text, markup)
        return True
    else:
        return False

def send_order_status(phone, data):
    status_code = int(data['status_code'])
    if users := filter_users_by_phone(phone):
        user = users[0]
        order = get_order_by_uuid_without_404(data['uuid'])
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
        send_newsletter(bot, user.user_id, text, markup)
        
        return True
    else:
        return False 