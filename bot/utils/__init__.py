from bot.utils.bot_functions import *
from yandex_geocoder import Client

def get_callback_query_data(update):
    data = update.data
    *args, result = str(data).split('_')
    return result

def get_location_coordinates(l):
    return l['latitude'], l['longitude']

def split_text_and_text_id(msg):
    return msg.split('<>?')

def get_last_msg_and_markup(context):
    return context.user_data['last_msg'], context.user_data['last_markup'] if 'last_markup' in context.user_data else None

def remove_inline_keyboards_from_last_msg(update, context):
    try:
        last_msg, markup = get_last_msg_and_markup(context)
        msg = bot_edit_message_text(update, context, last_msg.text, last_msg.message_id)
        return msg
    except:
        return None

def get_address_by_coordinates(lat, lon):
    try:
        client = Client('4d16304f-12ba-4134-ac9b-f0da5028a1f4')
        location = client.address(lon, lat)
        return location
    except:
        return ""

def set_last_msg_and_markup(context, msg, markup=None):
    context.user_data['last_msg'] = msg
    context.user_data['last_markup'] = markup

def is_phonenumber_correct(phone):
    phone = phone.replace(' ', '')
    phone = '+998' + phone if len(phone) == 9 else phone
    phone = '+' + phone if len(phone) == 12 and phone[:3] == '998' else phone
    if len(phone) == 13 and phone[:4] == '+998':
            return phone
    else:
        return False