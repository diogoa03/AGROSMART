import logging
import os
from datetime import datetime

def setup_logger():
    # Cria o diretório de logs se não existir
    os.makedirs('logs', exist_ok=True)
    
    # Cria o logger
    logger = logging.getLogger('agrosmart')
    logger.setLevel(logging.INFO)
    
    # Cria o manipulador de arquivo
    log_file = f'logs/agrosmart_{datetime.now().strftime("%Y%m%d")}.log'
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Cria o manipulador de console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Cria o formatador
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Adiciona os manipuladores ao logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger