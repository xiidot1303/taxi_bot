from app.resources.strings import lang_dict
from datetime import datetime, date, timedelta

def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def datetime_now():
    now = datetime.now()
    return now

def time_now():
    now = datetime.now()
    return now.time()

def today():
    today = date.today()
    return today

def month_by_index(index):
    date = datetime(2022, int(index), 13)
    return date.strftime('%B')