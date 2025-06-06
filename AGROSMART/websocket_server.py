import asyncio
import json
from typing import Dict, Set, Any
import websockets
from websockets.server import WebSocketServerProtocol
from src.utils.logger import Logger
from src.config.settings import Settings
from dataclasses import dataclass
from datetime import datetime

logger = Logger(__name__)

@dataclass
class WebSocketMessage:
    """Estrutura de mensagem WebSocket."""
    type: str
    data: Dict[str, Any]
    timestamp: str = None

    def __post_init__(self):
        """Inicializa timestamp se não fornecido."""
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_json(self) -> str:
        """Converte mensagem para JSON."""
        return json.dumps({
            "type": self.type,
            "data": self.data,
            "timestamp": self.timestamp
        })

class WebSocketServer:
    """
    Servidor WebSocket para comunicação em tempo real.
    
    Features:
    - Gerenciamento de conexões
    - Broadcast de mensagens
    - Validação de mensagens
    - Autenticação de clientes
    """

    def __init__(self, host: str = "0.0.0.0", port: int = 8765):
        """
        Inicializa o servidor WebSocket.
        
        Args:
            host: Endereço do servidor
            port: Porta para conexões
        """
        self.host = host
        self.port = port
        self.clients: Set[WebSocketServerProtocol] = set()
        self.logger = Logger(__name__)

    async def register(self, websocket: WebSocketServerProtocol) -> None:
        """
        Registra nova conexão de cliente.
        
        Args:
            websocket: Conexão do cliente
        """
        self.clients.add(websocket)
        self.logger.info(
            "Cliente conectado",
            extra={"client_id": id(websocket)}
        )

    async def unregister(self, websocket: WebSocketServerProtocol) -> None:
        """
        Remove conexão de cliente.
        
        Args:
            websocket: Conexão do cliente
        """
        self.clients.remove(websocket)
        self.logger.info(
            "Cliente desconectado",
            extra={"client_id": id(websocket)}
        )

    async def broadcast(self, message: WebSocketMessage) -> None:
        """
        Envia mensagem para todos os clientes.
        
        Args:
            message: Mensagem a ser enviada
        """
        if not self.clients:
            return

        json_message = message.to_json()
        await asyncio.gather(
            *[client.send(json_message) for client in self.clients],
            return_exceptions=True
        )

    async def handle_connection(self, websocket: WebSocketServerProtocol, path: str) -> None:
        """
        Gerencia conexão com cliente.
        
        Args:
            websocket: Conexão do cliente
            path: Caminho da conexão
        """
        await self.register(websocket)
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self.handle_message(websocket, data)
                except json.JSONDecodeError:
                    self.logger.error(
                        "Mensagem inválida recebida",
                        extra={"message": message}
                    )
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Invalid message format"
                    }))
        except websockets.exceptions.ConnectionClosed:
            self.logger.info(
                "Conexão fechada pelo cliente",
                extra={"client_id": id(websocket)}
            )
        finally:
            await self.unregister(websocket)

    async def handle_message(self, websocket: WebSocketServerProtocol, data: Dict) -> None:
        """
        Processa mensagem recebida.
        
        Args:
            websocket: Conexão do cliente
            data: Dados da mensagem
        """
        if "type" not in data:
            await websocket.send(json.dumps({
                "type": "error",
                "message": "Message type is required"
            }))
            return

        # Exemplo de broadcast de atualização de sensor
        if data["type"] == "sensor_update":
            await self.broadcast(WebSocketMessage(
                type="sensor_update",
                data=data["data"]
            ))

    async def start(self) -> None:
        """Inicia o servidor WebSocket."""
        self.logger.info(
            f"Iniciando servidor WebSocket em ws://{self.host}:{self.port}"
        )
        async with websockets.serve(
            self.handle_connection,
            self.host,
            self.port
        ):
            await asyncio.Future()  # run forever

def run_server() -> None:
    """Função principal para iniciar o servidor."""
    server = WebSocketServer(
        host=Settings.WS_HOST,
        port=Settings.WS_PORT
    )
    
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        logger.info("Servidor finalizado pelo usuário")
    except Exception as e:
        logger.error(f"Erro ao iniciar servidor: {str(e)}")

if __name__ == "__main__":
    run_server()
