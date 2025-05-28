#!/usr/bin/env python3
'''
Arquivo principal de execução do Sistema de Agricultura Inteligente
'''

import os
import sys
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def main():
    '''Função principal'''
    print("Sistema de Agricultura Inteligente")
    print("Para executar, configure primeiro as dependências:")
    print("1. pip install -r requirements.txt")
    print("2. Configure o arquivo .env")
    print("3. python scripts/setup_database.py")
    
if __name__ == "__main__":
    main()
