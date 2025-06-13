import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from ..utils.logger import setup_logger

logger = setup_logger()

class UserStore:
    def __init__(self):
        self.users_file = "data/users.json"
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        self._init_users_file()

    def _init_users_file(self):
        if not os.path.exists(self.users_file):
            default_user = {
                "admin": generate_password_hash("admin123")  # Default credentials
            }
            with open(self.users_file, 'w') as f:
                json.dump(default_user, f, indent=2)

    def verify_user(self, username, password):
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            if username in users:
                return check_password_hash(users[username], password)
            return False
        except Exception as e:
            logger.error(f"Error verifying user: {str(e)}")
            return False