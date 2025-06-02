import pytest
from flask import Flask
from unittest.mock import Mock, patch
from src.config.settings import Settings
from app import app

@pytest.fixture
def client():
    """Fixture para criar cliente de teste."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

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
    def test_weather_endpoint(self, client, mock_weather_service):
        """Testa endpoint de clima."""
        mock_weather_service.get_weather.return_value = Mock(
            __dict__={"data": {"temp": 25}},
            status=200
        )
        
        response = client.get('/api/weather?city=Lisboa&country=PT')
        
        assert response.status_code == 200
        mock_weather_service.get_weather.assert_called_with("Lisboa", "PT")
        
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
        mock_notificacao_service.listar_por_usuario.assert_called_with(1, page=1, per_page=20)