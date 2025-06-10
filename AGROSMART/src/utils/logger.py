"""
Logger personalizado para o AgroSmart.
Inclui rotação de arquivos, contexto extra e integração com settings globais.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from src.config.settings import Settings

class Logger:
    """
    Logger personalizado com rotação de arquivos e contexto extra.
    """
    
    MAX_BYTES = 10 * 1024 * 1024  # 10MB
    BACKUP_COUNT = 5
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    
    def __init__(self, name: str, log_level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        """Configura handlers para arquivo e console."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True, parents=True)
        
        # Handler de arquivo com rotação
        file_handler = RotatingFileHandler(
            log_dir / "app.log",
            maxBytes=self.MAX_BYTES,
            backupCount=self.BACKUP_COUNT
        )
        file_handler.setFormatter(self._get_formatter(detailed=True))
        
        # Handler de console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self._get_formatter())
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def _get_formatter(self, detailed: bool = False) -> logging.Formatter:
        """Retorna o formatador de log."""
        if detailed:
            return logging.Formatter(
                '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] %(message)s',
                datefmt=self.DATE_FORMAT
            )
        return logging.Formatter('%(levelname)s: %(message)s')

    def info(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Registra mensagem com nível INFO."""
        self.logger.info(message, extra=extra)

    def error(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Registra mensagem com nível ERROR."""
        self.logger.error(message, extra=extra)

    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Registra mensagem com nível WARNING."""
        self.logger.warning(message, extra=extra)

    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Registra mensagem com nível DEBUG."""
        self.logger.debug(message, extra=extra)