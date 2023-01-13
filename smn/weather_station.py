import json

class WeatherStation:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self) -> str:
        return json.dumps(self.__dict__, indent=4)
    
    def __str__(self) -> str:
        return f'<WeatherStation {self.name}>'
