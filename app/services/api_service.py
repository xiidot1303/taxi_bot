from app.utils import send_request
from config import API_KEY as api_key, API_URL as api_url

data = {'api_key': api_key}

def get_services():
    url = api_url + '/services'
    response = send_request(url, data)
    return response['response']['services']

def get_streets(city_id):
    url = api_url + '/streets'
    data['city_id'] = city_id
    response = send_request(url, data)
    return response['response']['streets']
