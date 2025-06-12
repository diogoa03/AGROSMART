import unittest
from src.services.recomendacao_service import RecomendacaoService

class TestRecomendacaoService(unittest.TestCase):
    def setUp(self):
        self.service = RecomendacaoService()

    def test_low_humidity_for_grapes(self):
        weather_data = {
            'temperature': 20,
            'humidity': 55   # Abaixo do limite inferior para uvas (60)
        }
        recommendation = self.service.get_recommendation(weather_data)
        
        self.assertTrue(recommendation['should_irrigate'])
        self.assertEqual(recommendation['intensity'], 'high')
        self.assertEqual(recommendation['humidity_status'], 'low')
        self.assertTrue('grape development' in recommendation['reason'].lower())

    def test_high_humidity_for_grapes(self):
        weather_data = {
            'temperature': 20,
            'humidity': 90  # Acima do limite superior para uvas (85)
        }
        recommendation = self.service.get_recommendation(weather_data)
        
        self.assertFalse(recommendation['should_irrigate'])
        self.assertEqual(recommendation['humidity_status'], 'high')
        self.assertTrue('fungal' in recommendation['reason'].lower())
        self.assertTrue(any('fungal diseases' in warning for warning in recommendation['warnings']))

    def test_optimal_conditions(self):
        weather_data = {
            'temperature': 25,
            'humidity': 70  # Condições ideais para uvas
        }
        recommendation = self.service.get_recommendation(weather_data)
        
        self.assertTrue('Normal conditions' in recommendation['reason'])
        self.assertEqual(recommendation['humidity_status'], 'normal')
        self.assertEqual(recommendation['temperature_status'], 'normal')

    def test_invalid_weather_data(self):
        invalid_data = {'temperature': 20}  # Faltando umidade
        
        with self.assertRaises(Exception):
            self.service.get_recommendation(invalid_data)

if __name__ == '__main__':
    unittest.main()