"""
Configurações e fixtures comuns para testes do AGROSMART.

Este módulo fornece:
- Configurações globais para testes
- Fixtures reutilizáveis
- Dados de exemplo padronizados
- Helpers para validação
"""

import pytest
from pathlib import Path
from typing import Generator, Dict, Any
from unittest.mock import Mock
from sqlalchemy.orm import Session
from datetime import datetime

# Diretórios de teste
TEST_DIR = Path(__file__).parent
TEST_DATA_DIR = TEST_DIR / 'data'
TEST_TEMP_DIR = TEST_DIR / 'temp'

# Dados padrão para testes
DEFAULT_WEATHER_DATA = {
    "main": {
        "temp": 25.6,
        "humidity": 65
    },
    "weather": [{"description": "céu limpo"}]
}

DEFAULT_SENSOR_DATA = {
    "umidade": 65.5,
    "temperatura": 25.0,
    "luminosidade": 1200
}

@pytest.fixture(autouse=True)
def setup_test_environment() -> Generator:
    """
    Configura ambiente de teste e faz limpeza.
    
    - Cria diretórios necessários
    - Limpa arquivos temporários após testes
    
    Yields:
        None
    """
    # Setup
    TEST_DATA_DIR.mkdir(exist_ok=True)
    TEST_TEMP_DIR.mkdir(exist_ok=True)
    
    yield
    
    # Cleanup
    for file in TEST_TEMP_DIR.glob('*'):
        try:
            file.unlink()
        except Exception as e:
            print(f"Erro ao limpar arquivo {file}: {e}")

@pytest.fixture
def mock_db_session() -> Mock:
    """
    Fixture para mock de sessão do banco.
    
    Returns:
        Mock: Sessão mockada com métodos comuns
    """
    mock = Mock(spec=Session)
    mock.query = Mock(return_value=mock)
    mock.filter = Mock(return_value=mock)
    mock.first = Mock()
    mock.all = Mock(return_value=[])
    mock.count = Mock(return_value=0)
    mock.add = Mock()
    mock.commit = Mock()
    mock.rollback = Mock()
    mock.close = Mock()
    return mock

@pytest.fixture
def sample_data() -> Dict[str, Any]:
    """
    Fixture com dados de exemplo para testes.
    
    Returns:
        Dict: Dados padronizados para testes
            - usuarios: Lista de usuários
            - sensores: Lista de sensores
            - notificacoes: Lista de notificações
    """
    return {
        "usuarios": [
            {
                "id": 1,
                "nome": "Teste User",
                "email": "test@example.com",
                "ativo": True
            }
        ],
        "sensores": [
            {
                "id": 1,
                "tipo": "UMIDADE",
                "valor": 65.5,
                "ativo": True,
                "ultima_leitura": datetime.now()
            },
            {
                "id": 2,
                "tipo": "TEMPERATURA",
                "valor": 25.0,
                "ativo": True,
                "ultima_leitura": datetime.now()
            }
        ],
        "notificacoes": [
            {
                "id": 1,
                "titulo": "Teste",
                "mensagem": "Mensagem de teste",
                "tipo": "INFO",
                "usuario_id": 1,
                "lida": False
            }
        ]
    }

def assert_dict_equal(d1: Dict, d2: Dict, ignore_keys: list = None) -> None:
    """
    Helper para comparar dicionários ignorando chaves específicas.
    
    Args:
        d1: Primeiro dicionário
        d2: Segundo dicionário
        ignore_keys: Lista de chaves para ignorar na comparação
    
    Raises:
        AssertionError: Se os dicionários forem diferentes
    """
    if ignore_keys is None:
        ignore_keys = []
        
    d1_filtered = {k: v for k, v in d1.items() if k not in ignore_keys}
    d2_filtered = {k: v for k, v in d2.items() if k not in ignore_keys}
    
    assert d1_filtered == d2_filtered, \
        f"Dicionários diferentes:\nEsperado: {d1_filtered}\nRecebido: {d2_filtered}"