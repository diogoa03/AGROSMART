import unittest
import os
from src.services.weather_service import WeatherService
from src.storage.data_store import DataStore

class TestWeatherService(unittest.TestCase):
    def setUp(self):
        self.weather_service = WeatherService()
        self.data_store = DataStore()

    def test_get_current_weather(self):
        weather_data = self.weather_service.get_current_weather()
        self.assertIsNotNone(weather_data)
        self.assertIn('temperature', weather_data)
        self.assertIn('humidity', weather_data)
        self.assertIn('description', weather_data)
        self.assertIn('timestamp', weather_data)

    def test_weather_history(self):
        weather_data = self.weather_service.get_current_weather()
        history = self.weather_service.get_weather_history()
        self.assertIsInstance(history, list)
        self.assertGreater(len(history), 0)

if __name__ == '__main__':
    unittest.main()