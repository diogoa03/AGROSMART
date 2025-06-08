from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass
from src.utils.logger import Logger
from src.models.recomendacao import Recomendacao, PrioridadeEnum

@dataclass
class RecomendacaoResponse:
    """Estrutura de resposta para recomendações."""
    success: bool
    data: Optional[Dict] = None
    status: int = 200
    message: str = ""

class RecomendacaoService:
    """Serviço para gerenciamento de recomendações."""
    
    def __init__(self):
        self.logger = Logger(__name__)

    def gerar_recomendacao_irrigacao(self, dados_sensor: Dict) -> RecomendacaoResponse:
        """Gera recomendação baseada em dados do sensor."""
        try:
            self._validar_dados(dados_sensor)
            
            umidade = dados_sensor['umidade']
            temperatura = dados_sensor['temperatura']
            
            recomendacao = Recomendacao()
            recomendacao.data_criacao = datetime.utcnow()
            
            if umidade < 20:
                recomendacao.descricao = "Necessária irrigação imediata"
                recomendacao.prioridade = PrioridadeEnum.ALTA
            elif umidade < 40:
                recomendacao.descricao = "Programar irrigação para as próximas 24h"
                recomendacao.prioridade = PrioridadeEnum.MEDIA
            else:
                recomendacao.descricao = "Níveis de umidade adequados"
                recomendacao.prioridade = PrioridadeEnum.BAIXA
                
            self.logger.info(f"Recomendação gerada: {recomendacao.prioridade.value}")
            return RecomendacaoResponse(
                success=True,
                data=self._to_dict(recomendacao),
                message="Recomendação gerada com sucesso"
            )
            
        except ValueError as e:
            self.logger.error(f"Erro de validação: {str(e)}")
            return RecomendacaoResponse(
                success=False,
                status=400,
                message=str(e)
            )
        
        except Exception as e:
            self.logger.error(f"Erro ao gerar recomendação: {str(e)}")
            return RecomendacaoResponse(
                success=False,
                status=500,
                message="Erro interno ao gerar recomendação"
            )

    def _validar_dados(self, dados: Dict) -> None:
        """Valida dados do sensor."""
        if 'umidade' not in dados:
            raise ValueError("Umidade não informada")
        if 'temperatura' not in dados:
            raise ValueError("Temperatura não informada")
        if dados['umidade'] < 0 or dados['umidade'] > 100:
            raise ValueError("Umidade deve estar entre 0 e 100")
        if dados['temperatura'] < -50 or dados['temperatura'] > 60:
            raise ValueError("Temperatura fora da faixa válida")

    def _to_dict(self, recomendacao: Recomendacao) -> Dict:
        """Converte recomendação para dicionário."""
        return {
            "id": recomendacao.id,
            "descricao": recomendacao.descricao,
            "prioridade": recomendacao.prioridade.value if hasattr(recomendacao.prioridade, "value") else recomendacao.prioridade,
            "data_criacao": recomendacao.data_criacao.isoformat() if recomendacao.data_criacao else None
        }