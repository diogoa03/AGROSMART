from datetime import datetime
import uuid  # Adicione esta linha
from ..utils.logger import setup_logger

# configuração do registo de eventos
logger = setup_logger()

class NotificationService:
    def __init__(self):

        # lista para armazenar as notificações
        self.notifications = []

        # níveis de severidade das notificações
        self.severity_levels = {
            'HIGH': 3,
            'MEDIUM': 2,
            'LOW': 1
        }

    def create_notification(self, recommendation):
        try:
            notifications = []
            
            # verificar condições de temperatura
            if recommendation['temperature_status'] == 'elevada':
                notifications.append({
                    'id': str(uuid.uuid4()),  
                    'type': 'ALERTA_TEMPERATURA',
                    'message': 'Temperatura elevada detetada - Risco para as vinhas',
                    'severity': 'HIGH', 
                    'timestamp': datetime.now().isoformat(),
                    'details': 'Aumentar a irrigação e monitorizar o stress das vinhas'
                })
            
            # verificar condições de humidade
            if recommendation['humidity_status'] == 'elevada':  
                notifications.append({
                    'id': str(uuid.uuid4()),
                    'type': 'ALERTA_HUMIDADE',
                    'message': 'Humidade elevada - Risco de doenças fúngicas',
                    'severity': 'HIGH',  
                    'timestamp': datetime.now().isoformat(),
                    'details': 'Monitorizar sinais de míldio e outras doenças fúngicas'
                })
            elif recommendation['humidity_status'] == 'baixa': 
                notifications.append({
                    'id': str(uuid.uuid4()),
                    'type': 'ALERTA_HUMIDADE',
                    'message': 'Humidade baixa - Risco de stress hídrico',
                    'severity': 'MEDIUM',  
                    'timestamp': datetime.now().isoformat(),
                    'details': 'Considerar aumento da irrigação'
                })

            # if recommendation['should_irrigate']:
            #     notifications.append({
            #         'id': str(uuid.uuid4()),
            #         'type': 'ALERTA_IRRIGAÇÃO',
            #         'message': f"Irrigação necessária - Intensidade {recommendation['intensity']}",
            #         'severity': 'HIGH' if recommendation['intensity'] == 'elevada' else 'MEDIUM', 
            #         'timestamp': datetime.now().isoformat(),
            #         'details': recommendation['reason']
            #     })

            # processar avisos
            # for warning in recommendation['warnings']:
            #     notifications.append({
            #         'id': str(uuid.uuid4()),
            #         'type': 'AVISO',
            #         'message': warning,
            #         'severity': 'MEDIUM',  
            #         'timestamp': datetime.now().isoformat(),
            #         'details': 'Aviso automático baseado nas condições atuais'
            #     })

            # guardar notificações na lista geral
            self.notifications.extend(notifications)
            return notifications

        except Exception as e:

            # registar erro no logger
            logger.error(f"Erro ao criar notificações: {str(e)}")
            raise

    def get_active_notifications(self, severity_level=None):
        try:
            # retornar notificações filtradas por nível de severidade, se especificado
            if severity_level:
                return [n for n in self.notifications 
                       if self.severity_levels[n['severity']] >= 
                       self.severity_levels[severity_level]]
            
            # caso contrário, retornar todas as notificações
            return self.notifications

        except Exception as e:

            # registar erro no logger
            logger.error(f"Error retrieving notifications: {str(e)}")
            raise

    def clear_notifications(self):

        # limpar todas as notificações
        self.notifications = []

    def delete_notification(self, notification_id):

        # remover uma notificação específica pelo ID
        self.notifications = [
            n for n in self.notifications if str(n.get('id')) != str(notification_id)
        ]