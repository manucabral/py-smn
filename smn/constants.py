class SMNConstants:
    '''Constants used by the SMN API'''
    BASE_ENDPOINT = 'https://ws.smn.gob.ar'
    WEATHER_ENDPOINT = f'{BASE_ENDPOINT}/map_items/weather'
    FORECAST_ENDPOINT = f'{BASE_ENDPOINT}/map_items/forecast/{{days}}'
    IP_API_ENDPOINT = 'http://ip-api.com/json'
    AVAILABLE_FORECASTS = ['now', '1 day', '2 days', '3 days', '4 days']