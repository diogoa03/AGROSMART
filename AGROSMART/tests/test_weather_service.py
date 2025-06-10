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

    def test_build_params(self, weather_service):
        """Testa construção de parâmetros da requisição."""
        params = weather_service._build_params("Lisboa", "PT")
        assert params["q"] == "Lisboa,PT"
        assert params["appid"] == "test_key"
        assert params["units"] == "metric"
        assert params["lang"] == "pt"