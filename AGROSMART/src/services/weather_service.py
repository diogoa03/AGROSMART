from typing import Dict, Optional
import requests
from datetime import datetime
from dataclasses import dataclass
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
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
        self.timeout = Settings.API_TIMEOUT
        self.session = self._create_session()
        
    def _create_session(self) -> requests.Session:
        """Cria e configura uma sessão HTTP reutilizável."""
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            max_retries=3,
            pool_connections=10,
            pool_maxsize=10
        )
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

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
            self._validate_input(city, country)
            self._validate_api_key()
            
            params = self._build_params(city, country)
            response = self._make_request(params)
            
            weather_data = response.json()
            self._validate_response(weather_data)
            
            self.logger.info(
                f"Dados meteorológicos obtidos com sucesso para {city}, {country}",
                extra={
                    "city": city,
                    "country": country,
                    "temperature": weather_data.get("main", {}).get("temp")
                }
            )
            
            return WeatherResponse(
                success=True,
                data=weather_data,
                status=200,
                message="Dados obtidos com sucesso"
            )
            
        except requests.Timeout:
            return self._handle_timeout_error(city)
            
        except requests.RequestException as e:
            return self._handle_request_error(e)
        
        except ValueError as e:
            return self._handle_validation_error(e)

    def _validate_input(self, city: str, country: str) -> None:
        """Valida os parâmetros de entrada."""
        if not city or not isinstance(city, str):
            raise ValueError("Cidade inválida")
        if not country or not isinstance(country, str) or len(country) != 2:
            raise ValueError("Código do país inválido (deve ser ISO 3166-2)")

    def _validate_api_key(self) -> None:
        """Valida se a API key está configurada."""
        if not self.api_key:
            raise ValueError("API key não configurada")

    def _validate_response(self, data: Dict) -> None:
        """Valida a resposta da API."""
        if not data or "main" not in data:
            raise WeatherAPIException("Resposta da API inválida")

    def _build_params(self, city: str, country: str) -> Dict:
        """Constrói os parâmetros da requisição."""
        return {
            "q": f"{city},{country}",
            "appid": self.api_key,
            "units": "metric",
            "lang": "pt"
        }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((requests.Timeout, requests.ConnectionError)),
        before_sleep=lambda retry_state: Logger(__name__).warning(
            f"Tentativa {retry_state.attempt_number} falhou, tentando novamente..."
        )
    )
    def _make_request(self, params: Dict) -> requests.Response:
        """Realiza a requisição HTTP com retry."""
        try:
            response = self.session.get(
                self.base_url,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"Erro na requisição: {str(e)}",
                extra={
                    "params": params,
                    "status_code": getattr(response, "status_code", None),
                    "error_type": type(e).__name__
                }
            )
            raise

    def _handle_timeout_error(self, city: str) -> WeatherResponse:
        """Trata erro de timeout."""
        error_msg = f"Timeout ao acessar API para {city}"
        self.logger.error(error_msg, extra={"city": city})
        return WeatherResponse(False, {}, 408, error_msg)

    def _handle_request_error(self, error: Exception) -> WeatherResponse:
        """Trata erros de requisição."""
        error_msg = f"Erro na requisição: {str(error)}"
        self.logger.error(
            error_msg,
            extra={"error_type": type(error).__name__}
        )
        return WeatherResponse(False, {}, 500, error_msg)

    def _handle_validation_error(self, error: Exception) -> WeatherResponse:
        """Trata erros de validação."""
        error_msg = str(error)
        self.logger.error(
            error_msg,
            extra={"error_type": "ValidationError"}
        )
        return WeatherResponse(False, {}, 400, error_msg)