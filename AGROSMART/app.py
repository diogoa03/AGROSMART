from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from typing import Dict, Any, Optional
from datetime import datetime
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

# Instância dos serviços
weather_service = WeatherService()
notificacao_service = NotificacaoService()

@app.before_request
def before_request() -> None:
    """Middleware para logging de requisições."""
    logger.info(f"Requisição recebida: {request.method} {request.path}")
    logger.info(f"Headers: {dict(request.headers)}")

def validate_request_data(data: Dict[str, Any], required_fields: list) -> Optional[str]:
    """Valida dados da requisição."""
    for field in required_fields:
        if field not in data:
            return f"Campo obrigatório não informado: {field}"
        if not data[field]:
            return f"Campo não pode estar vazio: {field}"
    return None

@app.errorhandler(Exception)
def handle_error(error: Exception) -> Response:
    """
    Handler global de erros.
    
    Args:
        error: Exceção capturada
        
    Returns:
        Response com detalhes do erro
    """
    logger.error(f"Erro: {str(error)}\n{traceback.format_exc()}")
    return jsonify({
        "erro": "Erro interno do servidor",
        "mensagem": str(error),
        "timestamp": datetime.now().isoformat()
    }), 500

@app.route('/api/weather')
@auth_required
def weather() -> Response:
    """
    Endpoint para obter dados meteorológicos.
    
    Query Params:
        city (str): Nome da cidade (default: Lisbon)
        country (str): Código do país (default: PT)
        
    Returns:
        Response com dados meteorológicos
    """
    city = request.args.get('city', 'Lisbon')
    country = request.args.get('country', 'PT')
    
    response = weather_service.get_weather(city, country)
    return jsonify(response.__dict__), response.status

@app.route('/api/notificacoes', methods=['POST'])
@auth_required
def criar_notificacao() -> Response:
    """
    Endpoint para criar notificação.
    
    Body:
        titulo (str): Título da notificação
        mensagem (str): Conteúdo da notificação
        tipo (str): Tipo da notificação (ALERTA, INFO, AVISO)
        usuario_id (int): ID do usuário destinatário
        
    Returns:
        Response com resultado da operação
    """
    dados: Dict[str, Any] = request.get_json()
    
    # Validação dos dados
    erro = validate_request_data(
        dados, 
        ['titulo', 'mensagem', 'tipo', 'usuario_id']
    )
    if erro:
        return jsonify({"erro": erro}), 400
    
    response = notificacao_service.criar(
        titulo=dados['titulo'],
        mensagem=dados['mensagem'],
        tipo=dados['tipo'],
        usuario_id=dados['usuario_id']
    )
    
    return jsonify(response.__dict__), response.status

@app.route('/api/notificacoes/<int:usuario_id>', methods=['GET'])
@auth_required
def listar_notificacoes(usuario_id: int) -> Response:
    """
    Lista notificações de um usuário.
    
    Path Params:
        usuario_id (int): ID do usuário
        
    Returns:
        Response com lista de notificações
    """
    response = notificacao_service.listar_por_usuario(usuario_id)
    return jsonify(response.__dict__), response.status

@app.route('/api/notificacoes/<int:notificacao_id>/lida', methods=['PUT'])
@auth_required
def marcar_como_lida(notificacao_id: int) -> Response:
    """
    Marca notificação como lida.
    
    Path Params:
        notificacao_id (int): ID da notificação
        
    Returns:
        Response com resultado da operação
    """
    response = notificacao_service.marcar_como_lida(notificacao_id)
    return jsonify(response.__dict__), response.status

if __name__ == '__main__':
    app.run(
        host=Settings.HOST,
        port=Settings.PORT,
        debug=Settings.DEBUG
    )