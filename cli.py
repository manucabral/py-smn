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

def get_arguments() -> ArgumentParser:
    parser = ArgumentParser(
        description='Non oficial @py-smn CLI client',
        epilog='Check main github repository for more information: https://github.com/manucabral/py-smn'
    )
    """
    Here goes arguments for the script to use
    :author @leoarayav
    """
    parser.add_argument("--province", help="Province to get data from")
    parser.add_argument("--name", help="Name of the city to get data from")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_arguments()
    if args.province: run(get_province(args.province, args.name))