from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Dict, Any

Base = declarative_base()

class Notificacao(Base):
    """
    Modelo de notificação do sistema.
    
    Attributes:
        id (int): Identificador único da notificação
        titulo (str): Título da notificação (max 100 chars)
        mensagem (str): Conteúdo da notificação (max 500 chars)
        tipo (str): Tipo da notificação (ALERTA, INFO, AVISO)
        usuario_id (int): ID do usuário destinatário
        data_criacao (datetime): Data de criação da notificação
        lida (bool): Indica se a notificação foi lida
        data_leitura (datetime): Data em que a notificação foi lida
    """
    
    __tablename__ = 'notificacoes'
    
    # Colunas do banco
    id = Column(Integer, primary_key=True)
    titulo = Column(String(100), nullable=False)
    mensagem = Column(String(500), nullable=False)
    tipo = Column(String(20), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    data_criacao = Column(DateTime, default=datetime.now, nullable=False)
    lida = Column(Boolean, default=False)
    data_leitura = Column(DateTime, nullable=True)
    
    # Relacionamentos
    usuario = relationship("Usuario", back_populates="notificacoes")
    
    # Tipos válidos de notificação
    TIPOS_VALIDOS = ["ALERTA", "INFO", "AVISO"]
    
    def __init__(self, **kwargs):
        """Inicializa uma nova notificação."""
        super().__init__(**kwargs)
        self.validate()
    
    def validate(self) -> None:
        """
        Valida os dados da notificação.
        
        Raises:
            ValueError: Se algum campo estiver inválido
        """
        if not self.titulo or len(self.titulo) > 100:
            raise ValueError("Título inválido ou muito longo")
        if not self.mensagem or len(self.mensagem) > 500:
            raise ValueError("Mensagem inválida ou muito longa")
        if self.tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo inválido. Use: {', '.join(self.TIPOS_VALIDOS)}")
    
    def marcar_como_lida(self) -> None:
        """Marca a notificação como lida, registrando a data."""
        if not self.lida:
            self.lida = True
            self.data_leitura = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte a notificação para dicionário.
        
        Returns:
            Dict com os dados da notificação
        """
        return {
            "id": self.id,
            "titulo": self.titulo,
            "mensagem": self.mensagem,
            "tipo": self.tipo,
            "usuario_id": self.usuario_id,
            "data_criacao": self.data_criacao.isoformat(),
            "lida": self.lida,
            "data_leitura": self.data_leitura.isoformat() if self.data_leitura else None
        }

    def __repr__(self) -> str:
        """Representação string do objeto."""
        return f"<Notificacao(id={self.id}, titulo='{self.titulo}', tipo='{self.tipo}')>"