import aiohttp
import asyncio
import json

from .forecast import Forecast

class Client:

    def __init__(self, session: aiohttp.ClientSession = None):
        self.__session = session or aiohttp.ClientSession()
    
    async def get(self, forecast: bool = False, days: int = 1):
        endpoint = 'https://ws.smn.gob.ar/map_items/weather'
        if forecast:
            if days > 4:
                raise ValueError('Forecast days must be less than 5')
            endpoint = f'https://ws.smn.gob.ar/map_items/forecast/{days}'
        async with self.__session.get(endpoint) as response:
            return Forecast(await response.json())
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.__session.close()