import requests
lat = '55.7558'

lon = '37.6173'

api_key = '4213b32140601bf64cef176f3f5b2add'

url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}/'

response = requests.get(url)

data = response.json()

print(data)

