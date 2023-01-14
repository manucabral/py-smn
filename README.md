# py-smn
A free and open source Python library for retrieving weather data from the National Meteorological Service of Argentina (SMN). 

## Usage
```py
import asyncio
import smn

async def main():
    async with smn.Client() as client:
        forecast_now = await client.get(forecast='now')
        weather_stations = forecast_now.filter(province='Buenos Aires', name='La Plata')
        for weather_station in weather_stations:
            print(weather_station.name, weather_station.weather['temp'])

if __name__ == '__main__':
    asyncio.run(main())
```

## Constributions
All constributions, bug reports or fixes and ideas are welcome.
