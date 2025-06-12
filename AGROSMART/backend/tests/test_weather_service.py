import unittest
import os
from unittest.mock import Mock, patch
from src.services.weather_service import WeatherService, socketio
from src.storage.data_store import DataStore

class TestWeatherService(unittest.TestCase):
    def setUp(self):
        self.weather_service = WeatherService()
        self.data_store = DataStore()
        # Faça o mock do socketio para evitar emissões reais durante os testes
        self.mock_socketio = Mock()
        socketio.emit = self.mock_socketio.emit

    def test_get_current_weather(self):
        weather_data = self.weather_service.get_current_weather()
        
        # Teste a estrutura dos dados meteorológicos
        self.assertIsNotNone(weather_data)
        self.assertIn('temperature', weather_data)
        self.assertIn('humidity', weather_data)
        self.assertIn('description', weather_data)
        self.assertIn('timestamp', weather_data)
        
        # Verifique se socketio.emit foi chamado com os dados corretos
        self.mock_socketio.emit.assert_called_once_with('weather_update', weather_data)

    def test_weather_history(self):
        weather_data = self.weather_service.get_current_weather()
        history = self.weather_service.get_weather_history()
        self.assertIsInstance(history, list)
        self.assertGreater(len(history), 0)

    @patch('requests.get')
    def test_weather_service_error(self, mock_get):
        # Simula erro da API
        mock_get.side_effect = Exception("API Error")
        
        with self.assertRaises(Exception):
            self.weather_service.get_current_weather()
        
        # Verifique se socketio.emit não foi chamado em caso de erro
        self.mock_socketio.emit.assert_not_called()

    def tearDown(self):
        # Limpe quaisquer dados de teste, se necessário
        pass

if __name__ == '__main__':
    unittest.main()