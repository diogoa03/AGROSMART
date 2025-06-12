# AGROSMART 

## Descrição

**AgroSmart** é um sistema de gestão agrícola construído com backend em Python Flask e frontend em React. Recolhe dados meteorológicos em tempo real através da API OpenWeatherMap e fornece recomendações de rega baseadas nas condições meteorológicas atuais.

## Funcionalidades

- **Monitorização Meteorológica:** Recolha automática de dados meteorológicos (temperatura, humidade, precipitação)
- **Recomendações Inteligentes:** Sugestões de rega baseadas em dados meteorológicos
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
│   ├── tests/            # Testes unitários
│   │   ├── test_weather_service.py
│   │   ├── test_recomendacao_service.py
│   │   ├── test_notification_service.py
│   │   └── test_user_auth.py
│   ├── docs/             # Documentação Sphinx
│   │   ├── source/
│   │   └── build/
│   └── requirements.txt  # Dependências Python
│
├── frontend/              # Frontend React
│   ├── public/
│   ├── src/
│   │   ├── components/   # Componentes React
│   │   ├── services/     # Lógica de chamadas API
│   │   ├── pages/        # Páginas principais
│   │   └── App.tsx
│   ├── package.json
│   └── tsconfig.json
│
├── .env                  # Variáveis de ambiente
├── .env.example          # Exemplo de variáveis de ambiente
└── [README.md]           # Este ficheiro
```

## Configuração e Execução

### Configuração do Backend

1. Navegar para a diretoria backend:
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

1. Navegar para a diretoria frontend:
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
- `GET /api/recommendations` - Obter recomendações de rega
- `GET /api/history/weather` - Obter histórico meteorológico
- `POST /api/login` - Autenticação de utilizadores
- `GET /api/notifications` - Obter notificações ativas (parâmetro opcional: severity=HIGH/MEDIUM/LOW)
- `DELETE /api/notifications` - Limpar todas as notificações

## Tecnologias Utilizadas

Backend:
- Python 3.10+
- Flask (Framework Web)
- Requests (para chamadas API)
- JSON (para armazenamento de dados)
- Werkzeug (para segurança)

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

> **Nota:** Não se esqueça de atualizar a sua chave API do OpenWeatherMap no ficheiro `.env`.