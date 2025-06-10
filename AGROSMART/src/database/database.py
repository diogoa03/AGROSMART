from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from src.config.settings import settings
from src.utils.logger import Logger

logger = Logger(__name__)

def create_database_engine(url: str, **kwargs) -> Engine:
    """Cria e configura o engine do banco de dados."""
    try:
        default_settings = {
            'pool_size': 5,
            'max_overflow': 10,
            'pool_timeout': 30,
            'pool_recycle': 1800,
            'echo': settings.DEBUG
        }
        default_settings.update(kwargs)
        
        if url.startswith('sqlite'):
            default_settings.pop('pool_size', None)
            default_settings.pop('max_overflow', None)
            default_settings['connect_args'] = {'check_same_thread': False}
            
        return create_engine(url, **default_settings)
        
    except Exception as e:
        logger.error(f"Erro ao criar engine: {str(e)}")
        raise

try:
    engine = create_database_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
except Exception as e:
    logger.critical(f"Falha ao inicializar banco: {str(e)}")
    raise

@contextmanager
def db_session() -> Generator[Session, None, None]:
    """Gerenciador de contexto para sessões do banco."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Erro na sessão: {str(e)}")
        raise
    finally:
        session.close()

def get_db() -> Generator[Session, None, None]:
    """Cria uma sessão de banco de dados."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def check_database_connection() -> bool:
    """Verifica se a conexão com o banco está funcionando."""
    try:
        with db_session() as session:
            session.execute("SELECT 1")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Erro na conexão: {str(e)}")
        return False