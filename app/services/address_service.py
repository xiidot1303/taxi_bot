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

def get_street_by_pk(pk):
    obj = get_object_or_404(Street, pk=pk)
    return obj

def filter_streets_by_title_regex(city, text_en, text_ru, text):
    if city:
        streets = Street.objects.filter(city = city)
    else:
        streets = Street.objects.filter()

    streets = streets.filter(
        Q(title__iregex=text_en) | Q(title__iregex=text_ru) | Q(title__icontains=text)
        )
    return streets

def cities_all():
    return City.objects.all()

def get_city_by_title(title):
    query = City.objects.filter(title=title)
    return query[0] if query else None