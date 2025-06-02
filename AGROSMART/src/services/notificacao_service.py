from typing import List, Optional, Dict, Any
from datetime import datetime
import bleach
from dataclasses import dataclass
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
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
    MAX_TITULO_LENGTH = 100
    MAX_MENSAGEM_LENGTH = 500
    
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
            # Sanitiza e valida entrada
            titulo = self._sanitize_input(titulo)
            mensagem = self._sanitize_input(mensagem)
            tipo = tipo.upper()
            
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
            
            self.logger.info(
                f"Notificação criada para usuário {usuario_id}",
                extra={
                    "notificacao_id": notificacao.id,
                    "tipo": tipo,
                    "usuario_id": usuario_id
                }
            )
            
            return NotificacaoResponse(
                success=True,
                data=self._to_dict(notificacao),
                message="Notificação criada com sucesso"
            )
            
        except ValueError as e:
            self.logger.error(
                f"Erro de validação: {str(e)}",
                extra={"usuario_id": usuario_id, "tipo": tipo}
            )
            return NotificacaoResponse(
                success=False,
                status=400,
                message=str(e)
            )
            
        except SQLAlchemyError as e:
            self.db.rollback()
            self.logger.error(
                f"Erro ao criar notificação: {str(e)}",
                extra={
                    "usuario_id": usuario_id,
                    "error_type": type(e).__name__
                }
            )
            return NotificacaoResponse(
                success=False,
                status=500,
                message="Erro interno ao criar notificação"
            )

    def listar_por_usuario(self, usuario_id: int, page: int = 1, per_page: int = 20) -> NotificacaoResponse:
        """
        Lista notificações de um usuário com paginação.
        
        Args:
            usuario_id: ID do usuário
            page: Número da página (default: 1)
            per_page: Itens por página (default: 20)
        """
        try:
            offset = (page - 1) * per_page
            notificacoes = self.db.query(Notificacao)\
                .filter(Notificacao.usuario_id == usuario_id)\
                .order_by(Notificacao.data_criacao.desc())\
                .offset(offset)\
                .limit(per_page)\
                .all()
                
            total = self.db.query(Notificacao)\
                .filter(Notificacao.usuario_id == usuario_id)\
                .count()
                
            return NotificacaoResponse(
                success=True,
                data={
                    "notificacoes": [self._to_dict(n) for n in notificacoes],
                    "total": total,
                    "page": page,
                    "per_page": per_page,
                    "pages": (total + per_page - 1) // per_page
                }
            )
                
        except SQLAlchemyError as e:
            self.logger.error(
                f"Erro ao listar notificações: {str(e)}",
                extra={"usuario_id": usuario_id}
            )
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
                self.logger.warning(
                    f"Notificação {notificacao_id} não encontrada",
                    extra={"notificacao_id": notificacao_id}
                )
                return NotificacaoResponse(
                    success=False,
                    status=404,
                    message="Notificação não encontrada"
                )

            if notificacao.lida:
                return NotificacaoResponse(
                    success=True,
                    data=self._to_dict(notificacao),
                    message="Notificação já estava marcada como lida"
                )

            notificacao.lida = True
            notificacao.data_leitura = datetime.now()
            self.db.commit()
            
            self.logger.info(
                f"Notificação {notificacao_id} marcada como lida",
                extra={"notificacao_id": notificacao_id}
            )
            
            return NotificacaoResponse(
                success=True,
                data=self._to_dict(notificacao),
                message="Notificação marcada como lida"
            )
            
        except SQLAlchemyError as e:
            self.db.rollback()
            self.logger.error(
                f"Erro ao marcar notificação: {str(e)}",
                extra={
                    "notificacao_id": notificacao_id,
                    "error_type": type(e).__name__
                }
            )
            return NotificacaoResponse(
                success=False,
                status=500,
                message="Erro ao atualizar notificação"
            )

    def _validar_dados(self, titulo: str, mensagem: str, tipo: str) -> None:
        """Valida os dados da notificação."""
        if not titulo or len(titulo) < 3:
            raise ValueError("Título deve ter pelo menos 3 caracteres")
        if len(titulo) > self.MAX_TITULO_LENGTH:
            raise ValueError(f"Título não pode ter mais que {self.MAX_TITULO_LENGTH} caracteres")
        if not mensagem:
            raise ValueError("Mensagem não pode estar vazia")
        if len(mensagem) > self.MAX_MENSAGEM_LENGTH:
            raise ValueError(f"Mensagem não pode ter mais que {self.MAX_MENSAGEM_LENGTH} caracteres")
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo inválido. Use: {', '.join(self.TIPOS_VALIDOS)}")

    def _sanitize_input(self, text: str) -> str:
        """Sanitiza entrada de texto para prevenir XSS."""
        return bleach.clean(text.strip())

    def _to_dict(self, notificacao: Notificacao) -> Dict[str, Any]:
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