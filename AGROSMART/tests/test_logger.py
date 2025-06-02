import pytest
import logging
import os
from pathlib import Path
from unittest.mock import patch, Mock
from src.utils.logger import Logger

class TestLogger:
    @pytest.fixture
    def mock_settings(self):
        """Fixture para simular configurações."""
        with patch('src.utils.logger.Settings') as mock:
            mock.LOGS_DIR = Path('./test_logs')
            yield mock
            
    @pytest.fixture
    def logger(self, mock_settings):
        """Fixture para criar instância do logger."""
        logger = Logger('test_logger')
        yield logger
        # Cleanup
        if mock_settings.LOGS_DIR.exists():
            for file in mock_settings.LOGS_DIR.glob('*.log'):
                file.unlink()
            mock_settings.LOGS_DIR.rmdir()

    def test_logger_initialization(self, logger):
        """Testa inicialização correta do logger."""
        assert logger.logger.name == 'test_logger'
        assert logger.logger.level == logging.INFO
        assert len(logger.logger.handlers) == 3

    def test_formatter_detailed(self, logger):
        """Testa formatador detalhado."""
        formatter = logger._get_formatter(detailed=True)
        assert '[%(asctime)s]' in formatter._fmt
        assert '%(extra)s' in formatter._fmt

    def test_formatter_simple(self, logger):
        """Testa formatador simples."""
        formatter = logger._get_formatter(detailed=False)
        assert formatter._fmt == '%(levelname)s: %(message)s'

    def test_format_extra_empty(self, logger):
        """Testa formatação de extra vazio."""
        assert logger._format_extra(None) == ""
        assert logger._format_extra({}) == "- {}"

    def test_format_extra_with_data(self, logger):
        """Testa formatação de extra com dados."""
        extra = {"user": "test", "action": "login"}
        assert logger._format_extra(extra) == f"- {extra}"

    def test_log_methods(self, logger):
        """Testa todos os métodos de log."""
        methods = ['info', 'error', 'warning', 'debug', 'critical']
        mock_logger = Mock()
        logger.logger = mock_logger
        
        for method in methods:
            getattr(logger, method)("Test message", {"test": "data"})
            getattr(mock_logger, method).assert_called_once()

    def test_log_file_creation(self, logger, mock_settings):
        """Testa criação de arquivos de log."""
        logger.info("Test message")
        
        log_files = list(mock_settings.LOGS_DIR.glob('*.log'))
        assert len(log_files) > 0

    def test_error_handling_in_format_extra(self, logger):
        """Testa tratamento de erro na formatação de extra."""
        class BadDict(dict):
            def __str__(self):
                raise Exception("Bad data")
                
        result = logger._format_extra(BadDict())
        assert result == "- Error formatting extra data"