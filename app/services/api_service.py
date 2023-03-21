from app.utils import send_request
from config import API_KEY as api_key, API_URL as api_url, DEBUG

data = {'api_key': api_key}

def get_services_api():
    url = api_url + '/services'
    response = send_request(url, data)
    return response['response']['services']

def get_streets_api(city_id):
    url = api_url + '/streets'
    data['city_id'] = city_id
    response = send_request(url, data)
    return response['response']['streets']

def calculate_order_pre_cost_api(
        phone, src, dst, src_street=None, src_house=None, dst_street=None, dst_house=None, 
        src_lat=None, src_lon=None, dst_lon=None, dst_lat=None, service_id=None
    ):
    url = api_url + '/order/pre_cost'
    data['phone'] = phone
    # identify src type
    if src == 'location':
        data['src_lat'] = src_lat
        data['src_lon'] = src_lon
    elif src == 'address':
        data['src_street'] = src_street
        data['src_house'] = src_house
    
    # identidy dst type
    if dst == 'location':
        data['dst_lat'] = dst_lat
        data['dst_lon'] = dst_lon
    elif dst == 'address':
        data['dst_street'] = dst_street
        data['dst_house'] = dst_house
    if service_id:
        data['service_id'] = service_id
    response = {}
    while not 'response' in response:
        response = send_request(url, data)
    
    return (
        response['response']['amount'], response['response']['distance'], 
        response['response']['token']
        )

def region_by_coordinates_api(lat, lon):
    url = api_url + '/region_by_coord'
    data['lat'] = lat
    data['lon'] = lon
    response = send_request(url, data)
    return response['response']['id'] if response['status'] == 'DONE' else None

def create_order_api(phone, token):
    url = api_url + '/order'
    data['phone'] = phone
    data['token'] = token
    # set comment  by debug mode
    if DEBUG:
        data['comment'] = 'TEST Гайрат акага'
    else:
        data['comment'] = 'From Telegram Bot'

    response = send_request(url, data, 'post')
    if response['status'] == 'DONE':
        return True, response['response']['uuid']
    elif response['status'] == 'ERROR':
        return False, response['error']['message']

def cancel_order_api(uuid):
    url = api_url + '/cancel_order'
    data['uuid'] = uuid
    response = send_request(url, data, 'post')
    return True if response['status'] == 'DONE' else False

def client_bonus_count(phone):
    url = api_url + '/client/bonus/count'
    data['phone'] = phone
    response = send_request(url, data)
    return response['response']['bonus']