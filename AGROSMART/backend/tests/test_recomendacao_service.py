import unittest
from src.services.recomendacao_service import RecomendacaoService

class TestRecomendacaoService(unittest.TestCase):
    def setUp(self):
        self.service = RecomendacaoService()

    def test_low_humidity_for_grapes(self):
        weather_data = {
            'temperature': 20,
            'humidity': 55  # Below low threshold for grapes (60)
        }
        recommendation = self.service.get_recommendation(weather_data)
        
        self.assertTrue(recommendation['should_irrigate'])
        self.assertEqual(recommendation['intensity'], 'high')
        self.assertEqual(recommendation['humidity_status'], 'low')
        self.assertTrue('grape development' in recommendation['reason'].lower())

    def test_high_humidity_for_grapes(self):
        weather_data = {
            'temperature': 20,
            'humidity': 90  # Above high threshold for grapes (85)
        }
        recommendation = self.service.get_recommendation(weather_data)
        
        self.assertFalse(recommendation['should_irrigate'])
        self.assertEqual(recommendation['humidity_status'], 'high')
        self.assertTrue('fungal' in recommendation['reason'].lower())
        self.assertTrue(any('fungal diseases' in warning for warning in recommendation['warnings']))

    def test_high_temperature_for_grapes(self):
        weather_data = {
            'temperature': 37,  # Above high threshold for grapes (35)
            'humidity': 70
        }
        recommendation = self.service.get_recommendation(weather_data)
        
        expected_conditions = {
            'should_irrigate': True,
            'temperature_status': 'high',
            'intensity': 'high'
        }
        
        # Test each expected condition
        for key, value in expected_conditions.items():
            self.assertEqual(recommendation[key], value, 
                           f"Expected {key} to be {value}, but got {recommendation[key]}")
        
        # Test warning message
        warning_found = any('stress vines' in warning.lower() 
                          for warning in recommendation['warnings'])
        self.assertTrue(warning_found, 
                       "Expected warning about vine stress not found")

    def test_optimal_conditions(self):
        weather_data = {
            'temperature': 25,
            'humidity': 70  # Optimal conditions for grapes
        }
        recommendation = self.service.get_recommendation(weather_data)
        
        self.assertTrue('Normal conditions' in recommendation['reason'])
        self.assertEqual(recommendation['humidity_status'], 'normal')
        self.assertEqual(recommendation['temperature_status'], 'normal')

    def test_invalid_weather_data(self):
        invalid_data = {'temperature': 20}  # Missing humidity
        
        with self.assertRaises(Exception):
            self.service.get_recommendation(invalid_data)

if __name__ == '__main__':
    unittest.main()