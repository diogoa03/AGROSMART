import requests
from typing import Dict, Optional
from src.config.settings import Settings
from src.utils.logger import Logger

class WeatherService:
    """Serviço para obter dados meteorológicos da OpenWeatherMap."""
    
    def __init__(self):
        self.logger = Logger(__name__)
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.api_key = Settings.OPENWEATHER_API_KEY

    def get_weather(self, city: str = "Lisbon", country: str = "PT") -> Dict:
        """
        Obtém dados meteorológicos de uma cidade específica.
        
        Args:
            city (str): Nome da cidade
            country (str): Código do país (ISO 3166)
            
        Returns:
            Dict: Dados meteorológicos ou mensagem de erro
        """
        try:
            params = {
                "q": f"{city},{country}",
                "appid": self.api_key,
                "units": "metric",
                "lang": "pt"
            }
            
            response = requests.get(
                self.base_url, 
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            weather_data = response.json()
            self.logger.info(f"Dados meteorológicos obtidos para {city}")
            return weather_data
            
        except requests.Timeout:
            error_msg = f"Timeout ao acessar API para {city}"
            self.logger.error(error_msg)
            return {"erro": error_msg}
            
        except requests.RequestException as e:
            error_msg = f"Erro ao obter dados meteorológicos: {str(e)}"
            self.logger.error(error_msg)
            return {"erro": error_msg}