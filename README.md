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

### 1. Backend

1. **Preparar Ambiente**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

2. **Instalar Dependências**
```bash
pip install -r requirements.txt
```

3. **Configurar Ambiente**
```bash
copy .env.example .env
# Adicione sua API_KEY do OpenWeatherMap no .env
```

4. **Iniciar Servidor**
```bash
python app.py
```

### 2. Frontend

1. **Instalar Dependências**
```bash
cd frontend
npm install
```

2. **Iniciar Aplicação**
```bash
npm start
```

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