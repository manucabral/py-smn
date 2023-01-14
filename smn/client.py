import aiohttp
import asyncio
import json

from typing import List, Union, Tuple
from .forecast import Forecast
from .constants import SMNConstants

class Client:
    '''Client for the SMN API'''
    __slots__ = ('__session',)

    def __init__(self, session: aiohttp.ClientSession = None):
        self.__session = session or aiohttp.ClientSession()
    
    async def get(self, forecast: str = 'now', days: int = 1) -> Union[Forecast, List[Forecast]]:
        if forecast not in SMNConstants.AVAILABLE_FORECASTS:
            # TODO: Raise a custom exception :p
            raise ValueError(f'Forecast must be one of {self.__available_forecasts}')
        endpoint = SMNConstants.WEATHER_ENDPOINT if forecast == 'now' else SMNConstants.FORECAST_ENDPOINT.format(days=days)
        async with self.__session.get(endpoint) as response:
            return Forecast(await response.json())
    
    async def get_location(self) -> Tuple[str, float, float]:
        async with self.__session.get(SMNConstants.IP_API_ENDPOINT) as response:
            data = await response.json()
            if response.status != 200:
                # TODO: Raise a custom exception :p
                raise ValueError('Could not get location, exceeded the limit of requests.')
            return data['regionName'], float(data['lat']), float(data['lon'])

    async def __aenter__(self) -> 'Client':
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.__session.close()