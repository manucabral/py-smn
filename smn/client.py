import aiohttp
import asyncio
import json

from typing import List, Union
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
    
    async def __aenter__(self) -> 'Client':
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.__session.close()