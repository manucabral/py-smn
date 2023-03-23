"""
    This is a non official command line interface for @py-smn weather service client
    @author @leoarayav
    NOTE: This application is not intended to be used in production, it is just a test.
    TODO: Transform this application in a POO application and add more features, arguments, etc.
"""

from asyncio import run
from argparse import ArgumentParser
from smn import Client

async def get_province(province: str, name: str) -> None:
    async with Client() as client:
        fcast_now = await client.get(forecast="now")
        weather_stations = fcast_now.filter(province=province, name=name)
        for station in weather_stations:
            print(station.name, station.weather['temp'])

async def get_nearest_weather() -> None:
    async with Client() as client:
        fcast_now = await client.get(forecast="now")
        province, lat, lon = await client.get_location()
        nearest_forecast = fcast_now.nearest(lat, lon)
        temp = nearest_forecast.weather['temp']
        station_name = nearest_forecast.name
        print(f'The temperature in {station_name} is {temp}°C')

def get_arguments() -> ArgumentParser:
    '''
        Get arguments from command line.

        Returns:
            ArgumentParser
    '''
    parser = ArgumentParser(
        description='Non oficial @py-smn CLI client',
        epilog='Check main github repository for more information: https://github.com/manucabral/py-smn'
    )
    parser.add_argument("--province", help="Province to get data from")
    parser.add_argument("--name", help="Name of the city to get data from")
    parser.add_argument("nearest", help="Get the nearest weather station")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_arguments()
    if args.province: 
        run(get_province(args.province, args.name))
    elif args.nearest: 
        run(get_nearest_weather())