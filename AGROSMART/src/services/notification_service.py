class NotificationService:
    """
    Serviço para gerenciar notificações.
    """
    
    def __init__(self):
        """
        Inicializa o serviço de notificações.
        """
        self.subscribers = []