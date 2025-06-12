from datetime import datetime
from ..utils.logger import setup_logger

logger = setup_logger()

class NotificationService:
    def __init__(self):
        self.notifications = []
        self.severity_levels = {
            'HIGH': 3,
            'MEDIUM': 2,
            'LOW': 1
        }

    def create_notification(self, recommendation):
        try:
            notifications = []
            
            # Verifica condições de temperatura
            if recommendation['temperature_status'] == 'high':
                notifications.append({
                    'type': 'TEMPERATURE_ALERT',
                    'message': 'Alta temperatura detetada - Risco para as vinhas',
                    'severity': 'HIGH',
                    'timestamp': datetime.now().isoformat(),
                    'details': 'Aumentar irrigação e monitorizar stress das vinhas'
                })
            
            # Verifica condições de humidade
            if recommendation['humidity_status'] == 'high':
                notifications.append({
                    'type': 'HUMIDITY_ALERT',
                    'message': 'Humidade elevada - Risco de doenças fúngicas',
                    'severity': 'HIGH',
                    'timestamp': datetime.now().isoformat(),
                    'details': 'Monitorizar sinais de míldio e outras doenças fúngicas'
                })
            elif recommendation['humidity_status'] == 'low':
                notifications.append({
                    'type': 'HUMIDITY_ALERT',
                    'message': 'Humidade baixa - Risco de stress hídrico',
                    'severity': 'MEDIUM',
                    'timestamp': datetime.now().isoformat(),
                    'details': 'Considerar aumento da irrigação'
                })

            # Adiciona recomendações de irrigação
            if recommendation['should_irrigate']:
                notifications.append({
                    'type': 'IRRIGATION_ALERT',
                    'message': f"Irrigação necessária - Intensidade {recommendation['intensity']}",
                    'severity': 'HIGH' if recommendation['intensity'] == 'high' else 'MEDIUM',
                    'timestamp': datetime.now().isoformat(),
                    'details': recommendation['reason']
                })

            # Processa avisos
            for warning in recommendation['warnings']:
                notifications.append({
                    'type': 'WARNING',
                    'message': warning,
                    'severity': 'MEDIUM',
                    'timestamp': datetime.now().isoformat(),
                    'details': 'Aviso automático baseado nas condições atuais'
                })

            self.notifications.extend(notifications)
            return notifications

        except Exception as e:
            logger.error(f"Error creating notifications: {str(e)}")
            raise

    def get_active_notifications(self, severity_level=None):
        try:
            if severity_level:
                return [n for n in self.notifications 
                       if self.severity_levels[n['severity']] >= 
                       self.severity_levels[severity_level]]
            return self.notifications

        except Exception as e:
            logger.error(f"Error retrieving notifications: {str(e)}")
            raise

    def clear_notifications(self):
        self.notifications = []