def get_callback_query_data(update):
    data = update.data
    *args, result = str(data).split('_')
    return result