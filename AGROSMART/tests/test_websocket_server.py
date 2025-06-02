import pytest
import asyncio
import json
from unittest.mock import Mock, patch
from websockets.server import WebSocketServerProtocol
from src.websocket.websocket_server import WebSocketServer, WebSocketMessage

@pytest.fixture
def websocket_server():
    """Fixture para criar instância do servidor."""
    return WebSocketServer(host="localhost", port=8765)

@pytest.fixture
def mock_websocket():
    """Fixture para simular conexão WebSocket."""
    mock = Mock(spec=WebSocketServerProtocol)
    mock.send = asyncio.coroutine(lambda x: None)
    return mock

@pytest.mark.asyncio
async def test_register_client(websocket_server, mock_websocket):
    """Testa registro de cliente."""
    await websocket_server.register(mock_websocket)
    assert mock_websocket in websocket_server.clients

@pytest.mark.asyncio
async def test_unregister_client(websocket_server, mock_websocket):
    """Testa remoção de cliente."""
    await websocket_server.register(mock_websocket)
    await websocket_server.unregister(mock_websocket)
    assert mock_websocket not in websocket_server.clients

@pytest.mark.asyncio
async def test_broadcast_message(websocket_server, mock_websocket):
    """Testa broadcast de mensagem."""
    await websocket_server.register(mock_websocket)
    
    message = WebSocketMessage(
        type="test",
        data={"value": 123}
    )
    
    await websocket_server.broadcast(message)
    mock_websocket.send.assert_called_once()

@pytest.mark.asyncio
async def test_handle_invalid_message(websocket_server, mock_websocket):
    """Testa tratamento de mensagem inválida."""
    await websocket_server.handle_message(
        mock_websocket,
        {"invalid": "message"}
    )
    
    mock_websocket.send.assert_called_once()
    sent_message = json.loads(mock_websocket.send.call_args[0][0])
    assert sent_message["type"] == "error"

@pytest.mark.asyncio
async def test_handle_sensor_update(websocket_server, mock_websocket):
    """Testa atualização de sensor."""
    await websocket_server.register(mock_websocket)
    
    sensor_data = {
        "type": "sensor_update",
        "data": {
            "sensor_id": 1,
            "value": 25.5
        }
    }
    
    await websocket_server.handle_message(mock_websocket, sensor_data)
    mock_websocket.send.assert_called_once()