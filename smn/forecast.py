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
            if all(value in weather_station.get(key) for key, value in kwargs.items()):
                yield WeatherStation(**weather_station)
    
    
            