from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Notificacao(Base):
    """Modelo de notificação."""
    
    __tablename__ = 'notificacoes'
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(100), nullable=False)
    mensagem = Column(String(500), nullable=False)
    tipo = Column(String(20), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    data_criacao = Column(DateTime, default=datetime.now, nullable=False)
    lida = Column(Boolean, default=False)
    data_leitura = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Notificacao(id={self.id}, titulo='{self.titulo}', tipo='{self.tipo}')>"