# AGROSMART (Versão Simplificada)

## Descrição

**AgroSmart** é um sistema simplificado de gestão agrícola construído com backend em Python Flask (com suporte a Socket.IO) e frontend em React. Recolhe dados meteorológicos em tempo real através da API OpenWeatherMap e fornece recomendações de irrigação baseadas nas condições meteorológicas atuais.

## Funcionalidades

- **Monitorização Meteorológica:** Recolha automática de dados meteorológicos (temperatura, humidade, precipitação)
- **Recomendações Inteligentes:** Sugestões de irrigação baseadas em dados meteorológicos
- **Armazenamento JSON Simples:** Armazenamento de dados local baseado em ficheiros
- **API REST:** Endpoints simples para integração
- **Interface React:** Interface web moderna e responsiva
- **Sistema de Registos:** Registos detalhados do sistema para monitorização
- **Atualização em tempo real:** O frontend recebe atualizações automáticas via Socket.IO sempre que há novos dados meteorológicos

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
│   │   └── utils/         # Utilitários
│   │       └── logger.py
│   ├── data/              # Diretório de armazenamento JSON
│   └── requirements.txt   # Dependências Python
│
├── frontend/               # Frontend React
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── pages/
│   │   └── App.tsx
│   ├── package.json
│   └── tsconfig.json
│
├── .env                    # Variáveis de ambiente
└── README.md               # Este ficheiro
```

## Configuração e Execução

### 1. Configuração do Backend

1. Navegue para o diretório backend:
    ```sh
    cd backend
    ```

2. Crie o ambiente virtual e instale as dependências:
    ```sh
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. Copie `.env.example` para `.env` e preencha a chave API do OpenWeatherMap:
    ```sh
    copy .env.example .env
    ```

4. **Instale o Flask-SocketIO e eventlet** (necessário para WebSocket funcionar):
    ```sh
    pip install flask-socketio eventlet
    ```

5. Execute o backend **usando o socketio.run** (não use `flask run`):
    ```sh
    python app.py
    ```

    O backend estará disponível em [http://localhost:5000](http://localhost:5000)

### 2. Configuração do Frontend

1. Navegue para o diretório frontend:
    ```sh
    cd frontend
    ```

2. Instale as dependências:
    ```sh
    npm install
    ```

3. Execute o servidor de desenvolvimento React:
    ```sh
    npm start
    ```

    O frontend estará disponível em [http://localhost:3000](http://localhost:3000)

### 3. Comunicação em Tempo Real (Socket.IO)

- O backend já está configurado para emitir eventos `weather_update` via Socket.IO.
- No frontend, o componente `Weather.tsx` deve usar o pacote `socket.io-client` para receber atualizações em tempo real.
- Certifique-se de instalar o pacote no frontend:
    ```sh
    npm install socket.io-client
    ```
- Exemplo de uso no React:
    ```tsx
    import { io } from "socket.io-client";
    const socket = io("http://localhost:5000", { transports: ["websocket"] });
    socket.on("weather_update", (data) => {
        // Atualize o estado do componente com os novos dados
    });
    ```

## Endpoints da API

- `GET /api/weather` - Obter dados meteorológicos atuais
- `GET /api/recommendations` - Obter recomendações de irrigação
- `GET /api/history/weather` - Obter histórico meteorológico
- `GET /api/notifications` - Obter notificações
- `DELETE /api/notifications` - Limpar notificações

## Tecnologias Utilizadas

Backend:
- Python 3.10+
- Flask
- Flask-SocketIO
- Requests (para chamadas API)
- JSON (para armazenamento de dados)
- eventlet (para WebSocket)

Frontend:
- React 18
- TypeScript
- Material-UI
- Axios
- socket.io-client

## Equipa

- Guilherme Mota
- Diogo A.
- José Folha

## Licença

Este projeto é apenas para fins académicos.

---

> **Nota:** Lembre-se de atualizar a sua chave API do OpenWeatherMap no ficheiro `.env`.