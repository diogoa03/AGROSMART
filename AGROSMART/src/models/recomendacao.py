from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Dict, Any
from enum import Enum as PyEnum

Base = declarative_base()

class PrioridadeEnum(PyEnum):
    """Enumeração para prioridades de recomendação."""
    BAIXA = "BAIXA"
    MEDIA = "MÉDIA"
    ALTA = "ALTA"

class Recomendacao(Base):
    """
    Modelo de recomendação do sistema.
    
    Attributes:
        id (int): Identificador único da recomendação
        descricao (str): Descrição detalhada da recomendação
        prioridade (str): Nível de prioridade (BAIXA, MÉDIA, ALTA)
        data_criacao (datetime): Data de criação da recomendação
        sensor_id (int): ID do sensor que gerou os dados
        implementada (bool): Indica se a recomendação foi implementada
        data_implementacao (datetime): Data em que foi implementada
    """
    
    __tablename__ = 'recomendacoes'
    
    # Colunas do banco
    id = Column(Integer, primary_key=True)
    descricao = Column(String(500), nullable=False)
    prioridade = Column(Enum(PrioridadeEnum), nullable=False)
    data_criacao = Column(DateTime, default=datetime.now, nullable=False)
    sensor_id = Column(Integer, ForeignKey('sensores.id'), nullable=False)
    implementada = Column(Boolean, default=False)
    data_implementacao = Column(DateTime, nullable=True)
    
    # Relacionamentos
    sensor = relationship("Sensor", back_populates="recomendacoes")
    
    def __init__(self, **kwargs):
        """Inicializa uma nova recomendação."""
        super().__init__(**kwargs)
        self.validate()
    
    def validate(self) -> None:
        """
        Valida os dados da recomendação.
        
        Raises:
            ValueError: Se algum campo estiver inválido
        """
        if not self.descricao or len(self.descricao) > 500:
            raise ValueError("Descrição inválida ou muito longa")
        if not isinstance(self.prioridade, PrioridadeEnum):
            raise ValueError(f"Prioridade inválida. Use: {', '.join(p.value for p in PrioridadeEnum)}")
    
    def marcar_como_implementada(self) -> None:
        """Marca a recomendação como implementada, registrando a data."""
        if not self.implementada:
            self.implementada = True
            self.data_implementacao = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte a recomendação para dicionário.
        
        Returns:
            Dict com os dados da recomendação
        """
        return {
            "id": self.id,
            "descricao": self.descricao,
            "prioridade": self.prioridade.value,
            "data_criacao": self.data_criacao.isoformat(),
            "sensor_id": self.sensor_id,
            "implementada": self.implementada,
            "data_implementacao": self.data_implementacao.isoformat() if self.data_implementacao else None
        }

    def __repr__(self) -> str:
        """Representação string do objeto."""
        return f"<Recomendacao(id={self.id}, prioridade='{self.prioridade.value}')>"