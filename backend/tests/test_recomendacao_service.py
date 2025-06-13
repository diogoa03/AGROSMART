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
        self.assertEqual(recommendation['intensity'], 'elevada')  # Alterado para 'elevada' em vez de 'high'
        self.assertEqual(recommendation['humidity_status'], 'baixa')  # Alterado para 'baixa' em vez de 'low'
        self.assertTrue('desenvolvimento das uvas' in recommendation['reason'].lower())  # Verificando texto em português

    def test_high_humidity_for_grapes(self):
        weather_data = {
            'temperature': 20,
            'humidity': 90  # Above high threshold for grapes (85)
        }
        recommendation = self.service.get_recommendation(weather_data)
        
        self.assertFalse(recommendation['should_irrigate'])
        self.assertEqual(recommendation['humidity_status'], 'elevada')  # Alterado para 'elevada' em vez de 'high'
        self.assertTrue('fúngicas' in recommendation['reason'].lower())  # Verificando texto em português
        self.assertTrue(any('míldio' in warning.lower() for warning in recommendation['warnings']))  # Verificando texto em português

    def test_optimal_conditions(self):
        weather_data = {
            'temperature': 22,  # Temperatura normal
            'humidity': 70  # Optimal conditions for grapes
        }
        recommendation = self.service.get_recommendation(weather_data)
        
        self.assertEqual(recommendation['reason'], 'Condições normais para a cultura da vinha')  # Texto exato em português
        self.assertEqual(recommendation['humidity_status'], 'normal')
        self.assertEqual(recommendation['temperature_status'], 'normal')
        self.assertEqual(recommendation['intensity'], 'baixa')  # Verificando que a intensidade é 'baixa' quando temp < 25

    def test_invalid_weather_data(self):
        invalid_data = {'temperature': 20}  # Missing humidity
        
        with self.assertRaises(Exception):
            self.service.get_recommendation(invalid_data)

if __name__ == '__main__':
    unittest.main()