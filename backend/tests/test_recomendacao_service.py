import unittest
from src.services.recomendacao_service import RecomendacaoService

class TestRecomendacaoService(unittest.TestCase):
    def setUp(self):
        
        # prepara o serviço
        self.service = RecomendacaoService()

    def test_low_humidity_for_grapes(self):
        
        # teste com humidade baixa
        weather_data = {
            'temperature': 20,
            'humidity': 55  
        }
        recommendation = self.service.get_recommendation(weather_data)
        
        # verifica os resultados
        self.assertTrue(recommendation['should_irrigate'])
        self.assertEqual(recommendation['intensity'], 'elevada') 
        self.assertEqual(recommendation['humidity_status'], 'baixa')  
        self.assertTrue('desenvolvimento das uvas' in recommendation['reason'].lower()) 

    def test_high_humidity_for_grapes(self):
        
        # teste com humidade alta
        weather_data = {
            'temperature': 20,
            'humidity': 90 
        }
        recommendation = self.service.get_recommendation(weather_data)
        
        # verifica os resultados
        self.assertFalse(recommendation['should_irrigate'])
        self.assertEqual(recommendation['humidity_status'], 'elevada')  
        self.assertTrue('fúngicas' in recommendation['reason'].lower())  
        self.assertTrue(any('míldio' in warning.lower() for warning in recommendation['warnings'])) 

    def test_optimal_conditions(self):
        
        # teste com condições ideais
        weather_data = {
            'temperature': 22,  
            'humidity': 70  
        }
        recommendation = self.service.get_recommendation(weather_data)
        
        # verifica os resultados
        self.assertEqual(recommendation['reason'], 'Condições normais para a cultura da vinha')  
        self.assertEqual(recommendation['humidity_status'], 'normal')
        self.assertEqual(recommendation['temperature_status'], 'normal')
        self.assertEqual(recommendation['intensity'], 'baixa')  

    def test_invalid_weather_data(self):

        # teste com dados incompletos
        invalid_data = {'temperature': 20}  
        
        # deve dar erro
        with self.assertRaises(Exception):
            self.service.get_recommendation(invalid_data)

if __name__ == '__main__':
    unittest.main()