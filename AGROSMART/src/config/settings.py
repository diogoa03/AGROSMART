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
    - Configurações JWT
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
        self.HOST = self._get_required_str("HOST", "0.0.0.0")
        
        # Chaves de API
        self.OPENWEATHER_API_KEY = self._get_required_str("OPENWEATHER_API_KEY")
        
        # Database
        self.DATABASE_URL = self._get_required_str(
            "DATABASE_URL", 
            "sqlite:///agrosmart.db"
        )
        
        # API Timeouts e Limites
        self.API_TIMEOUT = self._get_int("API_TIMEOUT", self.DEFAULT_TIMEOUT)
        self.MAX_RETRIES = self._get_int("MAX_RETRIES", self.DEFAULT_MAX_RETRIES)
        self.RATE_LIMIT = self._get_int("RATE_LIMIT", self.DEFAULT_RATE_LIMIT)
        
        # Paths
        self.BASE_DIR = Path(__file__).parent.parent
        self.LOGS_DIR = self.BASE_DIR / "logs"
        self.TEMP_DIR = self.BASE_DIR / "temp"
        
        # JWT Settings
        self.JWT_SECRET_KEY = self._get_required_str("JWT_SECRET_KEY", self.SECRET_KEY)
        self.JWT_ACCESS_TOKEN_EXPIRES = self._get_int("JWT_ACCESS_TOKEN_EXPIRES", 3600)
        
        # Validação inicial
        self._validate_settings()
    
    def _get_required_str(self, key: str, default: str = None) -> str:
        """
        Obtém uma string obrigatória das variáveis de ambiente.
        
        Args:
            key: Nome da variável de ambiente
            default: Valor padrão opcional
            
        Returns:
            str: Valor da variável de ambiente
            
        Raises:
            ValueError: Se a variável não existir e não tiver default
        """
        value = os.getenv(key, default)
        if value is None:
            raise ValueError(f"Configuração obrigatória não encontrada: {key}")
        return str(value)
    
    def _get_int(self, key: str, default: int) -> int:
        """
        Obtém um inteiro das variáveis de ambiente.
        
        Args:
            key: Nome da variável
            default: Valor padrão
            
        Returns:
            int: Valor convertido
        """
        try:
            return int(os.getenv(key, str(default)))
        except ValueError:
            return default
    
    def _get_bool(self, key: str, default: bool) -> bool:
        """
        Obtém um booleano das variáveis de ambiente.
        
        Args:
            key: Nome da variável
            default: Valor padrão
            
        Returns:
            bool: Valor convertido
        """
        return str(os.getenv(key, str(default))).lower() == "true"
    
    def _validate_settings(self) -> None:
        """
        Valida as configurações críticas do sistema.
        
        Raises:
            ValueError: Se alguma configuração estiver inválida
        """
        self._validate_secret_key()
        self._validate_api_keys()
        self._validate_timeouts()
        self._ensure_directories()
    
    def _validate_secret_key(self) -> None:
        """Valida a chave secreta."""
        if len(self.SECRET_KEY) < self.MIN_SECRET_KEY_LENGTH:
            raise ValueError(
                f"SECRET_KEY deve ter pelo menos {self.MIN_SECRET_KEY_LENGTH} caracteres"
            )
    
    def _validate_api_keys(self) -> None:
        """Valida as chaves de API."""
        if not self.OPENWEATHER_API_KEY:
            raise ValueError("OPENWEATHER_API_KEY é obrigatória")
    
    def _validate_timeouts(self) -> None:
        """Valida configurações de timeout."""
        if self.API_TIMEOUT < 1:
            raise ValueError("API_TIMEOUT deve ser maior que 0")
    
    def _ensure_directories(self) -> None:
        """Garante que os diretórios necessários existam."""
        self.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        self.TEMP_DIR.mkdir(parents=True, exist_ok=True)
    
    def as_dict(self) -> Dict[str, Any]:
        """
        Retorna todas as configurações como dicionário.
        
        Returns:
            Dict[str, Any]: Configurações em formato de dicionário
        """
        return {
            key: value for key, value in vars(self).items()
            if key.isupper()
        }

@lru_cache()
def get_settings() -> Settings:
    """
    Retorna instância única das configurações.
    
    Returns:
        Settings: Instância das configurações
        
    Note:
        Usa lru_cache para evitar múltiplas leituras do .env
    """
    return Settings()

# Instância global para uso em imports
settings = get_settings()