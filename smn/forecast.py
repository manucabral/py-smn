import json
from typing import Generator

from .weather_station import WeatherStation

class Forecast:
    '''The forecast class, contains all the weather stations.'''
    __slots__ = ('__data_json',)

    def __init__(self, data_json: dict):
        '''Initializes the forecast instance.'''
        self.__data_json = data_json
    
    def __repr__(self) -> str:
        '''Returns the forecast as a string.'''
        return json.dumps(self.__data_json, indent=4)
    
    def __str__(self) -> str:
        '''Returns the forecast as a string.'''
        return f'<Forecast {len(self.__data_json)} items>'
    
    def filter(self, **kwargs) -> Generator[str, None, None]:
        '''
        Filters the weather stations by the given kwargs.
        Available kwargs: province, name, lat, lon
        Example: filter(province='Buenos Aires')

        Args:
            **kwargs: The kwargs to filter by.
        Yields:
            Generator[str, None, None]: The filtered weather stations.
        '''
        for weather_station in self.__data_json:
            # Convert lat and lon to float !IMPORTANT
            weather_station['lat'] = float(weather_station['lat'])
            weather_station['lon'] = float(weather_station['lon'])
            if all(value in weather_station.get(key) for key, value in kwargs.items()):
                yield WeatherStation(**weather_station)
    
    def all(self) -> Generator[str, None, None]:
        '''
        Gets all the weather stations.

        Yields:
            Generator[str, None, None]: The weather stations.
        '''
        for weather_station in self.__data_json:
            # Convert lat and lon to float !IMPORTANT
            weather_station['lat'] = float(weather_station['lat'])
            weather_station['lon'] = float(weather_station['lon'])
            yield WeatherStation(**weather_station)

    def __distance(self, lat1, lon1, lat2, lon2) -> float:
        '''
        Calculates the distance between two points.

        Args:
            lat1 (float): The latitude of the first point.
            lon1 (float): The longitude of the first point.
            lat2 (float): The latitude of the second point.
            lon2 (float): The longitude of the second point.
        Returns:
            float: The distance between the two points.
        '''
        if lat1 == lat2 and lon1 == lon2:
            return 0
        return (lat1 - lat2) ** 2 + (lon1 - lon2) ** 2

    def nearest(self, lat: float, lon: float) -> WeatherStation:
        '''
        Gets the nearest weather station to the given coordinates.

        Args:
            lat (float): The latitude of the point.
            lon (float): The longitude of the point.
        Returns:
            WeatherStation: The nearest weather station.
        '''
        weather_stations = list(self.filter())
        lamda = lambda weather_station : self.__distance(lat, lon, weather_station.lat, weather_station.lon)
        return min(weather_stations, key=lamda)