from flask import Flask, jsonify, request
from flask_cors import CORS
from functools import wraps
from src.services.weather_service import WeatherService
from src.services.recomendacao_service import RecomendacaoService
from src.storage.users import UserStore
from src.utils.logger import setup_logger

app = Flask(__name__)
CORS(app)
logger = setup_logger()

weather_service = WeatherService()
recomendacao_service = RecomendacaoService()
user_store = UserStore()

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not user_store.verify_user(auth.username, auth.password):
            return jsonify({"message": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/api/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not user_store.verify_user(auth.username, auth.password):
        return jsonify({"message": "Invalid credentials"}), 401
    return jsonify({"message": "Login successful"}), 200

@app.route('/api/weather', methods=['GET'])
@require_auth
def get_weather():
    try:
        weather_data = weather_service.get_current_weather()
        return jsonify(weather_data)
    except Exception as e:
        logger.error(f"Error getting weather data: {str(e)}")
        return jsonify({"error": "Failed to fetch weather data"}), 500

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

@app.route('/api/history/weather', methods=['GET'])
@require_auth
def get_weather_history():
    try:
        history = weather_service.get_weather_history()
        return jsonify(history)
    except Exception as e:
        logger.error(f"Error getting weather history: {str(e)}")
        return jsonify({"error": "Failed to fetch weather history"}), 500

@app.route('/api/notifications', methods=['GET'])
@require_auth
def get_notifications():
    try:
        severity = request.args.get('severity', None)
        notifications = recomendacao_service.notification_service.get_active_notifications(severity)
        return jsonify(notifications)
    except Exception as e:
        logger.error(f"Error getting notifications: {str(e)}")
        return jsonify({"error": "Failed to fetch notifications"}), 500

@app.route('/api/notifications', methods=['DELETE'])
@require_auth
def clear_notifications():
    try:
        recomendacao_service.notification_service.clear_notifications()
        return jsonify({"message": "Notifications cleared successfully"})
    except Exception as e:
        logger.error(f"Error clearing notifications: {str(e)}")
        return jsonify({"error": "Failed to clear notifications"}), 500

if __name__ == '__main__':
    app.run(debug=True)