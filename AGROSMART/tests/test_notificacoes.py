import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from src.models.recomendacao import Recomendacao, PrioridadeEnum
from src.services.recomendacao_service import RecomendacaoService, RecomendacaoResponse

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
        
    @pytest.mark.parametrize("descricao,prioridade,sensor_id,expected_error", [
        ("", PrioridadeEnum.ALTA, 1, "Descrição não pode estar vazia"),
        ("A" * 501, PrioridadeEnum.ALTA, 1, "Descrição não pode ter mais que 500 caracteres"),
        ("Teste", "INVALID", 1, "Prioridade inválida"),
        ("Teste", PrioridadeEnum.ALTA, None, "ID do sensor é obrigatório")
    ])
    def test_validacoes_criacao(self, descricao, prioridade, sensor_id, expected_error):
        """Testa diferentes cenários de validação na criação."""
        with pytest.raises(ValueError) as exc:
            Recomendacao(
                descricao=descricao,
                prioridade=prioridade,
                sensor_id=sensor_id
            )
        assert expected_error in str(exc.value)

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

class TestRecomendacaoService:
    @pytest.fixture
    def mock_db_session(self):
        """Fixture para criar mock de sessão do banco."""
        mock = Mock()
        mock.query = Mock(return_value=mock)
        mock.filter = Mock(return_value=mock)
        mock.first = Mock()
        mock.all = Mock(return_value=[])
        return mock

    @pytest.fixture
    def service(self, mock_db_session):
        """Fixture para criar instância do serviço com mock do DB."""
        with patch('src.services.recomendacao_service.get_db') as mock_get_db:
            mock_get_db.return_value = iter([mock_db_session])
            return RecomendacaoService()

    def test_gerar_recomendacao_sucesso(self, service):
        """Testa geração de recomendação com sucesso."""
        dados_sensor = {
            "umidade": 15,
            "temperatura": 25
        }
        
        response = service.gerar_recomendacao_irrigacao(dados_sensor)
        
        assert response.success is True
        assert response.status == 200
        assert "Necessária irrigação imediata" in response.data["descricao"]
        assert response.data["prioridade"] == "ALTA"

    def test_gerar_recomendacao_dados_invalidos(self, service):
        """Testa geração com dados inválidos."""
        dados_sensor = {
            "umidade": -10,  # Inválido
            "temperatura": 25
        }
        
        response = service.gerar_recomendacao_irrigacao(dados_sensor)
        
        assert response.success is False
        assert response.status == 400
        assert "Umidade deve estar entre 0 e 100" in response.message

    def test_erro_banco_dados(self, service):
        """Testa tratamento de erro do banco de dados."""
        dados_sensor = {"umidade": 15, "temperatura": 25}
        service.db.commit.side_effect = Exception("Erro DB")
        
        response = service.gerar_recomendacao_irrigacao(dados_sensor)
        
        assert response.success is False
        assert response.status == 500
        service.db.rollback.assert_called_once()