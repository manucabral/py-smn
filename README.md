# py-smn
A free and open source Python library for retrieving weather data from the National Meteorological Service of Argentina (SMN). 

## Note
This package offers two ways to obtain the requested data, the first is through the [API](https://ws.smn.gob.ar) of SMN and the second is by the public data offered by the official SMN [website](https://www.smn.gob.ar/descarga-de-datos). I recommend you use the second option since it is more accurate and is updated every day.


## Usage
Using static (recommended method)
```py
import asyncio
import smn

async def main():
    async with smn.Client() as client:
        forecast_now = await client.get_static()
        province, lat, lon = await client.get_location()
        nearest_forecast = forecast_now.nearest(lat, lon)
        print(nearest_forecast.weather['temp'])

if __name__ == '__main__':
    asyncio.run(main())
```

Using API
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
