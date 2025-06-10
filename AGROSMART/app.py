from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
from src.config.settings import settings  # Changed from Settings to settings
from src.services.weather_service import WeatherService
from src.services.notificacao_service import NotificacaoService
from src.middleware.auth import auth_required
from src.utils.logger import Logger
import traceback

# Inicialização do app
app = Flask(__name__)
CORS(app)

# Configurações do Flask
app.config['SECRET_KEY'] = settings.SECRET_KEY  # Using settings instance
logger = Logger(__name__)

# Instância dos serviços
weather_service = WeatherService()
notificacao_service = NotificacaoService()

def create_error_response(error: str, status_code: int = 400) -> Tuple[Dict, int]:
    """
    Cria resposta de erro padronizada.
    
    Args:
        error: Mensagem de erro
        status_code: Código HTTP (default: 400)
        
    Returns:
        Tuple com dicionário de erro e status code
    """
    return {
        "erro": error,
        "timestamp": datetime.now().isoformat()
    }, status_code

@app.before_request
def before_request() -> None:
    """Middleware para logging de requisições."""
    logger.info(
        "Requisição recebida",
        extra={
            "method": request.method,
            "path": request.path,
            "headers": dict(request.headers)
        }
    )

def validate_request_data(data: Dict[str, Any], required_fields: list) -> Optional[str]:
    """
    Valida dados da requisição.
    
    Args:
        data: Dados da requisição
        required_fields: Lista de campos obrigatórios
        
    Returns:
        Mensagem de erro ou None se válido
    """
    if not data:
        return "Corpo da requisição vazio"
        
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
    logger.error(
        "Erro não tratado",
        extra={
            "error": str(error),
            "traceback": traceback.format_exc()
        }
    )
    response, status = create_error_response(
        "Erro interno do servidor",
        500
    )
    return jsonify(response), status

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
    dados = request.get_json()
    
    erro = validate_request_data(
        dados, 
        ['titulo', 'mensagem', 'tipo', 'usuario_id']
    )
    if erro:
        response, status = create_error_response(erro)
        return jsonify(response), status
    
    response = notificacao_service.criar(**dados)
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
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    response = notificacao_service.listar_por_usuario(
        usuario_id,
        page=page,
        per_page=per_page
    )
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
        host=settings.HOST,  # Changed from Settings.HOST
        port=settings.PORT,  # Changed from Settings.PORT  
        debug=settings.DEBUG  # Changed from Settings.DEBUG
    )