# AGROSMART

## Descrição

O **AgroSmart** é um sistema distribuído para gestão agrícola inteligente, desenvolvido em Python com Flask no backend e React no frontend. O sistema recolhe dados meteorológicos em tempo real da API OpenWeatherMap, monitoriza continuamente as condições atmosféricas e sugere práticas agrícolas como irrigação e fertilização, promovendo sustentabilidade e eficiência.

## Funcionalidades

- **Monitorização Meteorológica:** Consulta automática e periódica dos dados de temperatura, humidade, precipitação e previsão de chuva.
- **Recomendações Inteligentes:** Sugestão de ações agrícolas (rega, fertilização, etc.) com base nos dados recolhidos.
- **Notificações em Tempo Real:** Envio de alertas e recomendações via WebSockets.
- **Interface Web Responsiva:** Frontend minimalista em React.
- **API RESTful:** Endpoints seguros para integração e automação.
- **Documentação Automática:** Código documentado com Sphinx.
- **Testes Unitários:** Cobertura de funcionalidades críticas.
- **Trabalho Colaborativo:** Projeto versionado no GitHub.

## Estrutura do Projeto

```
AGROSMART/
│
├── app.py                  # Aplicação Flask principal
├── src/                    # Código-fonte backend (serviços, modelos, utils)
├── frontend-agrosmart/     # Aplicação React (frontend)
├── tests/                  # Testes unitários
├── docs/                   # Documentação Sphinx
├── .env                    # Variáveis de ambiente (NÃO versionar)
├── .env.example            # Exemplo de variáveis de ambiente
├── requirements.txt        # Dependências Python
├── README.md               # Este ficheiro
└── websocket_server.py     # Servidor WebSocket
```

## Como executar

### 1. Clonar o repositório

```sh
git clone https://github.com/diogoa03/AGROSMART.git
cd AGROSMART
```

### 2. Configurar variáveis de ambiente

Copie o ficheiro `.env.example` para `.env` e preencha com os seus dados:

```sh
cp .env.example .env
```

### 3. Instalar dependências do backend

```sh
pip install -r requirements.txt
```

### 4. Executar o backend

```sh
python app.py
```

### 5. Executar o frontend

```sh
cd frontend-agrosmart
npm install
npm start
```

Aceda a [http://localhost:3000](http://localhost:3000) para ver a interface.

## Testes

Para correr os testes unitários:

```sh
pytest tests/
```

## Documentação

A documentação técnica é gerada com Sphinx e pode ser consultada na pasta `docs/`.

## Tecnologias Utilizadas

- **Python 3.10+**
- **Flask**
- **SQLAlchemy**
- **WebSockets**
- **React**
- **Sphinx**
- **pytest**

## Equipa

- Guilherme Mota
- Diogo A.
- José Folha

## Licença

Este projeto é apenas para fins académicos.

---

> **Nota:** Para produção, altere as chaves e configurações sensíveis no ficheiro `.env`.