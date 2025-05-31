from datetime import datetime
from typing import Dict, List
from src.models.recomendacao import Recomendacao

class RecomendacaoService:
    def gerar_recomendacao_irrigacao(self, dados_sensor: Dict) -> Recomendacao:
        if dados_sensor.get('umidade', 0) < 0:
            raise ValueError("Umidade não pode ser negativa")
            
        recomendacao = Recomendacao()
        
        if dados_sensor['umidade'] < 20:
            recomendacao.descricao = "Necessária irrigação imediata"
            recomendacao.prioridade = "ALTA"
        elif dados_sensor['umidade'] < 40:
            recomendacao.descricao = "Programar irrigação para as próximas 24h"
            recomendacao.prioridade = "MÉDIA"
        else:
            recomendacao.descricao = "Níveis de umidade adequados"
            recomendacao.prioridade = "BAIXA"
            
        return recomendacao
    
    def listar_por_cultura(self, cultura_id: int) -> List[Recomendacao]:
        # TODO: Implementar consulta ao banco de dados
        return []