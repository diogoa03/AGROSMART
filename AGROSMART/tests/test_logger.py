import pytest
import logging
import tempfile
import shutil
from pathlib import Path
from src.utils.logger import Logger
from unittest.mock import patch

@pytest.fixture
def temp_log_dir():
    """Cria diretório temporário para logs."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_settings():
    """Mock das configurações."""
    with patch('src.config.settings.settings') as mock:
        mock.LOGS_DIR = Path(tempfile.mkdtemp())
        yield mock

@pytest.fixture
def logger(mock_settings):
    """Fixture para criar Logger."""
    return Logger("test")

def test_logger_initialization(logger):
    """Testa inicialização básica do logger."""
    assert logger.logger.name == "test"
    assert logger.logger.level == logging.INFO
    assert len(logger.logger.handlers) == 3  # Arquivo diário, rotativo e console

def test_log_levels(logger):
    """Testa todos os níveis de log."""
    messages = {
        "info": "test info",
        "error": "test error", 
        "warning": "test warning",
        "debug": "test debug",
        "critical": "test critical"
    }
    
    logger.info(messages["info"])
    logger.error(messages["error"])
    logger.warning(messages["warning"])
    logger.debug(messages["debug"])
    logger.critical(messages["critical"])

def test_format_extra(logger):
    """Testa formatação de dados extras."""
    # Teste com dict vazio
    assert logger._format_extra({}) == "- {}"
    
    # Teste com None
    assert logger._format_extra(None) == ""
    
    # Teste com dados
    extra = {"key": "value"}
    assert logger._format_extra(extra) == f"- {extra}"

def test_log_with_extra(logger):
    """Testa logging com dados extras."""
    extra = {"temperature": 25.5, "humidity": 65}
    logger.info("Weather data", extra=extra)

def test_handlers_configuration(logger, mock_settings):
    """Testa configuração dos handlers."""
    handlers = logger.logger.handlers
    
    # Verifica tipos dos handlers
    assert any(isinstance(h, logging.StreamHandler) for h in handlers)
    assert any(isinstance(h, logging.handlers.RotatingFileHandler) for h in handlers)
    assert any(isinstance(h, logging.handlers.TimedRotatingFileHandler) for h in handlers)

def test_handler_formatters(logger):
    """Testa formatadores dos handlers."""
    for handler in logger.logger.handlers:
        assert handler.formatter is not None
        
        if isinstance(handler, (logging.handlers.RotatingFileHandler, 
                              logging.handlers.TimedRotatingFileHandler)):
            # Handlers de arquivo devem usar formato detalhado
            assert '[%(name)s:%(lineno)d]' in handler.formatter._fmt
        else:
            # Handler de console usa formato simples
            assert handler.formatter._fmt == '%(levelname)s: %(message)s'

def test_log_file_creation(logger, mock_settings):
    """Testa criação de arquivos de log."""
    test_message = "Test log message"
    logger.info(test_message)
    
    log_files = list(mock_settings.LOGS_DIR.glob("*.log"))
    assert len(log_files) >= 1