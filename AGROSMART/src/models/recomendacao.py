from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Recomendacao(Base):
    """Modelo de recomendação."""
    
    __tablename__ = 'recomendacoes'
    
    id = Column(Integer, primary_key=True)
    descricao = Column(String(500), nullable=False)
    prioridade = Column(String(20), nullable=False)
    cultura_id = Column(Integer, ForeignKey('culturas.id'), nullable=False)
    data_criacao = Column(DateTime, default=datetime.now, nullable=False)
    
    def __repr__(self):
        return f"<Recomendacao(id={self.id}, prioridade='{self.prioridade}')>"