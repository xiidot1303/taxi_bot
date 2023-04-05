from bot.services.language_service import get_word, get_color

def cheque_info(
    chat_id, 
    src, dst, starttime, endtime, amount, distance, 
    standtime, waittime, street, house, dststreet, dsthouse,
    autonum, color, brand, model, lastname, firstname, phone, taximeter_data
    ):
    # text = get_word('cheque info', chat_id=chat_id)
    # text = text.format(
    #     car_phone = car_phone, car_firstname=car_firstname, brand=brand,
    #     model=model, color=color, autonum=autonum, amount=amount 
    # )


    text = "<b>{finish_text}</b>\n\n<i>{point_a_text}:</i> {point_a}\n<i>{point_b_text}:</i> {point_b}\n"
    text += "<i>{amount_text}:</i> {amount}\n<i>{baggage_text}:</i> {baggage}\n<i>{distance_text}:</i> {distance} {metr}\n"
    text += "<i>{standtime_text}:</i> {standtime}\n<i>{waittime_text}:</i> {waittime}\n\n"
    text += "{driver_info_text}:\n<i>{name_text}:</i> {lastname} {firstname}\n<i>{phone_text}:</i> {phone}\n"
    text += "<i>{car_info_text}:</i> {color} {brand} {model} | {autonum}\n"
    text = text.format(
        finish_text = get_word('finish_text', chat_id=chat_id),
        point_a_text = get_word('point a', chat_id=chat_id),
        point_a = src,
        point_b_text = get_word('point b', chat_id=chat_id),
        point_b = dst,
        amount_text = get_word('amount', chat_id=chat_id),
        amount = amount,
        baggage_text = get_word('baggage', chat_id=chat_id),
        baggage = float(taximeter_data['margin']) if 'margin' in taximeter_data else "",
        distance_text = get_word('distance', chat_id=chat_id),
        distance = distance,
        metr = get_word('meter', chat_id=chat_id),
        standtime_text = get_word('standtime', chat_id=chat_id),
        standtime = "{} {} {} {}".format(
            int(standtime) // 60 if standtime else standtime, 
            get_word('min.', chat_id=chat_id), 
            int(standtime) % 60 if standtime else standtime, 
            get_word('sek.', chat_id=chat_id)),
        waittime_text = get_word('waittime', chat_id=chat_id),
        waittime = waittime,
        driver_info_text = get_word('driver info', chat_id=chat_id),
        name_text = 'ℹ️ ' + get_word('name', chat_id=chat_id),
        lastname = lastname,
        firstname = firstname,
        phone_text = get_word('phone', chat_id=chat_id),
        phone = phone,
        car_info_text = get_word('car', chat_id=chat_id),
        color = get_color(color, chat_id=chat_id),
        brand = brand,
        model = model,
        autonum = autonum,

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
    # text1 = get_word('select point a', update)
    text2 = get_word('select address or location', update)
    text = f"{text2}"
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
    text = "{point_a_text}: {point_a}\n{price_text}: {price}\n\n{confirmation_text}".format(
        point_a_text = get_word('point a', update),
        point_a = point_a,
        price_text = get_word('price', update),
        price = price,
        confirmation_text = get_word('confirm order', update)
    )
    return text

def order_history_details_string(
    update,
    src, dst, starttime, endtime, amount, distance, 
    standtime, waittime, street, house, dststreet, dsthouse,
    autonum, color, brand, model, lastname, firstname, phone, taximeter_data
):
    text = "🕙 <b>{time}</b>\n\n<i>{point_a_text}:</i> {point_a}\n<i>{point_b_text}:</i> {point_b}\n"
    text += "<i>{amount_text}:</i> {amount}\n<i>{baggage_text}:</i> {baggage}\n<i>{distance_text}:</i> {distance} {metr}\n"
    text += "<i>{standtime_text}:</i> {standtime}\n<i>{waittime_text}:</i> {waittime}\n\n"
    text += "<i>{name_text}:</i> {lastname} {firstname}\n<i>{phone_text}:</i> {phone}\n"
    text += "<i>{car_info_text}:</i> {color} {brand} {model} | {autonum}\n"
    text = text.format(
        time = endtime.strftime("%d.%m.%Y %H:%M"),
        point_a_text = get_word('point a', update),
        point_a = src,
        point_b_text = get_word('point b', update),
        point_b = dst,
        amount_text = get_word('amount', update),
        amount = amount,
        baggage_text = get_word('baggage', update),
        baggage = float(taximeter_data['margin']) if 'margin' in taximeter_data else "",
        distance_text = get_word('distance', update),
        distance = distance,
        metr = get_word('meter', update),
        standtime_text = get_word('standtime', update),
        standtime = "{} {} {} {}".format(
            int(standtime) // 60 if standtime else standtime, 
            get_word('min.', update), 
            int(standtime) % 60 if standtime else standtime, 
            get_word('sek.', update)),
        waittime_text = get_word('waittime', update),
        waittime = waittime,
        name_text = get_word('driver name', update),
        lastname = lastname,
        firstname = firstname,
        phone_text = get_word('phone', update),
        phone = phone,
        car_info_text = get_word('car', update),
        color = get_color(color, update),
        brand = brand,
        model = model,
        autonum = autonum,

    )
    return text