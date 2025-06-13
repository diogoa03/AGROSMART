from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
from functools import wraps
from src.services.weather_service import WeatherService
from src.services.recomendacao_service import RecomendacaoService
from src.storage.users import UserStore
from src.utils.logger import setup_logger
import threading
import time

# inicialização da aplicação Flask
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # Configuração do socketio para comunicação em tempo real
logger = setup_logger()

# inicialização dos serviços
weather_service = WeatherService(socketio) 
recomendacao_service = RecomendacaoService()  
user_store = UserStore()  

# decorador para exigir autenticação nas rotas
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not user_store.verify_user(auth.username, auth.password):
            return jsonify({"message": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated

# rota para autenticação de utilizadores
@app.route('/api/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not user_store.verify_user(auth.username, auth.password):
        return jsonify({"message": "Invalid credentials"}), 401
    return jsonify({"message": "Login successful"}), 200

# rota para obter dados meteorológicos atuais
@app.route('/api/weather', methods=['GET'])
@require_auth
def get_weather():
    try:
        weather_data = weather_service.get_current_weather()
        return jsonify(weather_data)
    except Exception as e:
        logger.error(f"Error getting weather data: {str(e)}")
        return jsonify({"error": "Failed to fetch weather data"}), 500

# rota para obter recomendações baseadas no clima atual
@app.route('/api/recommendations', methods=['GET'])
@require_auth
def get_recommendations():
    try:
        weather_data = weather_service.get_current_weather()
        recommendations = recomendacao_service.get_recommendation(weather_data)
        return jsonify(recommendations)
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        return jsonify({"error": "Failed to generate recommendations"}), 500

# rota para obter histórico de dados meteorológicos
@app.route('/api/history/weather', methods=['GET'])
@require_auth
def get_weather_history():
    try:
        history = weather_service.get_weather_history()
        return jsonify(history)
    except Exception as e:
        logger.error(f"Error getting weather history: {str(e)}")
        return jsonify({"error": "Failed to fetch weather history"}), 500
    
# função para atualização periódica dos dados meteorológicos
def background_weather_updates():
    while True:
        weather_data = weather_service.get_current_weather()
        time.sleep(60)

# rota para obter notificações ativas
@app.route('/api/notifications', methods=['GET'])
@require_auth
def get_notifications():
    try:
        severity = request.args.get('severity', None)
        weather_data = weather_service.get_current_weather()
        recomendacao_service.get_recommendation(weather_data)
        notifications = recomendacao_service.notification_service.get_active_notifications(severity)
        return jsonify(notifications)
    except Exception as e:
        logger.error(f"Error getting notifications: {str(e)}")
        return jsonify({"error": "Failed to fetch notifications"}), 500

# rota para limpar todas as notificações
@app.route('/api/notifications', methods=['DELETE'])
@require_auth
def clear_notifications():
    try:
        recomendacao_service.notification_service.clear_notifications()
        return jsonify({"message": "Notifications cleared successfully"})
    except Exception as e:
        logger.error(f"Error clearing notifications: {str(e)}")
        return jsonify({"error": "Failed to clear notifications"}), 500

# rota para apagar uma notificação específica
@app.route('/api/notifications/<notification_id>', methods=['DELETE'])
@require_auth
def delete_notification(notification_id):
    try:
        recomendacao_service.notification_service.delete_notification(notification_id)
        return jsonify({"message": "Notification deleted successfully"})
    except Exception as e:
        logger.error(f"Error deleting notification: {str(e)}")
        return jsonify({"error": "Failed to delete notification"}), 500

# inicia a tarefa de atualização em segundo plano
@app.before_first_request
def start_background_task():
    thread = threading.Thread(target=background_weather_updates)
    thread.daemon = True
    thread.start()

# ponto de entrada do programa
if __name__ == '__main__':
    socketio.run(app, debug=True)