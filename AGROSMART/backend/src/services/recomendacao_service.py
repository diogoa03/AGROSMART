from ..utils.logger import setup_logger

logger = setup_logger()

class RecomendacaoService:
    def __init__(self):
        # Thresholds specific for grape cultivation
        self.temperature_thresholds = {
            'low': 10,    # Grapes need minimum 10°C for growth
            'high': 35    # Above 35°C can damage grape development
        }
        self.humidity_thresholds = {
            'low': 60,    # Grapes prefer humidity above 60%
            'high': 85    # Above 85% increases risk of fungal diseases
        }

    def get_recommendation(self, weather_data):
        try:
            temp = weather_data['temperature']
            humidity = weather_data['humidity']

            recommendation = {
                'should_irrigate': False,
                'intensity': 'none',
                'reason': '',
                'temperature_status': 'normal',
                'humidity_status': 'normal',
                'warnings': []
            }

            # Temperature analysis for grapes
            if temp > self.temperature_thresholds['high']:
                recommendation['temperature_status'] = 'high'
                recommendation['warnings'].append('High temperature may stress vines')
                recommendation['should_irrigate'] = True
                recommendation['intensity'] = 'high'
                recommendation['reason'] = 'High temperature requires increased irrigation'
            elif temp < self.temperature_thresholds['low']:
                recommendation['temperature_status'] = 'low'
                recommendation['warnings'].append('Low temperature may slow growth')

            # Humidity analysis for grapes
            if humidity < self.humidity_thresholds['low']:
                recommendation['humidity_status'] = 'low'
                recommendation['should_irrigate'] = True
                recommendation['intensity'] = 'high'
                recommendation['reason'] = 'Low humidity may affect grape development'
            elif humidity > self.humidity_thresholds['high']:
                recommendation['humidity_status'] = 'high'
                recommendation['reason'] = 'High humidity - monitor for fungal diseases'
                recommendation['warnings'].append('Risk of powdery mildew and other fungal diseases')
            else:
                recommendation['intensity'] = 'medium' if temp > 25 else 'low'
                recommendation['should_irrigate'] = temp > 25
                recommendation['reason'] = 'Normal conditions for grape cultivation'

            return recommendation

        except Exception as e:
            logger.error(f"Error generating grape cultivation recommendation: {str(e)}")
            raise