import unittest
from src.services.notification_service import NotificationService

class TestNotificationService(unittest.TestCase):
    def setUp(self):
        self.notification_service = NotificationService()

    def test_high_temperature_notification(self):
        recommendation = {
            'temperature_status': 'high',
            'humidity_status': 'normal',
            'should_irrigate': True,
            'intensity': 'high',
            'reason': 'High temperature requires increased irrigation',
            'warnings': ['High temperature may stress vines']
        }

        notifications = self.notification_service.create_notification(recommendation)
        
        self.assertTrue(any(n['type'] == 'TEMPERATURE_ALERT' for n in notifications))
        self.assertTrue(any(n['severity'] == 'HIGH' for n in notifications))

    def test_high_humidity_notification(self):
        recommendation = {
            'temperature_status': 'normal',
            'humidity_status': 'high',
            'should_irrigate': False,
            'intensity': 'none',
            'reason': 'High humidity - monitor for fungal diseases',
            'warnings': ['Risk of powdery mildew and other fungal diseases']
        }

        notifications = self.notification_service.create_notification(recommendation)
        
        self.assertTrue(any(n['type'] == 'HUMIDITY_ALERT' for n in notifications))
        self.assertTrue(any('fungal' in n['message'].lower() for n in notifications))

    def test_severity_filter(self):
        recommendation = {
            'temperature_status': 'high',
            'humidity_status': 'low',
            'should_irrigate': True,
            'intensity': 'high',
            'reason': 'Multiple conditions require attention',
            'warnings': ['Warning test']
        }

        self.notification_service.create_notification(recommendation)
        high_severity = self.notification_service.get_active_notifications('HIGH')
        medium_severity = self.notification_service.get_active_notifications('MEDIUM')
        
        self.assertTrue(len(high_severity) <= len(medium_severity))

if __name__ == '__main__':
    unittest.main()