from ..utils.logger import setup_logger
from .notification_service import NotificationService

# configuração do logger para registo de eventos
logger = setup_logger()

class RecomendacaoService:
    def __init__(self):

        # limiares específicos para o cultivo de uvas
        self.temperature_thresholds = {
            'low': 10,    # as uvas necessitam de pelo menos 10°C para crescimento
            'high': 35    # acima de 35°C pode danificar o desenvolvimento das uvas
        }
        self.humidity_thresholds = {
            'low': 60,    # as uvas preferem humidade acima de 60%
            'high': 85    # acima de 85% aumenta o risco de doenças fúngicas
        }

        # inicialização do serviço de notificações
        self.notification_service = NotificationService()

    def get_recommendation(self, weather_data):
        try:

            # extração dos dados meteorológicos
            temp = weather_data['temperature']
            humidity = weather_data['humidity']

            # estrutura base da recomendação
            recommendation = {
                'should_irrigate': False,
                'intensity': 'nenhuma',
                'reason': '',
                'temperature_status': 'normal',
                'humidity_status': 'normal',
                'warnings': []
            }

            # análise da temperatura para vinhas
            if temp > self.temperature_thresholds['high']:
                recommendation['temperature_status'] = 'elevada'
                recommendation['warnings'].append('Temperatura elevada pode causar stress nas vinhas')
                recommendation['should_irrigate'] = True
                recommendation['intensity'] = 'elevada'
                recommendation['reason'] = 'Temperatura elevada requer aumento da irrigação'
            elif temp < self.temperature_thresholds['low']:
                recommendation['temperature_status'] = 'baixa'
                recommendation['warnings'].append('Temperatura baixa pode atrasar o crescimento')

            # análise da humidade para vinhas
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
                # condições normais de humidade
                recommendation['intensity'] = 'média' if temp > 25 else 'baixa'
                recommendation['should_irrigate'] = temp > 25
                recommendation['reason'] = 'Condições normais para a cultura da vinha'
            
            self.notification_service.create_notification(recommendation)

            return recommendation
        except Exception as e:
            # Registo de erro no logger
            logger.error(f"Erro ao gerar recomendação para cultivo de uvas: {str(e)}")
            raise