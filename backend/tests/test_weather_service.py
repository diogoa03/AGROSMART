import unittest
from unittest.mock import Mock, patch
from src.services.weather_service import WeatherService
from src.storage.data_store import DataStore

class TestWeatherService(unittest.TestCase):
    def setUp(self):

        # prepara o serviço com socketio simulado
        self.mock_socketio = Mock()
        self.weather_service = WeatherService(self.mock_socketio)
        self.data_store = DataStore()

    @patch('requests.get')
    def test_get_current_weather(self, mock_get):

        # simula a resposta da API do tempo
        mock_get.return_value.json.return_value = {
            'main': {'temp': 22.5, 'humidity': 70},
            'weather': [{'description': 'clear sky'}]
        }
        mock_get.return_value.raise_for_status = Mock()

        weather_data = self.weather_service.get_current_weather()
        
        # verifica se os dados têm os campos necessários
        self.assertIsNotNone(weather_data)
        self.assertIn('temperature', weather_data)
        self.assertIn('humidity', weather_data)
        self.assertIn('description', weather_data)
        self.assertIn('timestamp', weather_data)
        
        # verifica se o evento foi emitido
        self.mock_socketio.emit.assert_called_once_with('weather_update', weather_data)

    @patch('requests.get')
    def test_weather_history(self, mock_get):

        # simula obtenção do histórico
        mock_get.return_value.json.return_value = {
            'main': {'temp': 22.5, 'humidity': 70},
            'weather': [{'description': 'clear sky'}]
        }
        mock_get.return_value.raise_for_status = Mock()

        self.weather_service.get_current_weather()
        history = self.weather_service.get_weather_history()
        self.assertIsInstance(history, list)

    @patch('requests.get')
    def test_weather_service_error(self, mock_get):
        
        # simula um erro na API
        mock_get.side_effect = Exception("API Error")
        
        with self.assertRaises(Exception):
            self.weather_service.get_current_weather()
        
        # confirma que não houve evento emitido
        self.mock_socketio.emit.assert_not_called()

    def tearDown(self):

        # limpeza após os testes
        pass

if __name__ == '__main__':
    unittest.main()