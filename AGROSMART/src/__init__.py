"""
Configurações e fixtures comuns para testes do AGROSMART.
"""
import pytest
from pathlib import Path
from typing import Generator, Dict, Any
from unittest.mock import Mock, patch

# Diretórios de teste
TEST_DIR = Path(__file__).parent