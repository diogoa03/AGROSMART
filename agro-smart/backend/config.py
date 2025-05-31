"""
Configuração do sistema de gestão agrícola inteligente.

Este módulo centraliza todas as configurações do sistema, incluindo
API keys, intervalos de atualização e configurações de WebSocket.
"""

import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do ficheiro .env
load_dotenv()


class Config:
    """
    Classe de configuração principal do sistema.
    
    Centraliza todas as configurações necessárias para o funcionamento
    do sistema, incluindo credenciais de API, configurações de rede
    e parâmetros operacionais.
    """
    
    # Configurações da API OpenWeatherMap
    OPENWEATHER_API_KEY = os.getenv('5f412107ccba21994bcbfd7565c75a1e')
    OPENWEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5'
    
    # Configurações do Flask
    SECRET_KEY = os.getenv('12345',)
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Configurações de atualização de dados
    WEATHER_UPDATE_INTERVAL = int(os.getenv('WEATHER_UPDATE_INTERVAL', '300'))  # 5 minutos em segundos
    
    # Configurações de localização padrão (pode ser alterada pelo utilizador)
    DEFAULT_LATITUDE = float(os.getenv('DEFAULT_LATITUDE', '40.6405'))  # Aveiro, Portugal
    DEFAULT_LONGITUDE = float(os.getenv('DEFAULT_LONGITUDE', '-8.6538'))
    DEFAULT_CITY = os.getenv('DEFAULT_CITY', 'Aveiro')
    
    # Configurações de recomendações agrícolas
    TEMP_IDEAL_MIN = float(os.getenv('TEMP_IDEAL_MIN', '15.0'))  # Celsius
    TEMP_IDEAL_MAX = float(os.getenv('TEMP_IDEAL_MAX', '25.0'))  # Celsius
    HUMIDITY_IDEAL_MIN = float(os.getenv('HUMIDITY_IDEAL_MIN', '60.0'))  # Percentagem
    HUMIDITY_IDEAL_MAX = float(os.getenv('HUMIDITY_IDEAL_MAX', '80.0'))  # Percentagem
    
    # Limiares para recomendações
    IRRIGATION_HUMIDITY_THRESHOLD = float(os.getenv('IRRIGATION_HUMIDITY_THRESHOLD', '40.0'))
    RAIN_THRESHOLD_MM = float(os.getenv('RAIN_THRESHOLD_MM', '5.0'))  # mm nas próximas 24h
    
    @classmethod
    def validate_config(cls):
        """
        Valida se todas as configurações essenciais estão definidas.
        
        Returns:
            bool: True se todas as configurações estão válidas
            
        Raises:
            ValueError: Se alguma configuração essencial estiver em falta
        """
        if cls.OPENWEATHER_API_KEY == 'your_api_key_here':
            raise ValueError("API Key do OpenWeatherMap não configurada. "
                           "Defina OPENWEATHER_API_KEY no ficheiro .env")
        
        if not cls.SECRET_KEY or cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            print("AVISO: Usando SECRET_KEY padrão. Altere para produção!")
        
        return True


class DevelopmentConfig(Config):
    """Configuração para ambiente de desenvolvimento."""
    DEBUG = True
    WEATHER_UPDATE_INTERVAL = 60  # Atualiza a cada minuto para testes


class ProductionConfig(Config):
    """Configuração para ambiente de produção."""
    DEBUG = False
    WEATHER_UPDATE_INTERVAL = 300  # Atualiza a cada 5 minutos


class TestingConfig(Config):
    """Configuração para ambiente de testes."""
    TESTING = True
    WEATHER_UPDATE_INTERVAL = 10  # Atualização rápida para testes
    OPENWEATHER_API_KEY = 'test_api_key'  # API key falsa para tests