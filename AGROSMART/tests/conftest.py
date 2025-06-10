import os
import sys
import pytest
from pathlib import Path
from unittest.mock import Mock, patch

# Adiciona o diretório raiz ao PYTHONPATH
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

@pytest.fixture
def mock_settings():
    """Fixture para configurações de teste."""
    with patch('src.config.settings.settings') as mock:
        mock.DATABASE_URL = "sqlite:///test.db"
        mock.API_TIMEOUT = 5
        mock.DEBUG = True
        mock.OPENWEATHER_API_KEY = "test-key"
        mock.SECRET_KEY = "test-secret-key"
        yield mock

@pytest.fixture
def mock_logger():
    """Fixture para logger de teste."""
    with patch('src.utils.logger.Logger') as mock:
        yield mock

@pytest.fixture(autouse=True)
def setup_test_env():
    """Configura ambiente de teste."""
    os.environ["TESTING"] = "true"
    os.environ["DATABASE_URL"] = "sqlite:///test.db"
    yield
    os.environ.pop("TESTING", None)
    os.environ.pop("DATABASE_URL", None)