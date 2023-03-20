from datetime import datetime, date, timedelta
import requests
import json

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

def send_request(url, data, type='get'):
    if type == 'get':
        response = json.loads(requests.get(url, params=data).content)
    else:
        response = json.loads(requests.post(url, data=data).content)

    return response