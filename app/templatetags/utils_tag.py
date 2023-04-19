from django import template
from app.utils import *
from app.resources.strings import lang_dict

register = template.Library()

@register.filter()
def index(l, i):
    try:
        return l[i]
    except:
        return ''

@register.filter()
def message_date(date: datetime):
    if not date:
        return ''
    now = datetime.now()
    today = datetime(
        year=now.year, month=now.month, day=now.day, 
        hour=date.hour, minute=date.minute, 
        second=date.second, microsecond=date.microsecond)
    days = (today - date).days
    if days == 0:
        r = date.strftime("%H:%M")
    elif days == 1:
        r = lang_dict['yesterday'][1]
    elif days < 7:
        r = date.strftime("%A")
    else:
        if today.year == date.year:
            month = lang_dict[date.strftime("%B").lower()][1]
            r = "{} {}".format(date.strftime("%d"), month)
        else:
            r = date.strftime("%d.%m.%y")
    return r

@register.filter()
def message_day(date: datetime):
    if not date:
        return ''
    now = datetime.now()
    today = datetime(
        year=now.year, month=now.month, day=now.day, 
        hour=date.hour, minute=date.minute, 
        second=date.second, microsecond=date.microsecond)
    days = (today - date).days
    if days == 0:
        r = lang_dict['today'][1]
    elif days == 1:
        r = lang_dict['yesterday'][1]
    else:
        if today.year == date.year:
            month = lang_dict[date.strftime("%B").lower()][1]
            r = "{} {}".format(date.strftime("%d"), month)
        else:
            month = lang_dict[date.strftime("%B").lower()][1]
            r = "{} {} {}".format(date.strftime("%d"), month, date.strftime("%Y"))
    return r