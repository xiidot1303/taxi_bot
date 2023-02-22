from bot.services.language_service import get_word

def cheque_info(chat_id, car_phone, car_firstname, brand, model, color, autonum, amount):
    text = get_word('cheque info', chat_id=chat_id)
    text = text.format(
        car_phone = car_phone, car_firstname=car_firstname, brand=brand,
        model=model, color=color, autonum=autonum, amount=amount 
    )
    return text

def car_info_string(chat_id, remaining, car_phone, car_firstname, brand, model, color, autonum):
    text = "{}: {} {} {}, {}: {}\n{}: {} {}\n{}: {}, {}".format(
        get_word('car', chat_id=chat_id), brand, model, color, 
        get_word('number', chat_id=chat_id), autonum,
        get_word('arrival time', chat_id=chat_id), remaining, get_word('minute', chat_id=chat_id),
        get_word('driver', chat_id=chat_id), car_firstname, car_phone

    )
    return text

def select_point_a_string(update):
    text1 = get_word('select point a', update)
    text2 = get_word('select address or location', update)
    text = f"{text1}\n{text2}"
    return text

def select_point_b_string(update, street, house=""):
    point_a_text = get_word('point a', update)
    text1 = get_word('select point b', update)
    text2 = get_word('select address or location', update)
    text = f"{point_a_text}: {street} {house}\n\n{text1}\n{text2}"
    return text

def address_description_for_query_string(update, city):
    city_text = get_word('city', chat_id=update.inline_query.from_user.id)
    description = f'{city_text}: {city}'
    return description

def order_details_before_confirmation_string(update, point_a, house_a, point_b, house_b, price, distance):
    text = "{point_a_text}: {point_a}, {house_a}\n{point_b_text}: {point_b}, {house_b}\n{price_text}: {price}\n{distance_text}: {distance}\n\n{confirmation_text}".format(
        point_a_text = get_word('point a', update),
        point_a = point_a,
        house_a = house_a,
        point_b_text = get_word('point b', update),
        point_b = point_b if point_b else '❌',
        house_b = house_b,
        price_text = get_word('price', update),
        price = price,
        distance_text = get_word('distance', update),
        distance = distance if distance else '',
        confirmation_text = get_word('confirm order', update)
    )
    return text
