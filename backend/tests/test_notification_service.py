import unittest
from src.services.notification_service import NotificationService

class TestNotificationService(unittest.TestCase):
    def setUp(self):
        
        # prepara o serviço para os testes
        self.notification_service = NotificationService()

    def test_high_temperature_notification(self):
        recommendation = {
            'temperature_status': 'elevada',  
            'humidity_status': 'normal',
            'should_irrigate': True,
            'intensity': 'elevada',           
            'reason': 'Temperatura elevada requer aumento da irrigação',
            'warnings': ['Temperatura elevada pode causar stress nas vinhas']
        }
        notifications = self.notification_service.create_notification(recommendation)
        self.assertTrue(any(n['type'] == 'ALERTA_TEMPERATURA' for n in notifications))
        self.assertTrue(any(n['severity'] == 'HIGH' for n in notifications))

    def test_high_humidity_notification(self):
        recommendation = {
            'temperature_status': 'normal',
            'humidity_status': 'elevada',    
            'should_irrigate': False,
            'intensity': 'nenhuma',
            'reason': 'Humidade elevada - monitorizar doenças fúngicas',
            'warnings': ['Risco de míldio e outras doenças fúngicas']
        }
        notifications = self.notification_service.create_notification(recommendation)
        self.assertTrue(any(n['type'] == 'ALERTA_HUMIDADE' for n in notifications))
        self.assertTrue(any('fúngicas' in n['message'].lower() for n in notifications))

    def test_severity_filter(self):

        # testa filtros de prioridade
        recommendation = {
            'temperature_status': 'high',
            'humidity_status': 'low',
            'should_irrigate': True,
            'intensity': 'high',
            'reason': 'Multiple conditions require attention',
            'warnings': ['Warning test']
        }

        # cria alertas e filtra por prioridade
        self.notification_service.create_notification(recommendation)
        high_severity = self.notification_service.get_active_notifications('HIGH')
        medium_severity = self.notification_service.get_active_notifications('MEDIUM')
        
        # confirma que há menos ou igual número de alertas altos vs. médios
        self.assertTrue(len(high_severity) <= len(medium_severity))

if __name__ == '__main__':
    unittest.main()