import aiohttp
import asyncio
import json

from typing import List, Union, Tuple
from .forecast import Forecast
from .constants import SMNConstants
from .exceptions import LimitExceeded, ForecastNotAvailable

class Client:
    '''Client for the SMN API'''
    __slots__ = ('__session',)

    def __init__(self, session: aiohttp.ClientSession = None):
        self.__session = session or aiohttp.ClientSession()
    
    async def get(self, forecast: str = 'now') -> Union[Forecast, List[Forecast]]:
        if forecast not in SMNConstants.AVAILABLE_FORECASTS:
            raise ForecastNotAvailable(f'The forecast "{forecast}" is not available.')
        if forecast == 'now':
            endpoint = SMNConstants.WEATHER_ENDPOINT
        else:
            day = forecast.split(' ')[0]
            endpoint = SMNConstants.FORECAST_ENDPOINT.format(days=day)
        try:
            async with self.__session.get(endpoint) as response:
                return Forecast(await response.json())
        except asyncio.TimeoutError:
            raise LimitExceeded('Could not get forecast, exceeded the limit of requests.')
        
    async def get_location(self) -> Tuple[str, float, float]:
        try:
            async with self.__session.get(SMNConstants.IP_API_ENDPOINT) as response:
                data = await response.json()
                if response.status != 200:
                    raise LimitExceeded('Could not get location, exceeded the limit of requests.')
                return data['regionName'], float(data['lat']), float(data['lon'])
        except asyncio.TimeoutError:
            raise LimitExceeded('Could not get location, exceeded the limit of requests.')
        
    async def __aenter__(self) -> 'Client':
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.__session.close()