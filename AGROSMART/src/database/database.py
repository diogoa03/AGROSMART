from contextlib import contextmanager
from typing import Generator, Any
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine  # Corrigido aqui
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from src.config.settings import Settings
from src.utils.logger import Logger

logger = Logger(__name__)

def create_database_engine(url: str, **kwargs) -> Engine:
    """
    Cria e configura o engine do banco de dados.
    
    Args:
        url: String de conexão com o banco de dados
        **kwargs: Argumentos adicionais para configuração
        
    Returns:
        Engine: Engine configurado do SQLAlchemy
        
    Raises:
        SQLAlchemyError: Se houver erro na criação do engine
    """
    try:
        # Configurações padrão do engine
        default_settings = {
            'pool_size': 5,
            'max_overflow': 10,
            'pool_timeout': 30,
            'pool_recycle': 1800,
            'echo': Settings.DEBUG
        }
        
        # Atualiza com argumentos fornecidos
        default_settings.update(kwargs)
        
        # Cria o engine com tratamento para SQLite
        if url.startswith('sqlite'):
            default_settings.pop('pool_size', None)
            default_settings.pop('max_overflow', None)
            default_settings['connect_args'] = {'check_same_thread': False}
            
        return create_engine(url, **default_settings)
        
    except Exception as e:
        logger.error(f"Erro ao criar engine do banco: {str(e)}")
        raise

try:
    engine = create_database_engine(Settings.DATABASE_URL)
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
except Exception as e:
    logger.critical(f"Falha ao inicializar banco de dados: {str(e)}")
    raise

@contextmanager
def db_session() -> Generator[Session, None, None]:
    """
    Gerenciador de contexto para sessões do banco.
    
    Yields:
        Session: Sessão do SQLAlchemy
        
    Example:
        with db_session() as session:
            session.query(Model).all()
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Erro na sessão do banco: {str(e)}", 
                    extra={'error': str(e), 'type': type(e).__name__})
        raise
    finally:
        if session:
            session.close()

def get_db() -> Generator[Session, None, None]:
    """
    Cria uma sessão de banco de dados para dependency injection.
    
    Yields:
        Session: Sessão do SQLAlchemy
        
    Example:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    session = None
    try:
        session = SessionLocal()
        yield session
    except SQLAlchemyError as e:
        logger.error(f"Erro na sessão do banco: {str(e)}", 
                    extra={'error': str(e), 'type': type(e).__name__})
        raise
    finally:
        if session:
            session.close()

def check_database_connection() -> bool:
    """
    Verifica se a conexão com o banco está funcionando.
    
    Returns:
        bool: True se conectado, False caso contrário
    """
    try:
        with db_session() as session:
            session.execute("SELECT 1")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Erro na conexão com banco: {str(e)}", 
                    extra={'error': str(e), 'type': type(e).__name__})
        return False