from contextlib import contextmanager
from typing import Generator, Any
from sqlalchemy import create_engine, Engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from src.config.settings import settings  # Alterado para importar a instância
from src.utils.logger import Logger

logger = Logger(__name__)

def create_database_engine(url: str, **kwargs) -> Engine:
    ...
    default_settings = {
        'pool_size': 5,
        'max_overflow': 10,
        'pool_timeout': 30,
        'pool_recycle': 1800,
        'echo': settings.DEBUG  # Alterado
    }
    ...
try:
    engine = create_database_engine(settings.DATABASE_URL)  # Alterado
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
except Exception as e:
    logger.critical(f"Falha ao inicializar banco de dados: {str(e)}")
    raise

...

def check_database_connection() -> bool:
    """
    Verifica se a conexão com o banco está funcionando.
    """
    try:
        with db_session() as session:
            session.execute(text("SELECT 1"))  # Alterado
        return True
    except SQLAlchemyError as e:
        logger.error(f"Erro na conexão com banco: {str(e)}", 
                    extra={'error': str(e), 'type': type(e).__name__})
        return False