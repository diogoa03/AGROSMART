from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from typing import Dict, Any
from src.config.settings import Settings
from src.services.weather_service import WeatherService
from src.services.notificacao import NotificacaoService
from src.middleware.auth import auth_required
from src.utils.logger import Logger
import traceback

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = Settings.SECRET_KEY
logger = Logger(__name__)

weather_service = WeatherService()
notificacao_service = NotificacaoService()

@app.before_request
def before_request() -> None:
    """Middleware para logging de requisições."""
    logger.info(f"Requisição recebida: {request.method} {request.path}")

@app.errorhandler(Exception)
def handle_error(error: Exception) -> Response:
    """Handler global de erros."""
    logger.error(f"Erro: {str(error)}\n{traceback.format_exc()}")
    return jsonify({
        "erro": "Erro interno do servidor",
        "mensagem": str(error)
    }), 500

@app.route('/api/weather')
@auth_required
def weather() -> Response:
    """Endpoint para obter dados meteorológicos."""
    city = request.args.get('city', 'Lisbon')
    data = weather_service.get_weather(city)
    return jsonify(data)

@app.route('/api/notificacoes', methods=['POST'])
@auth_required
def criar_notificacao() -> Response:
    """Endpoint para criar notificação."""
    dados: Dict[str, Any] = request.get_json()
    
    notificacao = notificacao_service.criar(
        titulo=dados['titulo'],
        mensagem=dados['mensagem'],
        tipo=dados['tipo'],
        usuario_id=dados['usuario_id']
    )
    
    if notificacao:
        return jsonify({"mensagem": "Notificação criada com sucesso"}), 201
    return jsonify({"erro": "Erro ao criar notificação"}), 400

if __name__ == '__main__':
    app.run(debug=Settings.DEBUG)