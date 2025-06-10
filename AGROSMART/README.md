# AGROSMART (Versão Simplificada)

## Descrição

**AgroSmart** é um sistema simplificado de gestão agrícola construído com backend em Python Flask e frontend em React. Recolhe dados meteorológicos em tempo real através da API OpenWeatherMap e fornece recomendações de irrigação baseadas nas condições meteorológicas atuais.

## Funcionalidades

- **Monitorização Meteorológica:** Recolha automática de dados meteorológicos (temperatura, humidade, precipitação)
- **Recomendações Inteligentes:** Sugestões de irrigação baseadas em dados meteorológicos
- **Armazenamento JSON Simples:** Armazenamento de dados local baseado em ficheiros
- **API REST:** Endpoints simples para integração
- **Interface React:** Interface web moderna e responsiva
- **Sistema de Registos:** Registos detalhados do sistema para monitorização

## Estrutura do Projeto

```
AGROSMART/
│
├── backend/                # Backend Flask
│   ├── app.py             # Aplicação Flask principal
│   ├── src/
│   │   ├── services/      # Lógica de negócio
│   │   │   ├── weather_service.py
│   │   │   └── recomendacao_service.py
│   │   ├── storage/       # Armazenamento de dados
│   │   │   └── data_store.py
│   │   └── utils/        # Utilitários
│   │       └── logger.py
│   ├── data/             # Diretório de armazenamento JSON
│   └── requirements.txt  # Dependências Python
│
├── frontend/              # Frontend React
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── pages/
│   │   └── App.tsx
│   ├── package.json
│   └── tsconfig.json
│
├── .env                  # Variáveis de ambiente
└── README.md            # Este ficheiro
```

## Configuração e Execução

### Configuração do Backend

1. Navegar para o diretório backend:
```sh
cd backend
```

2. Criar ambiente virtual e instalar dependências:
```sh
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Copiar `.env.example` para `.env` e preencher a chave API do OpenWeatherMap:
```sh
copy .env.example .env
```

4. Executar o backend Flask:
```sh
python app.py
```

### Configuração do Frontend

1. Navegar para o diretório frontend:
```sh
cd frontend
```

2. Instalar dependências:
```sh
npm install
```

3. Executar servidor de desenvolvimento React:
```sh
npm start
```

Aceder à aplicação em [http://localhost:3000](http://localhost:3000)
API Backend disponível em [http://localhost:5000](http://localhost:5000)

## Endpoints da API

- `GET /api/weather` - Obter dados meteorológicos atuais
- `GET /api/recommendations` - Obter recomendações de irrigação
- `GET /api/history/weather` - Obter histórico meteorológico

## Tecnologias Utilizadas

Backend:
- Python 3.10+
- Flask
- Requests (para chamadas API)
- JSON (para armazenamento de dados)

Frontend:
- React 18
- TypeScript
- Material-UI
- Axios

## Equipa

- Guilherme Mota
- Diogo A.
- José Folha

## Licença

Este projeto é apenas para fins académicos.

---

> **Nota:** Lembre-se de atualizar a sua chave API do OpenWeatherMap no ficheiro `.env`.