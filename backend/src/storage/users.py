import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from ..utils.logger import setup_logger

# configuração do logger para registo de eventos
logger = setup_logger()

class UserStore:
    def __init__(self):

        # definição do caminho para o ficheiro de utilizadores
        self.users_file = "data/users.json"

        # cria a pasta de dados se não existir
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        
        # inicializa o ficheiro de utilizadores
        self._init_users_file()

    def _init_users_file(self):
         
        # verifica se o ficheiro de utilizadores existe, senão cria-o com um utilizador padrão
         if not os.path.exists(self.users_file):
            default_user = {
                "admin": generate_password_hash("admin123")
            }
            
            # guarda o utilizador padrão no ficheiro
            with open(self.users_file, 'w') as f:
                json.dump(default_user, f, indent=2)

    def verify_user(self, username, password):
        try:

            # abre o ficheiro de utilizadores
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            # verifica se o utilizador existe e se a senha está correta
            if username in users:
                return check_password_hash(users[username], password)
            return False
        
        except Exception as e:

            # regista o erro em caso de falha na verificação
            logger.error(f"Error verifying user: {str(e)}")
            return False