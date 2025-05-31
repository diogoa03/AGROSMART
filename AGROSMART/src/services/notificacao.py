from typing import List
from datetime import datetime
from src.models.notificacao import Notificacao

class NotificacaoService:
    def criar(self, titulo: str, mensagem: str, tipo: str, usuario_id: int) -> Notificacao:
        notificacao = Notificacao(
            titulo=titulo,
            mensagem=mensagem,
            tipo=tipo,
            usuario_id=usuario_id,
            data_criacao=datetime.now(),
            lida=False
        )
        # TODO: Salvar no banco de dados
        return notificacao
    
    def listar_por_usuario(self, usuario_id: int) -> List[Notificacao]:
        # TODO: Implementar consulta ao banco de dados
        return []
    
    def marcar_como_lida(self, notificacao_id: int) -> bool:
        # TODO: Implementar atualização no banco de dados
        return True