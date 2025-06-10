import pytest
from flask import Flask
from unittest.mock import Mock, patch
from app import app

@pytest.fixture
def client():
    """Cliente de teste."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Testa endpoint de health check."""
    response = client.get('/health')
    assert response.status_code == 200

@pytest.fixture
def mock_weather_service():
    """Fixture para mock do serviço de clima."""
    with patch('app.weather_service') as mock:
        yield mock

@pytest.fixture
def mock_notificacao_service():
    """Fixture para mock do serviço de notificações."""
    with patch('app.notificacao_service') as mock:
        yield mock

class TestAPI:
    def test_weather_endpoint_success(self, client, mock_weather_service):
        """Testa endpoint de clima com sucesso."""
        mock_weather_service.get_weather.return_value = Mock(
            __dict__={"data": {"temp": 25}},
            status=200
        )
        
        response = client.get('/api/weather?city=Lisboa&country=PT')
        
        assert response.status_code == 200
        mock_weather_service.get_weather.assert_called_with("Lisboa", "PT")

    def test_weather_endpoint_failure(self, client, mock_weather_service):
        """Testa endpoint de clima com erro."""
        mock_weather_service.get_weather.return_value = Mock(
            __dict__={"error": "City not found"},
            status=404
        )
        
        response = client.get('/api/weather?city=Invalid&country=XX')
        
        assert response.status_code == 404
        assert "City not found" in response.get_json()["error"]

    def test_criar_notificacao_sucesso(self, client, mock_notificacao_service):
        """Testa criação de notificação com sucesso."""
        dados = {
            "titulo": "Teste",
            "mensagem": "Mensagem teste",
            "tipo": "INFO",
            "usuario_id": 1
        }
        mock_notificacao_service.criar.return_value = Mock(
            __dict__={"success": True},
            status=201
        )
        
        response = client.post('/api/notificacoes', json=dados)
        
        assert response.status_code == 201
        mock_notificacao_service.criar.assert_called_with(**dados)

    def test_criar_notificacao_dados_invalidos(self, client):
        """Testa criação com dados inválidos."""
        response = client.post('/api/notificacoes', json={})
        
        assert response.status_code == 400
        assert "Corpo da requisição vazio" in response.get_json()["erro"]

    def test_listar_notificacoes(self, client, mock_notificacao_service):
        """Testa listagem de notificações."""
        mock_notificacao_service.listar_por_usuario.return_value = Mock(
            __dict__={"data": []},
            status=200
        )
        
        response = client.get('/api/notificacoes/1')
        
        assert response.status_code == 200
        mock_notificacao_service.listar_por_usuario.assert_called_with(
            1, page=1, per_page=20
        )

    def test_marcar_notificacao_lida(self, client, mock_notificacao_service):
        """Testa marcação de notificação como lida."""
        mock_notificacao_service.marcar_como_lida.return_value = Mock(
            __dict__={"success": True},
            status=200
        )
        
        response = client.put('/api/notificacoes/1/lida')
        
        assert response.status_code == 200
        mock_notificacao_service.marcar_como_lida.assert_called_with(1)

    @pytest.mark.parametrize("endpoint,method", [
        ('/api/weather', 'GET'),
        ('/api/notificacoes', 'POST'),
        ('/api/notificacoes/1', 'GET'),
        ('/api/notificacoes/1/lida', 'PUT')
    ])
    def test_endpoint_requer_autenticacao(self, client, endpoint, method):
        """Testa autenticação nos endpoints."""
        if method == 'GET':
            response = client.get(endpoint)
        elif method == 'POST':
            response = client.post(endpoint, json={})
        else:
            response = client.put(endpoint)
            
        assert response.status_code == 401
        assert "Token não fornecido" in response.get_json()["erro"]