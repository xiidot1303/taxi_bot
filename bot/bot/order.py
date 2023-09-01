from bot.bot import *

def to_the_get_point_a(update, context):
    # text on message
    text1 = get_word('select point a', update)
    text2 = select_point_a_string(update)
    # create inline button to switch to inline query
    location_req_markup = request_location_keyboard(update)
    markup = selecting_address_keyboard(update)
    # bot_send_and_delete_message(update, context, text, reply_markup=reply_keyboard_remove())
    bot_send_message(update, context, text1, location_req_markup)
    msg = update_message_reply_text(update, text2, markup)
    set_last_msg_and_markup(context, msg, markup)
    return GET_POINT_A

def _to_the_get_point_a_house(update, context):
    text = get_word('type house number', update)
    markup = selecting_address_house_keyboard(update)
    msg = update_message_reply_text(update, text, markup)
    set_last_msg_and_markup(context, msg, markup)
    return GET_POINT_A_HOUSE


def _to_the_get_point_b(update, context):
    # text on message
    street = context.user_data['src_street']
    house = context.user_data['src_house']
    text = select_point_b_string(update, street, house)
    # create inline button to switch to inline query
    markup = selecting_address_with_skip_keyboard(update)
    bot_send_and_delete_message(update, context, text, reply_markup=reply_keyboard_remove())
    msg = update_message_reply_text(update, text, markup)
    set_last_msg_and_markup(context, msg, markup)
    return GET_POINT_B

def _to_the_get_point_b_house(update, context):
    text = get_word('type house number', update)
    markup = selecting_address_house_keyboard(update)
    msg = update_message_reply_text(update, text, markup)
    set_last_msg_and_markup(context, msg, markup)
    return GET_POINT_B_HOUSE

def _to_the_confirm_order(update, context):
    data = context.user_data
    bot_user = get_object_by_update(update)
    # calculate order by data and get price, distance and token
    price, distance, token = calculate_order_pre_cost_api(
        bot_user.phone,
        data['src'], data['dst'], data['src_street'], data['src_house'],
        data['dst_street'], data['dst_house'], 
        data['src_lat'] if 'src_lat' in data else None, 
        data['src_lon'] if 'src_lon' in data else None, 
        data['dst_lon'] if 'dst_lon' in data else None, 
        data['dst_lat'] if 'dst_lat' in data else None, 
        data['service_id']
    )
    # make text for message
    text = order_details_before_confirmation_string(
        update, data['src_street'], data['src_house'], 
        data['dst_street'], data['dst_house'], price, distance)
    markup = confirm_order_keyboard(update)
    msg = update_message_reply_text(update, text, markup)
    # save token to user_data
    context.user_data['token'] = token
    # save last msg
    set_last_msg_and_markup(context, msg, markup)
    return CONFIRM_ORDER

def _to_the_order_process(update, context):
    data = context.user_data
    # get token from user_data
    token = context.user_data['token']
    # get bot user
    bot_user = get_object_by_update(update)
    # create order api
    status, uuid_or_msg = create_order_api(bot_user.phone, token)
    # check status, if error send message
    if not status:
        update_message_reply_text(update, uuid_or_msg)
        return
    # create order
    order = create_order(
        bot_user, uuid_or_msg, data['src'], data['dst'], 
        data['src_street'], data['src_house'],
        data['dst_street'], data['dst_house'], 
        data['src_lat'] if 'src_lat' in data else None, 
        data['src_lon'] if 'src_lon' in data else None, 
        data['dst_lon'] if 'dst_lon' in data else None, 
        data['dst_lat'] if 'dst_lat' in data else None, 
        data['service_id']
    )
    # send message
    text = get_word('order in process', update)
    markup = ReplyKeyboardMarkup(
        keyboard=[[get_word('cancel order', update)]], resize_keyboard=True
        )
    msg = update_message_reply_text(update, text, markup)
    # set data  to user_data
    context.user_data['order'] = order
    # save last msg
    set_last_msg_and_markup(context, msg, markup)
    return ORDER_PROCESS

######## POINT A ########

@ignore_start
def get_point_a_query(update, context):
    update = update.callback_query
    # check, is data back
    if update.data == 'back':
        bot_delete_message(update, context)
        main_menu(update, context)
        return ConversationHandler.END

@ignore_start
def get_point_a(update, context):
    bot_send_chat_action(update, context)
    # identify message type, location or text
    if location := update.message.location:
        # get coordinates from dict
        lat, lon = get_location_coordinates(location)
        # remove inline keyboard from last message
        remove_inline_keyboards_from_last_msg(update, context)
        # check, is coordinates in available regions
        # if not region_by_coordinates_api(lat, lon):
        #     text = get_word('invalid location', update)
        #     bot_send_message(update, context, text)
        #     return to_the_get_point_a(update, context)
        # get address by coordinates
        address = get_address_by_coordinates(lat, lon)
        # save data to user_data
            # set point a type
        context.user_data['src'] = 'location'
        context.user_data['src_lat'] = lat
        context.user_data['src_lon'] = lon
        context.user_data['src_street'] = address
        context.user_data['src_house'] = ''
        context.user_data['service_id'] = None

        if context.user_data['next'] == GET_POINT_B:
            return _to_the_get_point_b(update, context)
        else:
            return _to_the_confirm_order(update, context)
    else:
        try:
            # get street_id
            street_title, street_id = split_text_and_text_id(update.message.text)
            street = get_street_by_pk(int(street_id))
            # remove inline keyboard from last messgae
            remove_inline_keyboards_from_last_msg(update, context)
            # save data to user data
                # set point a type
            context.user_data['src'] = 'address'
            context.user_data['src_street'] = street.title
            context.user_data['service_id'] = street.city.city_id
            # return _to_the_get_point_a_house(update, context)
            return _to_the_confirm_order(update, context)
        except Exception as ex:
            print(ex)
            bot_delete_message(update, context)

@ignore_start
def get_point_a_house(update, context):
    # get message text
    msg = update.message.text
    # check, is message back or skip
    if msg == get_word('back', update):
        # back to getting point a
        return to_the_get_point_a(update, context)
    elif msg == get_word('skip', update):
        # empty house value
        context.user_data['src_house'] = ""
    else:
        # save house to user_data
        context.user_data['src_house'] = msg

    if context.user_data['next'] == GET_POINT_B:
        return _to_the_get_point_b(update, context)
    else:
        return _to_the_confirm_order(update, context)

######## POINT B ########

@ignore_start
def get_point_b_query(update, context):
    update = update.callback_query
    # check, is data back
    if update.data == 'back':
        bot_delete_message(update, context)
        context.user_data['next'] = GET_POINT_B
        return to_the_get_point_a(update, context)
    elif update.data == 'skip':
        bot_delete_message(update, context)
        context.user_data['dst'] = ''
        context.user_data['dst_street'] = ''
        context.user_data['dst_house'] = ''
        return _to_the_confirm_order(update, context)

@ignore_start
def get_point_b(update, context):
    bot_send_chat_action(update, context)
    # identify message type, location or text
    if location := update.message.location:
        # get coordinates from dict
        lat, lon = get_location_coordinates(location)
        # remove inline keyboard from last messgae
        remove_inline_keyboards_from_last_msg(update, context)
        # check, is coordinates in available regions
        # if not region_by_coordinates_api(lat, lon):
        #     text = get_word('invalid location', update)
        #     bot_send_message(update, context, text)
        #     return _to_the_get_point_b(update, context)
        # get address by coordinates
        address = get_address_by_coordinates(lat, lon)
        # save data to user_data
            # set point a type
        context.user_data['dst'] = 'location'
        context.user_data['dst_lat'] = lat
        context.user_data['dst_lon'] = lon
        context.user_data['dst_street'] = address
        context.user_data['dst_house'] = ''
        return _to_the_confirm_order(update, context)
    else:
        try:
            # get street_id
            street_title, street_id = split_text_and_text_id(update.message.text)
            street = get_street_by_pk(int(street_id))
            # remove inline keyboard from last messgage
            remove_inline_keyboards_from_last_msg(update, context)
            # save data to user data
                # set point a type
            context.user_data['dst'] = 'address'
            context.user_data['dst_street'] = street.title
            return _to_the_get_point_b_house(update, context)
        except Exception as ex:
            print(ex)
            bot_delete_message(update, context)

@ignore_start
def get_point_b_house(update, context):
    # get message text
    msg = update.message.text
    # check, is message back or skip
    if msg == get_word('back', update):
        # back to getting point a
        return _to_the_get_point_b(update, context)
    elif msg == get_word('skip', update):
        # empty house value
        context.user_data['dst_house'] = ""
    else:
        # save house to user_data
        context.user_data['dst_house'] = msg

    return _to_the_confirm_order(update, context)

@is_start
def confirm_order(update, context):
    # get message text
    msg = update.message.text
    # check message status
    if msg == get_word('confirm', update):
        return _to_the_order_process(update, context)
    elif msg == get_word('change point a', update):
        # set next step after selecting point a
        context.user_data['next'] = CONFIRM_ORDER
        return to_the_get_point_a(update, context)
    elif msg == get_word('change point b', update):
        return _to_the_get_point_b(update, context)


@ignore_start
def order_process(update, context):
    # get message text
    msg = update.message.text
    if msg == get_word('cancel order', update):
        # get old order from user_data
        order = context.user_data['order']
        # get new order
        order = get_order_by_id(order.id)
        # check, can cancel order
        if order.status in [80, 10, 11, 1]:
            # cancel order
            cancel_order_api(order.uuid)
            main_menu(update, context)
            return ConversationHandler.END
    # ignore current message and delete
    bot_delete_message(update, context)
    return