from typing import Dict, Optional
import requests
from datetime import datetime
from dataclasses import dataclass
from src.config.settings import Settings
from src.utils.logger import Logger
from src.exceptions.weather_exceptions import WeatherAPIException

@dataclass
class WeatherResponse:
    """Estrutura de resposta para dados meteorológicos."""
    success: bool
    data: Dict
    status: int
    message: str = ""

class WeatherService:
    """Serviço para obter dados meteorológicos."""
    
    def __init__(self):
        """Inicializa o serviço com configurações e logger."""
        self.logger = Logger(__name__)
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.api_key = Settings.OPENWEATHER_API_KEY
        self.timeout = Settings.API_TIMEOUT  # Moved to settings
        
    def get_weather(self, city: str = "Lisbon", country: str = "PT") -> WeatherResponse:
        """
        Obtém dados meteorológicos de uma cidade.
        
        Args:
            city (str): Nome da cidade
            country (str): Código do país ISO 3166
            
        Returns:
            WeatherResponse: Objeto contendo dados meteorológicos ou erro
            
        Raises:
            WeatherAPIException: Se houver erro na API
        """
        try:
            self._validate_api_key()
            
            params = self._build_params(city, country)
            response = self._make_request(params)
            
            return WeatherResponse(
                success=True,
                data=response.json(),
                status=200,
                message="Dados obtidos com sucesso"
            )
            
        except requests.Timeout:
            return self._handle_timeout_error(city)
            
        except requests.RequestException as e:
            return self._handle_request_error(e)
        
        except ValueError as e:
            return self._handle_validation_error(e)

    def _validate_api_key(self) -> None:
        """Valida se a API key está configurada."""
        if not self.api_key:
            raise ValueError("API key não configurada")

    def _build_params(self, city: str, country: str) -> Dict:
        """Constrói os parâmetros da requisição."""
        return {
            "q": f"{city},{country}",
            "appid": self.api_key,
            "units": "metric",
            "lang": "pt"
        }

    def _make_request(self, params: Dict) -> requests.Response:
        """Realiza a requisição HTTP."""
        response = requests.get(
            self.base_url, 
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response

    def _handle_timeout_error(self, city: str) -> WeatherResponse:
        """Trata erro de timeout."""
        error_msg = f"Timeout ao acessar API para {city}"
        self.logger.error(error_msg)
        return WeatherResponse(False, {}, 408, error_msg)

    def _handle_request_error(self, error: Exception) -> WeatherResponse:
        """Trata erros de requisição."""
        error_msg = f"Erro na requisição: {str(error)}"
        self.logger.error(error_msg)
        return WeatherResponse(False, {}, 500, error_msg)

    def _handle_validation_error(self, error: Exception) -> WeatherResponse:
        """Trata erros de validação."""
        error_msg = str(error)
        self.logger.error(error_msg)
        return WeatherResponse(False, {}, 400, error_msg)