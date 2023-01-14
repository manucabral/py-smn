import asyncio
import smn

async def main():
    async with smn.Client() as client:
        forecast_now = await client.get(forecast='now')
        province, lat, lon = await client.get_location()
        # province is not used in this example, but it's a good idea to use it!
        nearest = forecast_now.nearest(lat, lon)
        print(nearest.name)
        print(nearest.weather['temp'])

if __name__ == '__main__':
    asyncio.run(main())
