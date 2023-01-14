import aiohttp
import asyncio
from typing import List, Union, Tuple, Dict

from .forecast import Forecast
from .constants import SMNConstants
from .exceptions import LimitExceeded, ForecastNotAvailable

class Client:
    '''The client core class.'''
    __slots__ = ('__session',)

    def __init__(self, session: aiohttp.ClientSession = None):
        '''
        Initializes the client instance.

        Args:
            session (aiohttp.ClientSession, optional): The session to use. Defaults to None.
        '''
        self.__session = session or aiohttp.ClientSession()
    
    async def __get(self, endpoint: str) -> Dict:
        '''
        Makes a GET request to the given endpoint.

        Args:
            endpoint (str): The endpoint to make the request to.
        Raises:
            LimitExceeded: If the limit of requests per minute is exceeded.
        Returns:
            Dict: The response as a dictionary.
        '''
        try:
            async with self.__session.get(endpoint) as response:
                return await response.json()
        except asyncio.TimeoutError:
            raise LimitExceeded('Could not get forecast, exceeded the limit of requests.')

    async def get(self, forecast: str = 'now') -> Union[Forecast, List[Forecast]]:
        '''
        Gets the forecast for the given location.

        Args:
            forecast (str, optional): The forecast to get. Defaults to 'now'.
        Raises:
            ForecastNotAvailable: If the forecast is not available for the given location.
        Returns:
            Union[Forecast, List[Forecast]]: The forecast or list of forecasts.
        '''
        if forecast not in SMNConstants.AVAILABLE_FORECASTS:
            raise ForecastNotAvailable(f'The forecast "{forecast}" is not available.')
        if forecast == 'now':
            endpoint = SMNConstants.WEATHER_ENDPOINT
        else:
            endpoint = SMNConstants.FORECAST_ENDPOINT.format(days=forecast.split(' ')[0])
        return Forecast(await self.__get(endpoint))
        
    async def get_location(self) -> Tuple[str, float, float]:
        '''
        Gets the location of the client. You can use this to get the nearest forecast.

        Returns:
            Tuple[str, float, float]: The province, latitude and longitude of the client.
        '''
        data = await self.__get(SMNConstants.IP_API_ENDPOINT)
        return data['regionName'], float(data['lat']), float(data['lon'])
        
    async def __aenter__(self) -> 'Client':
        '''
        Async context manager for the client.

        Returns:
            Client: The client.
        '''
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        '''
        Async context manager for the client.

        Args:
            exc_type (Exception): The exception type.
            exc_val (Exception): The exception value.
            exc_tb (Exception): The exception traceback.
        '''
        await self.__session.close()
    
    def __del__(self) -> None:
        '''
        Closes the session when the client is deleted.
        '''
        if not self.__session.closed:
            asyncio.run(self.__session.close())
        
    def __repr__(self) -> str:
        '''
        Returns the representation of the client.

        Returns:
            str: The representation of the client.
        '''
        return f'<Client session={self.__session}>'
    
    def __str__(self) -> str:
        '''
        Returns the string representation of the client.

        Returns:
            str: The string representation of the client.
        '''
        return self.__repr__()
    