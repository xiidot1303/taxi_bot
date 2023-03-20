from bot.models import *
from bot.resources.strings import lang_dict
from bot.resources.colors import colors_dict

def get_word(text, update=None, chat_id=None):
    if not chat_id:
        chat_id = update.message.chat.id

    user = Bot_user.objects.get(user_id=chat_id)
    text = text.lower()
    if user.lang == "uz":
        result = lang_dict[text][0]
    else:
        result = lang_dict[text][1]
    
    return result if result else text

def get_color(color, update=None, chat_id=None):
    if not chat_id:
        chat_id = update.message.chat.id

    user = Bot_user.objects.get(user_id=chat_id)

    if user.lang == "uz":
        result = colors_dict[color] if color in colors_dict else color
    else:
        result = color
    return result
    