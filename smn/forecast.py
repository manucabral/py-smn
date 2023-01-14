import json
from typing import Generator

from .weather_station import WeatherStation

class Forecast:
    __slots__ = ('__data_json',)

    def __init__(self, data_json: dict):
        self.__data_json = data_json
    
    def __repr__(self) -> str:
        return json.dumps(self.__data_json, indent=4)
    
    def __str__(self) -> str:
        return f'<Forecast {len(self.__data_json)} items>'
    
    def filter(self, **kwargs) -> Generator[str, None, None]:
        '''Filter the forecast by the given kwargs'''
        for weather_station in self.__data_json:
            # Convert lat and lon to float !IMPORTANT
            weather_station['lat'] = float(weather_station['lat'])
            weather_station['lon'] = float(weather_station['lon'])
            if all(value in weather_station.get(key) for key, value in kwargs.items()):
                yield WeatherStation(**weather_station)
    
    def __distance(self, lat1, lon1, lat2, lon2) -> float:
        '''Get the distance between two points'''
        if lat1 == lat2 and lon1 == lon2:
            return 0
        return (lat1 - lat2) ** 2 + (lon1 - lon2) ** 2

    def nearest(self, lat: float, lon: float) -> WeatherStation:
        '''Get the nearest weather station to the given lat and lon'''
        weather_stations = list(self.filter())
        lamda = lambda weather_station : self.__distance(lat, lon, weather_station.lat, weather_station.lon)
        return min(weather_stations, key=lamda)
            