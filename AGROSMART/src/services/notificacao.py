from typing import List, Optional, Dict
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.models.notificacao import Notificacao
from src.database import get_db
from src.utils.logger import Logger

@dataclass
class NotificacaoResponse:
    """Estrutura de resposta para operações de notificação."""
    success: bool
    data: Optional[Dict] = None
    status: int = 200
    message: str = ""

class NotificacaoService:
    """Serviço para gerenciamento de notificações."""
    
    TIPOS_VALIDOS = ["ALERTA", "INFO", "AVISO"]
    
    def __init__(self):
        """Inicializa o serviço com conexão ao banco e logger."""
        self.db: Session = next(get_db())
        self.logger = Logger(__name__)

    def criar(self, titulo: str, mensagem: str, tipo: str, usuario_id: int) -> NotificacaoResponse:
        """
        Cria uma nova notificação.
        
        Args:
            titulo: Título da notificação
            mensagem: Conteúdo da notificação
            tipo: Tipo da notificação (ALERTA, INFO, AVISO)
            usuario_id: ID do usuário destinatário
            
        Returns:
            NotificacaoResponse com resultado da operação
        """
        try:
            self._validar_dados(titulo, mensagem, tipo)

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
            return NotificacaoResponse(
                success=True,
                data=self._to_dict(notificacao),
                message="Notificação criada com sucesso"
            )
            
        except ValueError as e:
            self.logger.error(f"Erro de validação: {str(e)}")
            return NotificacaoResponse(
                success=False,
                status=400,
                message=str(e)
            )
            
        except SQLAlchemyError as e:
            self.db.rollback()
            self.logger.error(f"Erro ao criar notificação: {str(e)}")
            return NotificacaoResponse(
                success=False,
                status=500,
                message="Erro interno ao criar notificação"
            )

    def listar_por_usuario(self, usuario_id: int) -> NotificacaoResponse:
        """Lista todas as notificações de um usuário."""
        try:
            notificacoes = self.db.query(Notificacao)\
                .filter(Notificacao.usuario_id == usuario_id)\
                .order_by(Notificacao.data_criacao.desc())\
                .all()
                
            return NotificacaoResponse(
                success=True,
                data={"notificacoes": [self._to_dict(n) for n in notificacoes]}
            )
                
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao listar notificações: {str(e)}")
            return NotificacaoResponse(
                success=False,
                status=500,
                message="Erro ao buscar notificações"
            )

    def marcar_como_lida(self, notificacao_id: int) -> NotificacaoResponse:
        """Marca uma notificação como lida."""
        try:
            notificacao = self.db.query(Notificacao)\
                .filter(Notificacao.id == notificacao_id)\
                .first()
                
            if not notificacao:
                return NotificacaoResponse(
                    success=False,
                    status=404,
                    message="Notificação não encontrada"
                )

            notificacao.lida = True
            notificacao.data_leitura = datetime.now()
            self.db.commit()
            
            return NotificacaoResponse(
                success=True,
                data=self._to_dict(notificacao),
                message="Notificação marcada como lida"
            )
            
        except SQLAlchemyError as e:
            self.db.rollback()
            self.logger.error(f"Erro ao marcar notificação: {str(e)}")
            return NotificacaoResponse(
                success=False,
                status=500,
                message="Erro ao atualizar notificação"
            )

    def _validar_dados(self, titulo: str, mensagem: str, tipo: str) -> None:
        """Valida os dados da notificação."""
        if not titulo or len(titulo) < 3:
            raise ValueError("Título deve ter pelo menos 3 caracteres")
        if not mensagem:
            raise ValueError("Mensagem não pode estar vazia")
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo inválido. Use: {', '.join(self.TIPOS_VALIDOS)}")

    def _to_dict(self, notificacao: Notificacao) -> Dict:
        """Converte uma notificação em dicionário."""
        return {
            "id": notificacao.id,
            "titulo": notificacao.titulo,
            "mensagem": notificacao.mensagem,
            "tipo": notificacao.tipo,
            "usuario_id": notificacao.usuario_id,
            "data_criacao": notificacao.data_criacao.isoformat(),
            "lida": notificacao.lida,
            "data_leitura": notificacao.data_leitura.isoformat() if notificacao.data_leitura else None
        }