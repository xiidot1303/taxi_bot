from bot.utils.bot_functions import *
from bot.services import filter_users_by_phone
from bot.services import string_service

def send_cheque(phone, car_phone, car_firstname, brand, model, color, autonum, amount):
    if users := filter_users_by_phone(phone):
        user = users[0]
        text = string_service.cheque_info(user.user_id, car_phone, car_firstname, brand, model, color, autonum, amount)
        send_newsletter(user.user_id, text)
        return True
    else:
        return False