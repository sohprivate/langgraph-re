import os
import requests
from typing import Any, Dict

class WeatherAgent:
    """Agent responsible for retrieving weather data from OpenWeatherMap."""

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("WEATHER_API_KEY")
        if not self.api_key:
            raise ValueError("WEATHER_API_KEY not provided")

    def get_current_weather(self, location: str) -> Dict[str, Any]:
        """Fetch current weather data for a given location."""
        params = {"q": location, "appid": self.api_key, "units": "metric"}
        response = requests.get(f"{self.BASE_URL}/weather", params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_forecast(self, location: str) -> Dict[str, Any]:
        """Fetch 5 day / 3 hour forecast data."""
        params = {"q": location, "appid": self.api_key, "units": "metric"}
        response = requests.get(f"{self.BASE_URL}/forecast", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
