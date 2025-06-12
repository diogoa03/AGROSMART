import unittest
import os
import json
from src.storage.users import UserStore
from werkzeug.security import generate_password_hash

class TestUserAuthentication(unittest.TestCase):
    def setUp(self):
        # Usar um arquivo de usuários específico para testes
        self.test_users_file = "data/test_users.json"
        self.user_store = UserStore()
        self.user_store.users_file = self.test_users_file
        
        # Criar dados de usuário de teste
        test_users = {
            "testuser": generate_password_hash("testpass123"),
            "admin": generate_password_hash("admin123")
        }
        os.makedirs(os.path.dirname(self.test_users_file), exist_ok=True)
        with open(self.test_users_file, 'w') as f:
            json.dump(test_users, f)

    def tearDown(self):
        # Limpar o arquivo de teste após os testes
        if os.path.exists(self.test_users_file):
            os.remove(self.test_users_file)

    def test_valid_user_login(self):
        """Test login with valid credentials"""
        self.assertTrue(self.user_store.verify_user("testuser", "testpass123"))
        self.assertTrue(self.user_store.verify_user("admin", "admin123"))

    def test_invalid_password(self):
        """Test login with invalid password"""
        self.assertFalse(self.user_store.verify_user("testuser", "wrongpass"))

    def test_nonexistent_user(self):
        """Test login with non-existent user"""
        self.assertFalse(self.user_store.verify_user("nonexistent", "anypass"))

    def test_empty_credentials(self):
        """Test login with empty credentials"""
        self.assertFalse(self.user_store.verify_user("", ""))
        self.assertFalse(self.user_store.verify_user("testuser", ""))
        self.assertFalse(self.user_store.verify_user("", "testpass123"))

    def test_file_corruption(self):
        """Test behavior when users file is corrupted"""
        # Corrompe o arquivo com JSON inválido
        with open(self.test_users_file, 'w') as f:
            f.write("invalid json content")
        
        self.assertFalse(self.user_store.verify_user("testuser", "testpass123"))

if __name__ == '__main__':
    unittest.main()