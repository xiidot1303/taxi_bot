
def filter_years_of_client_orders(bot_user):
    client_phone = bot_user.phone
    return [2022]

def filter_months_of_client_orders(bot_user, year):
    client_phone = bot_user.phone
    return [3,5]

def filter_days_of_client_orders(bot_user, year, month):
    client_phone = bot_user.phone
    return list(range(33))

def filter_orders_by_date(bot_user, day, month, year):
    return [1, 2]