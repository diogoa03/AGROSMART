import pytest
import os
from pathlib import Path
from src.config.settings import Settings, get_settings

class TestSettings:
    @pytest.fixture
    def mock_env(self, monkeypatch):
        """Fixture para simular variáveis de ambiente."""
        env_vars = {
            "SECRET_KEY": "x" * 32,
            "OPENWEATHER_API_KEY": "test_key",
            "DATABASE_URL": "sqlite:///test.db",
            "DEBUG": "False",
            "PORT": "5000"
        }
        for key, value in env_vars.items():
            monkeypatch.setenv(key, value)
            
    def test_required_settings(self, mock_env):
        """Testa se configurações obrigatórias são carregadas."""
        settings = Settings()
        assert len(settings.SECRET_KEY) >= 32
        assert settings.OPENWEATHER_API_KEY == "test_key"
        
    def test_default_values(self):
        """Testa valores padrão."""
        settings = Settings()
        assert settings.API_TIMEOUT == 10
        assert settings.PORT == 5000
        
    def test_bool_conversion(self):
        """Testa conversão de booleanos."""
        settings = Settings()
        assert isinstance(settings.DEBUG, bool)
        
    def test_paths_creation(self, tmp_path):
        """Testa criação de diretórios."""
        settings = Settings()
        assert settings.LOGS_DIR.exists()
        assert settings.TEMP_DIR.exists()
        
    def test_singleton(self):
        """Testa se get_settings retorna sempre a mesma instância."""
        s1 = get_settings()
        s2 = get_settings()
        assert s1 is s2
        
    def test_invalid_secret_key(self, mock_env, monkeypatch):
        """Testa validação de SECRET_KEY curta."""
        monkeypatch.setenv("SECRET_KEY", "short")
        with pytest.raises(ValueError) as exc:
            Settings()
        assert "SECRET_KEY" in str(exc.value)