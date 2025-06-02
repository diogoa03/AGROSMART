from contextlib import contextmanager
from typing import Generator, Any
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from src.config.settings import Settings
from src.utils.logger import Logger

logger = Logger(__name__)

def create_database_engine(url: str) -> Engine:
    """
    Cria e configura o engine do banco de dados.
    
    Args:
        url: String de conexão com o banco de dados
        
    Returns:
        Engine: Engine configurado do SQLAlchemy
        
    Raises:
        SQLAlchemyError: Se houver erro na criação do engine
    """
    try:
        return create_engine(
            url,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800
        )
    except Exception as e:
        logger.error(f"Erro ao criar engine do banco: {str(e)}")
        raise

engine = create_database_engine(Settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
        logger.error(f"Erro na sessão do banco: {str(e)}")
        raise
    finally:
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
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Erro na sessão do banco: {str(e)}")
        raise
    finally:
        db.close()

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
        logger.error(f"Erro na conexão com banco: {str(e)}")
        return False