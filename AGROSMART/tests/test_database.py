import pytest
from unittest.mock import Mock, patch
from sqlalchemy.exc import SQLAlchemyError
from src.database.database import (
    create_database_engine,
    db_session,
    get_db,
    check_database_connection
)

@pytest.fixture
def mock_session():
    """Fixture para criar mock de sessão."""
    mock = Mock()
    mock.execute = Mock()
    mock.commit = Mock()
    mock.rollback = Mock()
    mock.close = Mock()
    return mock

@pytest.fixture
def mock_engine():
    """Fixture para mock do engine."""
    with patch('src.database.database.create_engine') as mock:
        yield mock

def test_create_engine_success(mock_engine):
    """Testa criação bem sucedida do engine."""
    url = "sqlite:///test.db"
    create_database_engine(url)
    mock_engine.assert_called_once()
    
    call_args = mock_engine.call_args[1]
    assert 'connect_args' in call_args
    assert call_args['connect_args']['check_same_thread'] is False

def test_create_engine_postgres(mock_engine):
    """Testa criação do engine com PostgreSQL."""
    url = "postgresql://user:pass@localhost:5432/db"
    create_database_engine(url)
    
    call_args = mock_engine.call_args[1]
    assert call_args['pool_size'] == 5
    assert call_args['max_overflow'] == 10
    assert call_args['pool_timeout'] == 30

def test_create_engine_failure(mock_engine):
    """Testa falha na criação do engine."""
    mock_engine.side_effect = SQLAlchemyError("Erro de conexão")
    with pytest.raises(SQLAlchemyError):
        create_database_engine("invalid://url")

def test_db_session_success(mock_session):
    """Testa uso normal do contexto de sessão."""
    with patch('src.database.database.SessionLocal', return_value=mock_session):
        with db_session() as session:
            session.execute("SELECT 1")
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()

def test_db_session_error(mock_session):
    """Testa rollback em caso de erro."""
    mock_session.execute.side_effect = SQLAlchemyError("Erro de execução")
    with patch('src.database.database.SessionLocal', return_value=mock_session):
        with pytest.raises(SQLAlchemyError):
            with db_session() as session:
                session.execute("SELECT 1")
        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()

def test_get_db(mock_session):
    """Testa gerador de sessão."""
    with patch('src.database.database.SessionLocal', return_value=mock_session):
        db = next(get_db())
        assert db == mock_session
        mock_session.close.assert_not_called()

def test_check_connection_success(mock_session):
    """Testa verificação de conexão bem sucedida."""
    with patch('src.database.database.SessionLocal', return_value=mock_session):
        result = check_database_connection()
        assert result is True
        mock_session.execute.assert_called_once_with("SELECT 1")

def test_check_connection_failure(mock_session):
    """Testa verificação de conexão com falha."""
    mock_session.execute.side_effect = SQLAlchemyError("Erro de conexão")
    with patch('src.database.database.SessionLocal', return_value=mock_session):
        result = check_database_connection()
        assert result is False