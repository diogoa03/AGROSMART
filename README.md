# AGROSMART 🌱

## 📋 Descrição
AGROSMART é um sistema de gestão agrícola que utiliza Flask e React para fornecer monitorização meteorológica em tempo real e recomendações inteligentes de irrigação.

## ⭐ Funcionalidades

- **Monitorização Meteorológica:** Dados em tempo real (temperatura, humidade, precipitação)
- **Recomendações Inteligentes:** Sistema baseado em condições meteorológicas
- **Interface Moderna:** Dashboard React com atualizações em tempo real
- **WebSocket:** Comunicação bidirecional com Socket.IO
- **API REST:** Endpoints documentados para integração
- **Armazenamento Local:** Sistema de dados baseado em JSON

## 🛠️ Tecnologias

### Backend
- Python 3.10+
- Flask & Flask-SocketIO
- JSON (armazenamento)
- OpenWeatherMap API
- eventlet (WebSocket)

### Frontend
- React 18
- TypeScript
- Material-UI
- Socket.IO Client
- Axios

## 📦 Estrutura
```
AGROSMART/
├── backend/                
│   ├── app.py             # Aplicação principal
│   ├── src/
│   │   ├── services/      # Lógica de negócio
│   │   ├── storage/       # Armazenamento
│   │   └── utils/         # Utilitários
│   ├── data/              # Dados JSON
│   └── requirements.txt    
│
├── frontend/              
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── services/      # Serviços API
│   │   ├── pages/         # Páginas
│   │   └── App.tsx        # Componente principal
│   └── package.json
```

## 🚀 Instalação

### 0. Clonar o Repositório
```bash
# Clone o repositório
git clone https://github.com/diogoa03/AGROSMART.git

# Entre na pasta do projeto
cd AGROSMART
```

### 1. Backend

1. **Preparar Ambiente**
```bash
# Entre na pasta do backend
cd backend

# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

2. **Instalar Dependências**
```bash
pip install -r requirements.txt
```

3. **Configurar Ambiente**
```bash
# Copie o arquivo de exemplo
copy .env.example .env  # Windows
# ou
cp .env.example .env    # Linux/Mac

# Edite o arquivo .env e adicione sua API_KEY do OpenWeatherMap
# Obtenha sua chave em: https://openweathermap.org/api
```
4. **Iniciar Servidor**
```bash
python app.py
# O servidor estará rodando em http://localhost:5000
```

### 2. Frontend

1. **Instalar Dependências**
```bash
# Entre na pasta do frontend
cd frontend

# Instale as dependências
npm install
```

2. **Iniciar Aplicação**
```bash
npm start
# A aplicação estará disponível em http://localhost:3000
```

### 3. Verificação da Instalação

1. **Verificar Serviços**
- Backend: http://localhost:5000/api/health
- Frontend: http://localhost:3000

2. **Credenciais Padrão**
- Usuário: admin
- Senha: admin123


## 📡 API Endpoints

### Dados Meteorológicos
- `GET /api/weather` - Dados atuais
- `GET /api/history/weather` - Histórico

### Recomendações
- `GET /api/recommendations` - Recomendações de irrigação

### Notificações
- `GET /api/notifications` - Listar notificações
- `DELETE /api/notifications` - Limpar todas
- `DELETE /api/notifications/:id` - Remover específica

## 👥 Equipa
- Guilherme Mota
- Diogo A.
- José Folha

## 📝 Notas
- Backend: http://localhost:5000
- Frontend: http://localhost:3000
- Requer Node.js 16+ e Python 3.10+
- Configure a API key do OpenWeatherMap no `.env`

## 📄 Licença
Este projeto é apenas para fins académicos.

---
Documentação detalhada disponível na pasta `/docs`.