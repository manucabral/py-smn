import json

class WeatherStation:
    '''The weather station class, contains all the weather station data.'''
    def __init__(self, **kwargs):
        '''Initializes the weather station instance.'''
        self.__dict__.update(kwargs)

    def __repr__(self) -> str:
        '''Returns the weather station as a string.'''
        return json.dumps(self.__dict__, indent=4)
    
    def __str__(self) -> str:
        '''Returns the weather station as a string.'''
        return f'<WeatherStation {self.name}>'
