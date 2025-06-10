import os
from pathlib import Path
from typing import Any, Dict
from dotenv import load_dotenv
from functools import lru_cache

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class Settings:
    """
    Configurações da aplicação com validação e cache.
    
    Gerencia todas as configurações do sistema, incluindo:
    - Configurações básicas (SECRET_KEY, DEBUG, PORT)
    - Chaves de API (OpenWeather)
    - Configurações de banco de dados
    - Timeouts e limites
    - Caminhos do sistema
    """
    
    # Valores padrão e constantes
    MIN_SECRET_KEY_LENGTH = 32
    DEFAULT_PORT = 5000
    DEFAULT_TIMEOUT = 10
    DEFAULT_MAX_RETRIES = 3
    DEFAULT_RATE_LIMIT = 100
    
    def __init__(self):
        """Inicializa as configurações com valores do .env."""
        # Configurações básicas
        self.SECRET_KEY = self._get_required_str("SECRET_KEY")
        self.DEBUG = self._get_bool("DEBUG", True)
        self.PORT = self._get_int("PORT", self.DEFAULT_PORT)
        self.HOST = self._get_str("HOST", "0.0.0.0")
        
        # Database
        self.DATABASE_URL = self._get_required_str(
            "DATABASE_URL", 
            "sqlite:///agrosmart.db"
        )
        
        # API Keys
        self.OPENWEATHER_API_KEY = self._get_required_str("OPENWEATHER_API_KEY")
        
        # API Timeouts e Limites
        self.API_TIMEOUT = self._get_int("API_TIMEOUT", self.DEFAULT_TIMEOUT)
        self.MAX_RETRIES = self._get_int("MAX_RETRIES", self.DEFAULT_MAX_RETRIES)
        self.RATE_LIMIT = self._get_int("RATE_LIMIT", self.DEFAULT_RATE_LIMIT)
        
        # JWT Settings
        self.JWT_SECRET_KEY = self._get_required_str("JWT_SECRET_KEY")
        self.JWT_ALGORITHM = "HS256"
        self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES = self._get_int("JWT_ACCESS_TOKEN_EXPIRES", 30)
        
        # Paths
        self.BASE_DIR = Path(__file__).parent.parent.parent
        self.LOGS_DIR = self.BASE_DIR / "logs"
        self.TEMP_DIR = self.BASE_DIR / "temp"
        
        # Validação inicial
        self._validate_settings()
    
    def _get_required_str(self, key: str, default: str = None) -> str:
        """Obtém uma string obrigatória do ambiente."""
        value = os.getenv(key, default)
        if value is None:
            raise ValueError(f"Configuração obrigatória não encontrada: {key}")
        return value
    
    def _get_str(self, key: str, default: str) -> str:
        """Obtém uma string opcional do ambiente."""
        return os.getenv(key, default)
    
    def _get_int(self, key: str, default: int) -> int:
        """Converte valor do ambiente para inteiro."""
        return int(os.getenv(key, default))
    
    def _get_bool(self, key: str, default: bool) -> bool:
        """Converte valor do ambiente para boolean."""
        return str(os.getenv(key, str(default))).lower() == "true"
    
    def _validate_settings(self) -> None:
        """Valida as configurações críticas."""
        if len(self.SECRET_KEY) < self.MIN_SECRET_KEY_LENGTH:
            raise ValueError(
                f"SECRET_KEY deve ter pelo menos {self.MIN_SECRET_KEY_LENGTH} caracteres"
            )
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL é obrigatória")
        if not self.OPENWEATHER_API_KEY:
            raise ValueError("OPENWEATHER_API_KEY é obrigatória")
        if not self.JWT_SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY é obrigatória")

@lru_cache()
def get_settings() -> Settings:
    """Retorna uma instância cacheada das configurações."""
    return Settings()

# Instância global para uso em imports
settings = get_settings()