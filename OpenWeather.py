#!/usr/bin/python3

import json,requests
from pprint import pprint

'''
Ref
https://openweathermap.org/current

Weather call
https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}

Direct Geocode
http://api.openweathermap.org/geo/1.0/direct?q={city name},{state code},{country code}&limit={limit}&appid={API key}

Zip Geocode
http://api.openweathermap.org/geo/1.0/zip?zip={zip code},{country code}&appid={API key}
'''

url='https://api.openweathermap.org/data/2.5/weather'
api_key='1c3cc2b116ecaa10232bfc058c368971'

def get_geo_loc(city :str ,state : str):
    geo_url='http://api.openweathermap.org/geo/1.0/direct'

    geo_payload={
        'q':f'{city}, {state}',
        'appid':api_key
    }

    geocode=requests.get(geo_url,geo_payload)
    # pprint(geo_payload)
    # pprint(geocode.json())

    # print(f"Name: {geocode.json()[0]['name']}")
    print(f"Lat: {(lat:=geocode.json()[0]['lat'])}")
    print(f"Lon: {(lon:=geocode.json()[0]['lon'])}")

    return lat,lon

def get_cur_weather(lat:float,lon:float):
    params={
        'lat':lat,
        'lon':lon,
        'units':'imperial',
        'appid':api_key
    }
    current_weather=requests.get(url,params)
    # pprint(current_weather.json())

    return current_weather.json()

def feels_like(city,state):
    lat,lon=get_geo_loc(city,state)
    weather=get_cur_weather(lat,lon)

    print(f'Name: {city}, {state}')
    feels=weather['main']['feels_like']
    print(f'Feels like: {feels}')

city='Saskatoon'
state='Saskatchewan'
feels_like(city,state)
print()

city='Oklahoma City'
state='Oklahoma'
feels_like(city,state)

lat,lon=get_geo_loc(city,state)
weather=get_cur_weather(lat,lon)
pprint(weather)
