# Sistema de Agricultura Inteligente

Sistema de monitoramento meteorológico e recomendações para agricultura.

## Funcionalidades

- Monitoramento de dados meteorológicos em tempo real
- Recomendações inteligentes para agricultura
- Dashboard web interativo
- Comunicação WebSocket para atualizações em tempo real
- API REST completa

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente virtual: `venv\Scripts\activate` (Windows)
4. Instale as dependências: `pip install -r requirements.txt`
5. Configure as variáveis de ambiente: `copy .env.example .env`
6. Configure o banco de dados: `python scripts/setup_database.py`
7. Execute o sistema: `python main.py`

## Testes

Execute os testes com: `pytest tests/`
