class WebSocketServer:
    """
    Servidor WebSocket para comunicação em tempo real.
    """
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8765):
        """
        Inicializa o servidor WebSocket.

        Args:
            host (str): Endereço do host
            port (int): Porta do servidor
        """
        self.host = host
        self.port = port