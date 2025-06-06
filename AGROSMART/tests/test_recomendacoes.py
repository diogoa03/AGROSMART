import pytest
from datetime import datetime
from src.models.recomendacao import Recomendacao, PrioridadeEnum

class TestRecomendacao:
    @pytest.fixture
    def recomendacao_valida(self):
        """Fixture para criar uma recomendação válida."""
        return Recomendacao(
            descricao="Necessária irrigação imediata",
            prioridade=PrioridadeEnum.ALTA,
            sensor_id=1
        )
    
    def test_criar_recomendacao_valida(self, recomendacao_valida):
        """Testa criação de recomendação com dados válidos."""
        assert recomendacao_valida.descricao == "Necessária irrigação imediata"
        assert recomendacao_valida.prioridade == PrioridadeEnum.ALTA
        assert not recomendacao_valida.implementada
        
    def test_validacao_descricao_vazia(self):
        """Testa validação de descrição vazia."""
        with pytest.raises(ValueError) as exc:
            Recomendacao(
                descricao="",
                prioridade=PrioridadeEnum.ALTA,
                sensor_id=1
            )
        assert "Descrição inválida" in str(exc.value)
        
    def test_validacao_prioridade_invalida(self):
        """Testa validação de prioridade inválida."""
        with pytest.raises(ValueError) as exc:
            Recomendacao(
                descricao="Teste",
                prioridade="INVALID",
                sensor_id=1
            )
        assert "Prioridade inválida" in str(exc.value)
        
    def test_marcar_como_implementada(self, recomendacao_valida):
        """Testa marcação de recomendação como implementada."""
        assert not recomendacao_valida.implementada
        assert recomendacao_valida.data_implementacao is None
        
        recomendacao_valida.marcar_como_implementada()
        
        assert recomendacao_valida.implementada
        assert isinstance(recomendacao_valida.data_implementacao, datetime)
        
    def test_to_dict(self, recomendacao_valida):
        """Testa conversão para dicionário."""
        dict_data = recomendacao_valida.to_dict()
        
        assert dict_data["descricao"] == "Necessária irrigação imediata"
        assert dict_data["prioridade"] == "ALTA"
        assert not dict_data["implementada"]
        assert dict_data["data_implementacao"] is None