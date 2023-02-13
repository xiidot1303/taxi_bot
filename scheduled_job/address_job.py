from app.services.api_service import *
from app.services.address_service import *

def update_streets():
    for city in filter_cities():
        try:
            streets_list = get_streets(city_id=city.city_id)
            for street in streets_list:
                get_or_create_street(street, city)
        except:
            pass

def update_cities():
    try:
        cities_list = get_services()
        for city in cities_list:
            get_or_create_city(city['name'], city['city_id'])   
    except:
        pass