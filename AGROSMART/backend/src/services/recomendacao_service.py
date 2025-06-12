from ..utils.logger import setup_logger
from .notification_service import NotificationService

logger = setup_logger()

class RecomendacaoService:
    def __init__(self):
        # Limiares específicos para o cultivo de uvas
        self.temperature_thresholds = {
            'low': 10,     # Uvas precisam de no mínimo 10°C para crescer
            'high': 35    # Acima de 35°C pode prejudicar o desenvolvimento das uvas
        }
        self.humidity_thresholds = {
            'low': 60,    # Uvas preferem umidade acima de 60%
            'high': 85    # Acima de 85% aumenta o risco de doenças fúngicas
        }
        self.notification_service = NotificationService()

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

            # Análise de temperatura para uvas
            if temp > self.temperature_thresholds['high']:
                recommendation['temperature_status'] = 'high'
                recommendation['warnings'].append('High temperature may stress vines')
                recommendation['should_irrigate'] = True
                recommendation['intensity'] = 'high'
                recommendation['reason'] = 'High temperature requires increased irrigation'
            elif temp < self.temperature_thresholds['low']:
                recommendation['temperature_status'] = 'low'
                recommendation['warnings'].append('Low temperature may slow growth')

            # Análise de umidade para uvas
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

            # Criar notificações com base na recomendação
            notifications = self.notification_service.create_notification(recommendation)
            recommendation['notifications'] = notifications
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Error generating grape cultivation recommendation: {str(e)}")
            raise