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