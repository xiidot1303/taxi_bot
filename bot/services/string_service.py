from bot.services.language_service import get_word

def cheque_info(chat_id, car_phone, car_firstname, brand, model, color, autonum, amount):
    text = get_word('cheque info', chat_id=chat_id)
    text = text.format(
        car_phone = car_phone, car_firstname=car_firstname, brand=brand,
        model=model, color=color, autonum=autonum, amount=amount 
    )
    return text