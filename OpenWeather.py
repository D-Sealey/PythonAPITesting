#!/usr/bin/python3

#need to execute below to get requests module
#pip install requests

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

def get_geo_loc(city :str ,state :str =''):
    '''Returns lat and lon from city name'''
    geo_url='http://api.openweathermap.org/geo/1.0/direct'

    if state:
        geo_payload={
            'q':f'{city}, {state}',
            'appid':api_key
        }
    else:
        geo_payload={
            'q':f'{city}',
            'appid':api_key
        }

    #--this is the API call--
    geocode=requests.get(geo_url,geo_payload)

    if geocode.json():
        lat=geocode.json()[0]['lat']
        # print(f"Lat: {(lat:=geocode.json()[0]['lat'])}")
        lon=geocode.json()[0]['lon']
        # print(f"Lon: {(lon:=geocode.json()[0]['lon'])}")
    else:
        print(f'Cannot find city {city}.')
        lat,lon=None,None
    return lat,lon

def get_cur_weather(lat:float,lon:float):
    '''Returns weather data from provided lat and lon'''
    url='https://api.openweathermap.org/data/2.5/weather'
    params={
        'lat':lat,
        'lon':lon,
        'units':'imperial',
        'appid':api_key
    }

    #--this is the API call--
    current_weather=requests.get(url,params)
    '''equivalent to
    https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={api_key}
    '''

    return current_weather.json()

class City:
    def __init__(self,name:str,lat:float=None,lon:float=None):
        self.name=name
        if lat and lon:
            self.lat=lat
            self.lon=lon
        else:
            self.lat,self.lon=get_geo_loc(name)
        ...
    def get_weather(self):
        self.weather=get_cur_weather(self.lat,self.lon)
        return self.weather
        ...
    def temp(self):
        if not (self.lat and self.lon):
            print('Need a valid location.')
            return None
        temp=self.get_weather()['main']['temp']
        feels=self.get_weather()['main']['feels_like']
        print(f'{self.name}')
        print(f'Temp is: {temp} F')
        print(f'Feels like: {feels} F')
    ...


#---TESTING---
city='London'
lat,lon=get_geo_loc(city)
weather=get_cur_weather(lat,lon)
# pprint(weather)

city='Saskatoon'
lat,lon=get_geo_loc(city)
weather=get_cur_weather(lat,lon)
# pprint(weather)

'''Class tests'''
Tokyo=City('Tokyo')
# pprint(Tokyo.get_weather())

Sask=City('Saskatoon')
Sask.temp()
# pprint(Sask.get_weather())

OKC=City('Oklahoma City')
OKC.temp()

OKC_test=City('OKC',35,-97)
OKC_test=City('OKC')
OKC_test.temp()

'''Geocoding tests'''
geo_url='http://api.openweathermap.org/geo/1.0/direct'

city='London'
geo_payload={
    'q':f'{city}',
    'appid':api_key,
    'limit':3 #defaults to 1 if limit not specified
}

#--this is the important API part--
geocode=requests.get(geo_url,geo_payload)

# pprint(geo_payload)
# pprint(geocode.json())
