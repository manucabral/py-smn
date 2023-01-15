class SMNConstants:
    '''Constants used by the SMN API'''
    API_ENDPOINT = 'https://ws.smn.gob.ar/map_items/'
    STATIC_ENDPOINT = f'https://ssl.smn.gob.ar/dpd/zipopendata.php?dato='
    API_WEATHER_ENDPOINT = f'{API_ENDPOINT}/map_items/weather/'
    API_FORECAST_ENDPOINT = f'{API_ENDPOINT}/map_items/forecast/{{days}}'
    API_IP_ENDPOINT = 'http://ip-api.com/json'
    AVAILABLE_FORECASTS = ['now', '1 day', '2 days', '3 days', '4 days']