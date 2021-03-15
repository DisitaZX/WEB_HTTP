import sys
from io import BytesIO
import requests
from PIL import Image
from math import sqrt


toponym_to_find = " ".join(sys.argv[1:])
search_api_server = "https://search-maps.yandex.ru/v1/"
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
address_ll = "37.588392,55.734036"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)
json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    pass
json_response = response.json()
organization = json_response["features"][0]
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]
point = organization["geometry"]["coordinates"]
distance = sqrt((float(toponym_longitude) - float(point[0]))**2 - (float(toponym_lattitude) - float(point[1]))**2)
org_point = "{0},{1}".format(point[0], point[1])
delta = [str((float(toponym_longitude) - float(point[0])) * 2),
         str((float(toponym_lattitude) - float(point[1])) * 2)]
if float(delta[0]) < 0:
    delta[0] = delta[0][1:]
if float(delta[1]) < 0:
    delta[1] = delta[1][1:]
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([delta[0], delta[1]]),
    "l": "map",
    "pt": "{0},pm2dgl".format(org_point)
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(
    response.content)).show()
snippet = {'Адрес': organization['properties']['CompanyMetaData']['address'],
           'Название': organization['properties']['CompanyMetaData']['name'],
           'Часы работы': organization['properties']['CompanyMetaData']['Hours']['text'],
           'Расстояние до аптеки': f'{int(distance * 100000)} метров'}
for key, val in snippet.items():
    print(f'{key}: {val}')
