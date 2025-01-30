import os

import requests
from datetime import datetime, timedelta

def get_temp():
    lat = '55.7558'
    lon = '37.6173'
    api_key = os.getenv('API_WEATHER')


    url = f'https://projecteol.ru/api/weather/?lat={lat}&lon={lon}&date={datetime.now()}&token={api_key}'


    response = requests.get(url)


    data = response.json()
    first_forecast = data[0]
    temp_2_kelvin = first_forecast['temp_2']
    temp_2_celsius = temp_2_kelvin - 273.15
    return round(temp_2_celsius,2)


