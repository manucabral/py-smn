import re
from typing import Dict, List

class Parser:

    @staticmethod
    def grmn_to_decimal(degrees: str, minutes: str) -> float:
        '''Converts a GRMN coordinate to decimal.'''
        decimal = round(abs(float(degrees)) + abs(float(minutes)) / 60, 2)
        return decimal if degrees[0] != '-' else -decimal
    
    @staticmethod
    def csv_to_json(filename: str) -> List[Dict]:
        '''Converts a CSV file to JSON.'''
        with open(filename, 'r', errors='ignore') as file:
            lines = file.read().splitlines()
            weather_data = []
            for line in lines:
                data = line.split(';')
                try:
                    wind_data = data[8].split('  ')
                    wind_speed = wind_data[1]
                    wind_dir = wind_data[0]
                except:
                    continue
                weather_data.append({
                    'name': data[0].strip(),
                    'description': data[3],
                    'visibility': data[4],
                    'temp': data[5],
                    'tempDesc': data[6],
                    'humidity': data[7],
                    'wind_speed': wind_speed,
                    'wind_dir': wind_dir,
                    'pressure': data[9][:-3],
                })
        return weather_data

    @staticmethod
    def ws_to_json(filename: str) -> List[Dict]:
        '''Converts a Weather Station file to JSON.'''
        with open(filename, 'r', errors='ignore') as file:
            lines = file.read().splitlines()
            lines = lines[2:] # remove header
            weather_stations = []
            for line in lines:
                data = re.split(r'\s{2,}', line) # split by 2 or more spaces
                data = [i for i in data if i] # remove empty strings
                if len(data) < 2:
                    continue
                # name is soo long, TODO: fix that
                if 'SAENZ' in data[0] or 'MILITAR' in data[0]:
                    data.insert(1, 'undefined')
                weather_stations.append({
                    'name': data[0],
                    'province': data[1],
                    'lat': Parser.grmn_to_decimal(data[2], data[3]),
                    'lon': Parser.grmn_to_decimal(data[4], data[5]),
                    'height': data[6],
                    'int_number': data[7],
                })
        return weather_stations

    @staticmethod
    def merge_data(weather_stations: List[Dict], weather_data: List[Dict]):
        '''Merges the weather stations and weather data.'''
        for station in weather_stations:
            for data in weather_data:
                if data['name'].split(' ')[0].lower() in station['name'].lower():
                    station.update({'weather': data})
        return weather_stations