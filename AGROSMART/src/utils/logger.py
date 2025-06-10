"""
Logger personalizado para o AgroSmart.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from src.config.settings import settings

class Logger:
    """Logger personalizado com rotação de arquivos e contexto extra."""
    
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
        log_dir = settings.LOGS_DIR
        log_dir.mkdir(exist_ok=True, parents=True)
        
        # Handler de arquivo com rotação por tamanho
        size_handler = RotatingFileHandler(
            log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log",
            maxBytes=self.MAX_BYTES,
            backupCount=self.BACKUP_COUNT,
            encoding='utf-8'
        )
        size_handler.setFormatter(self._get_formatter(detailed=True))
        
        # Handler de arquivo com rotação diária
        time_handler = TimedRotatingFileHandler(
            log_dir / "app.log",
            when='midnight',
            interval=1,
            backupCount=30,
            encoding='utf-8'
        )
        time_handler.setFormatter(self._get_formatter(detailed=True))
        
        # Handler de console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self._get_formatter())
        
        self.logger.addHandler(size_handler)
        self.logger.addHandler(time_handler)
        self.logger.addHandler(console_handler)
    
    def _get_formatter(self, detailed: bool = False) -> logging.Formatter:
        """Retorna o formatador de log apropriado."""
        if detailed:
            return logging.Formatter(
                '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] '
                '%(message)s %(extra)s',
                datefmt=self.DATE_FORMAT
            )
        return logging.Formatter('%(levelname)s: %(message)s')

    def _format_extra(self, extra: Optional[Dict[str, Any]] = None) -> str:
        """Formata informações extras para o log."""
        if not extra:
            return ""
        try:
            if isinstance(extra, dict) and not extra:
                return "- {}"
            return f"- {extra}"
        except Exception:
            return "- Error formatting extra data"

    def info(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Registra mensagem com nível INFO."""
        self.logger.info(message, extra={"extra": self._format_extra(extra)})

    def error(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Registra mensagem com nível ERROR."""
        self.logger.error(message, extra={"extra": self._format_extra(extra)})

    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Registra mensagem com nível WARNING."""
        self.logger.warning(message, extra={"extra": self._format_extra(extra)})

    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Registra mensagem com nível DEBUG."""
        self.logger.debug(message, extra={"extra": self._format_extra(extra)})

    def critical(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Registra mensagem com nível CRITICAL."""
        self.logger.critical(message, extra={"extra": self._format_extra(extra)})