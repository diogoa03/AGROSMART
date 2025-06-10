import pytest
import requests
from unittest.mock import Mock, patch
from datetime import datetime
from src.services.weather_service import WeatherService, WeatherResponse
from src.exceptions.weather_exceptions import WeatherAPIException

class TestWeatherService:
    @pytest.fixture
    def weather_service(self):
        """Fixture para criar instância do serviço com configurações de teste."""
        with patch('src.services.weather_service.settings') as mock_settings:
            mock_settings.OPENWEATHER_API_KEY = "test_key"
            mock_settings.API_TIMEOUT = 5
            return WeatherService()
    
    @pytest.fixture
    def mock_response(self):
        """Fixture para simular resposta da API."""
        mock = Mock()
        mock.json.return_value = {
            "main": {
                "temp": 25.6,
                "humidity": 65
            },
            "weather": [{"description": "céu limpo"}]
        }
        mock.status_code = 200
        return mock

    def test_get_weather_success(self, weather_service, mock_response):
        """Testa obtenção bem sucedida de dados meteorológicos."""
        with patch.object(weather_service.session, 'get', return_value=mock_response):
            response = weather_service.get_weather("Lisboa", "PT")
            
            assert response.success is True
            assert response.status == 200
            assert response.data["main"]["temp"] == 25.6
            assert "Dados obtidos com sucesso" in response.message

    def test_validate_input_invalid_city(self, weather_service):
        """Testa validação de cidade inválida."""
        with pytest.raises(ValueError) as exc:
            weather_service._validate_input("", "PT")
        assert "Cidade inválida" in str(exc.value)

    def test_validate_input_invalid_country(self, weather_service):
        """Testa validação de país inválido."""
        with pytest.raises(ValueError) as exc:
            weather_service._validate_input("Lisboa", "PRT")
        assert "Código do país inválido" in str(exc.value)

    def test_timeout_error(self, weather_service):
        """Testa tratamento de timeout."""
        with patch.object(weather_service.session, 'get', side_effect=requests.Timeout):
            response = weather_service.get_weather("Lisboa", "PT")
            
            assert response.success is False
            assert response.status == 408
            assert "Timeout" in response.message

    @pytest.mark.parametrize("exception,expected_status", [
        (requests.ConnectionError(), 500),
        (requests.RequestException(), 500),
        (ValueError("Cidade inválida"), 400)
    ])
    def test_error_handling(self, weather_service, exception, expected_status):
        """Testa diferentes cenários de erro."""
        with patch.object(weather_service.session, 'get', side_effect=exception):
            response = weather_service.get_weather("Lisboa", "PT")
            
            assert response.success is False
            assert response.status == expected_status

    def test_retry_mechanism(self, weather_service, mock_response):
        """Testa mecanismo de retry em caso de timeout."""
        with patch.object(weather_service.session, 'get') as mock_get:
            mock_get.side_effect = [
                requests.Timeout,
                requests.ConnectionError,
                mock_response
            ]
            
            response = weather_service.get_weather("Lisboa", "PT")
            
            assert response.success is True
            assert mock_get.call_count == 3

    def test_invalid_api_response(self, weather_service):
        """Testa resposta inválida da API."""
        mock_response = Mock()
        mock_response.json.return_value = {"cod": "404", "message": "city not found"}
        
        with patch.object(weather_service.session, 'get', return_value=mock_response):
            with pytest.raises(WeatherAPIException):
                weather_service._validate_response(mock_response.json())

    def test_build_params(self, weather_service):
        """Testa construção de parâmetros da requisição."""
        params = weather_service._build_params("Lisboa", "PT")
        
        assert params["q"] == "Lisboa,PT"
        assert params["appid"] == "test_key"
        assert params["units"] == "metric"
        assert params["lang"] == "pt"

    def test_get_weather(self, weather_service):
        """Testa obtenção do clima."""
        with patch('requests.Session.get') as mock_get:
            mock_get.return_value.json.return_value = {"temp": 25}
            response = weather_service.get_weather("Lisboa", "PT")
            assert response.success is True