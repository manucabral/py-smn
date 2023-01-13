import asyncio
import os
import smn

async def main():
    async with smn.Client() as client:
        forecast_now = await client.get(forecast='now')
        weather_stations = forecast_now.filter(province='Buenos Aires', name='La Plata')
        for weather_station in weather_stations:
            print(weather_station.name, weather_station.weather['temp'])

if __name__ == '__main__':
    asyncio.run(main())
