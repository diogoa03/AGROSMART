from src.services.notification_service import NotificationService

notification_service = NotificationService()

# Example recommendation
recommendation = {
    'temperature_status': 'high',
    'humidity_status': 'normal',
    'should_irrigate': True,
    'intensity': 'high',
    'reason': 'High temperature requires increased irrigation',
    'warnings': ['High temperature may stress vines']
}

# Create notifications
notifications = notification_service.create_notification(recommendation)

# Retrieve active notifications
active_notifications = notification_service.get_active_notifications()

# Clear notifications
notification_service.clear_notifications()