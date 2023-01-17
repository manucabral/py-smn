import aiohttp
import asyncio
import os
from zipfile import ZipFile
from typing import List, Union, Tuple, Dict

from .forecast import Forecast
from .constants import SMNConstants
from .exceptions import LimitExceeded, ForecastNotAvailable
from .parser import Parser

class Client:
    '''
    The client core class.
    
    Args:
        session (aiohttp.ClientSession, optional): The session to use. Defaults to None.
        keep_data (bool, optional): If the data should be kept. Defaults to False.
    '''
    __slots__ = ('__session', 'keep_data')

    def __init__(self, session: aiohttp.ClientSession = None, keep_data: bool = False):
        '''Initializes the client instance.'''
        self.__session = session or aiohttp.ClientSession()
        self.keep_data = keep_data
    
    async def __get(self, endpoint: str, save: bool = False, format: str = '.txt') -> Dict:
        '''
        Makes a GET request to the given endpoint.

        Args:
            endpoint (str): The endpoint to make the request to.
            save (bool, optional): Saves the data in a file. Defaults to False.
            format (str, optional): The format of the file. Defaults to '.txt'.
        Raises:
            LimitExceeded: If the limit of requests per minute is exceeded.
        Returns:
            Dict: The response as a dictionary.
        '''
        try:
            async with self.__session.get(endpoint) as response:
                if save and response.status == 200:
                    filename = f'd{format}'
                    with open(filename, 'wb') as output_file:
                        async for chunk in response.content.iter_chunked(10):
                            output_file.write(chunk)
                    # If the format is '.zip', extracts only the first file.
                    if format == '.zip':
                        with ZipFile(filename) as zipfile:
                            extracted_file = zipfile.namelist()[0]
                            zipfile.extractall()
                        return extracted_file
                    return filename
                return await response.json()
        except asyncio.TimeoutError:
            raise LimitExceeded('Could not get forecast, exceeded the limit of requests.')

    async def get_static(self) -> Forecast:
        '''
        Gets the static data from the SMN Open Data.

        Returns:
            Forecast: The forecast with the static data.
        '''
        # NOTE: The data is in a zip file, set the format to '.zip'
        tf_filename = await self.__get(SMNConstants.STATIC_ENDPOINT + 'tiepre', save=True, format='.zip')
        ws_filename = await self.__get(SMNConstants.STATIC_ENDPOINT + 'estaciones', save=True, format='.zip')
        weather_stations = Parser.ws_to_json(filename=ws_filename)
        weather_data = Parser.csv_to_json(filename=tf_filename)
        if len(weather_data) == 0:
            raise ForecastNotAvailable('No updated data available for today. Try again later.')
        return Forecast(Parser.merge_data(weather_stations, weather_data))

    async def get(self, forecast: str = 'now') -> Union[Forecast, List[Forecast]]:
        '''
        Gets the forecast data from the SMN API.

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
            endpoint = SMNConstants.API_ENDPOINT + 'weather'
        else:
            endpoint = SMNConstants.API_ENDPOINT + f'forecast/{forecast.split(" ")[0]}'
        return Forecast(await self.__get(endpoint))

    async def get_location(self) -> Tuple[str, float, float]:
        '''
        Gets the location of the client. You can use this to get the nearest forecast.

        Returns:
            Tuple[str, float, float]: The province, latitude and longitude of the client.
        '''
        data = await self.__get(SMNConstants.API_IP_ENDPOINT)
        return data['regionName'], float(data['lat']), float(data['lon'])
        
    async def __aenter__(self) -> 'Client':
        '''
        Async context manager for the client.

        Returns:
            Client: The client.
        '''
        return self
    
    def __clear(self) -> None:
        '''
        Clear all the data downloaded.
        '''
        if self.keep_data:
            return
        for file in os.listdir():
            if file.endswith('.txt') or file.endswith('.zip'):
                os.remove(file)

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        '''
        Async context manager for the client.

        Args:
            exc_type (Exception): The exception type.
            exc_val (Exception): The exception value.
            exc_tb (Exception): The exception traceback.
        '''
        await self.__session.close()
        self.__clear()
    
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