import pytest
from flask import Flask
from unittest.mock import Mock, patch
from app import app

@pytest.fixture
def client():
    """Cliente de teste."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Testa endpoint de health check."""
    response = client.get('/health')
    assert response.status_code == 200