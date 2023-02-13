from app.services import *
from app.models import City, Street

def get_or_create_city(title, city_id):
    obj = City.objects.get_or_create(city_id=city_id)[0]
    obj.title = title
    obj.save()
    return obj

def filter_cities():
    return City.objects.all()

def get_or_create_street(title, city):
    obj = Street.objects.get_or_create(title=title, city=city)
    return obj