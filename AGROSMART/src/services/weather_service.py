import requests
from src.config.settings import Settings


class WeatherService:
    """Serviço para obter dados meteorológicos da OpenWeatherMap."""

    @staticmethod
    def get_weather(city="Lisbon", country="PT"):
        params = {
            "q": f"{city},{country}",
            "appid": Settings.OPENWEATHER_API_KEY,
            "units": "metric",
            "lang": "pt"
        }
        response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)
        if response.status_code == 200:
            return response.json()
        return {"erro": "Não foi possível obter dados meteorológicos."}