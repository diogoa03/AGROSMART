from typing import List, Optional, Dict
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.models.notificacao import Notificacao
from src.database import get_db
from src.utils.logger import Logger

class NotificacaoService:
    def __init__(self):
        self.db: Session = next(get_db())
        self.logger = Logger(__name__)

    def criar(self, titulo: str, mensagem: str, tipo: str, usuario_id: int) -> Optional[Notificacao]:
        """
        Cria uma nova notificação.
        
        Args:
            titulo (str): Título da notificação
            mensagem (str): Conteúdo da notificação
            tipo (str): Tipo da notificação (ALERTA, INFO, etc)
            usuario_id (int): ID do usuário destinatário
            
        Returns:
            Optional[Notificacao]: Notificação criada ou None em caso de erro
        """
        try:
            notificacao = Notificacao(
                titulo=titulo,
                mensagem=mensagem,
                tipo=tipo,
                usuario_id=usuario_id,
                data_criacao=datetime.now(),
                lida=False
            )
            self.db.add(notificacao)
            self.db.commit()
            self.db.refresh(notificacao)
            
            self.logger.info(f"Notificação criada para usuário {usuario_id}")
            return notificacao
            
        except SQLAlchemyError as e:
            self.db.rollback()
            self.logger.error(f"Erro ao criar notificação: {str(e)}")
            return None

    def listar_por_usuario(self, usuario_id: int) -> List[Notificacao]:
        """Lista todas as notificações de um usuário."""
        try:
            return self.db.query(Notificacao)\
                .filter(Notificacao.usuario_id == usuario_id)\
                .order_by(Notificacao.data_criacao.desc())\
                .all()
                
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao listar notificações: {str(e)}")
            return []

    def marcar_como_lida(self, notificacao_id: int) -> bool:
        """Marca uma notificação como lida."""
        try:
            notificacao = self.db.query(Notificacao)\
                .filter(Notificacao.id == notificacao_id)\
                .first()
                
            if notificacao:
                notificacao.lida = True
                notificacao.data_leitura = datetime.now()
                self.db.commit()
                return True
            return False
            
        except SQLAlchemyError as e:
            self.db.rollback()
            self.logger.error(f"Erro ao marcar notificação como lida: {str(e)}")
            return False