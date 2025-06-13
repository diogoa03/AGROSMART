from ..utils.logger import setup_logger
from .notification_service import NotificationService

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
        self.notification_service = NotificationService()

    def get_recommendation(self, weather_data):
        try:
            temp = weather_data['temperature']
            humidity = weather_data['humidity']

            recommendation = {
                'should_irrigate': False,
                'intensity': 'nenhuma',
                'reason': '',
                'temperature_status': 'normal',
                'humidity_status': 'normal',
                'warnings': []
            }

            # Temperature analysis for grapes
            if temp > self.temperature_thresholds['high']:
                recommendation['temperature_status'] = 'elevada'
                recommendation['warnings'].append('Temperatura elevada pode causar stress nas vinhas')
                recommendation['should_irrigate'] = True
                recommendation['intensity'] = 'elevada'
                recommendation['reason'] = 'Temperatura elevada requer aumento da irrigação'
            elif temp < self.temperature_thresholds['low']:
                recommendation['temperature_status'] = 'baixa'
                recommendation['warnings'].append('Temperatura baixa pode atrasar o crescimento')

            # Humidity analysis for grapes
            if humidity < self.humidity_thresholds['low']:
                recommendation['humidity_status'] = 'baixa'
                recommendation['should_irrigate'] = True
                recommendation['intensity'] = 'elevada'
                recommendation['reason'] = 'Humidade baixa pode afetar o desenvolvimento das uvas'
            elif humidity > self.humidity_thresholds['high']:
                recommendation['humidity_status'] = 'elevada'
                recommendation['reason'] = 'Humidade elevada - monitorizar doenças fúngicas'
                recommendation['warnings'].append('Risco de míldio e outras doenças fúngicas')
            else:
                recommendation['intensity'] = 'média' if temp > 25 else 'baixa'
                recommendation['should_irrigate'] = temp > 25
                recommendation['reason'] = 'Condições normais para a cultura da vinha'
            
            # Don't create notifications based on recommendations anymore
            # Just return the recommendation without adding notifications
            return recommendation
            
        except Exception as e:
            logger.error(f"Erro ao gerar recomendação para cultivo de uvas: {str(e)}")
            raise