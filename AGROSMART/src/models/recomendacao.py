from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Dict, Any
from enum import Enum as PyEnum

Base = declarative_base()

class PrioridadeEnum(PyEnum):
    """Enumeração para prioridades de recomendação."""
    BAIXA = "BAIXA"
    MEDIA = "MEDIA"  # Corrigido: sem acento
    ALTA = "ALTA"

    @classmethod
    def values(cls) -> list[str]:
        """Retorna lista de valores válidos."""
        return [e.value for e in cls]

class Recomendacao(Base):
    """
    Modelo de recomendação do sistema.
    
    Attributes:
        id (int): Identificador único da recomendação
        descricao (str): Descrição da recomendação (max 500 chars)
        prioridade (PrioridadeEnum): Prioridade da recomendação
        data_criacao (datetime): Data de criação da recomendação
        sensor_id (int): ID do sensor relacionado
        implementada (bool): Indica se a recomendação foi implementada
        data_implementacao (datetime): Data de implementação
    """
    __tablename__ = 'recomendacoes'
    
    id = Column(Integer, primary_key=True)
    descricao = Column(String(500), nullable=False)
    prioridade = Column(Enum(PrioridadeEnum), nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow, nullable=False)
    sensor_id = Column(Integer, ForeignKey('sensores.id'), nullable=False)
    implementada = Column(Boolean, default=False)
    data_implementacao = Column(DateTime, nullable=True)
    
    sensor = relationship("Sensor", back_populates="recomendacoes")
    
    def __init__(self, **kwargs):
        if 'prioridade' in kwargs and isinstance(kwargs['prioridade'], str):
            try:
                kwargs['prioridade'] = PrioridadeEnum(kwargs['prioridade'])
            except ValueError:
                raise ValueError(f"Prioridade inválida. Use: {', '.join(PrioridadeEnum.values())}")
        super().__init__(**kwargs)
        self.validate()
    
    def validate(self) -> None:
        if not self.descricao:
            raise ValueError("Descrição não pode estar vazia")
        if len(self.descricao) > 500:
            raise ValueError("Descrição não pode ter mais que 500 caracteres")
        if not isinstance(self.prioridade, PrioridadeEnum):
            raise ValueError(f"Prioridade inválida. Use: {', '.join(PrioridadeEnum.values())}")
        if not self.sensor_id:
            raise ValueError("ID do sensor é obrigatório")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "descricao": self.descricao,
            "prioridade": self.prioridade.value if self.prioridade else None,
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None,
            "sensor_id": self.sensor_id,
            "implementada": self.implementada,
            "data_implementacao": self.data_implementacao.isoformat() if self.data_implementacao else None
        }
    
    def __repr__(self) -> str:
        return f"<Recomendacao(id={self.id}, prioridade='{self.prioridade.value}', sensor_id={self.sensor_id})>"