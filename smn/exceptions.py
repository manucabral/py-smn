class LimitExceeded(Exception):
    """Raised when the limit of requests per minute is exceeded."""

class ForecastNotAvailable(Exception):
    """Raised when the forecast is not available for the given location."""