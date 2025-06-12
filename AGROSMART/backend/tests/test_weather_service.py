import unittest
import os
from unittest.mock import Mock, patch
from src.services.weather_service import WeatherService, socketio
from src.storage.data_store import DataStore

class TestWeatherService(unittest.TestCase):
    def setUp(self):
        self.weather_service = WeatherService()
        self.data_store = DataStore()
        # Mock the socketio to avoid actual emissions during tests
        self.mock_socketio = Mock()
        socketio.emit = self.mock_socketio.emit

    def test_get_current_weather(self):
        weather_data = self.weather_service.get_current_weather()
        
        # Test weather data structure
        self.assertIsNotNone(weather_data)
        self.assertIn('temperature', weather_data)
        self.assertIn('humidity', weather_data)
        self.assertIn('description', weather_data)
        self.assertIn('timestamp', weather_data)
        
        # Verify that socketio.emit was called with correct data
        self.mock_socketio.emit.assert_called_once_with('weather_update', weather_data)

    def test_weather_history(self):
        weather_data = self.weather_service.get_current_weather()
        history = self.weather_service.get_weather_history()
        self.assertIsInstance(history, list)
        self.assertGreater(len(history), 0)

    @patch('requests.get')
    def test_weather_service_error(self, mock_get):
        # Simulate API error
        mock_get.side_effect = Exception("API Error")
        
        with self.assertRaises(Exception):
            self.weather_service.get_current_weather()
        
        # Verify that socketio.emit was not called on error
        self.mock_socketio.emit.assert_not_called()

    def tearDown(self):
        # Clean up any test data if needed
        pass

if __name__ == '__main__':
    unittest.main()