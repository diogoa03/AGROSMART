from functools import wraps
from flask import request, jsonify
from datetime import datetime
from typing import Callable, Any
from src.config.settings import Settings
from src.utils.logger import Logger

logger = Logger(__name__)

def auth_required(f: Callable) -> Callable:
    """
    Decorador para proteger rotas que necessitam autenticação.
    
    Args:
        f: Função/rota a ser decorada
        
    Returns:
        Função decorada que valida token JWT
    """
    @wraps(f)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        # Obtém token do header Authorization
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            logger.warning("Token não fornecido")
            return jsonify({
                "erro": "Token não fornecido",
                "timestamp": datetime.now().isoformat()
            }), 401
            
        try:
            # Remove prefixo 'Bearer ' se presente
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
            else:
                token = auth_header
                
            # TODO: Implementar validação do token JWT
            # Por enquanto aceita qualquer token não vazio
            if not token:
                raise ValueError("Token inválido")
                
            # Adiciona informações do usuário ao contexto da request
            # TODO: Decodificar token e extrair dados do usuário
            request.user = {
                "id": 1,  # Placeholder
                "role": "user"  # Placeholder
            }
            
            return f(*args, **kwargs)
            
        except Exception as e:
            logger.error(
                "Erro na autenticação",
                extra={
                    "error": str(e),
                    "token": auth_header
                }
            )
            return jsonify({
                "erro": "Token inválido ou expirado",
                "timestamp": datetime.now().isoformat()
            }), 401
            
    return decorated