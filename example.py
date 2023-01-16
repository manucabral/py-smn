import asyncio
import smn

async def nearest_static():
    # Let's get the nearest weather station to the client and print the temperature.
    async with smn.Client() as client:
        # Get the static forecast.
        forecast_now = await client.get_static()
        # Get the location using your IP.
        # NOTE: province is not used in this example, but you can use it to filter the weather stations.
        province, lat, lon = await client.get_location()
        # Get the nearest weather station.
        nearest_forecast = forecast_now.nearest(lat, lon)
        # Now we can get the temperature and more.
        temp = nearest_forecast.weather['temp']
        station_name = nearest_forecast.name
        print(f'The temperature in {station_name} is {temp}°C')

async def all_static():
    # Let's get all the weather stations.
    async with smn.Client() as client:
        # Get the static forecast.
        forecast_now = await client.get_static()
        # Now we can get all the weather stations using a simple for loop.
        for weather_station in forecast_now.all():
            print(weather_station)

async def filtering():
    # Let's get all the weather stations in Buenos Aires.
    async with smn.Client() as client:
        # Get the static forecast.
        forecast_now = await client.get_static()
        # Now we can get filter by province and iterate over the result.
        # NOTE: you can use more than one filter at the same time.
        for weather_station in forecast_now.filter(province='BUENOS AIRES'):
            print(weather_station)

if __name__ == '__main__':
    asyncio.run(nearest_static())
    asyncio.run(all_static())
    asyncio.run(filtering())