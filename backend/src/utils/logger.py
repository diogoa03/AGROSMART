import logging
import os
from datetime import datetime

def setup_logger():
    
    # cria a pasta de logs se não existir
    os.makedirs('logs', exist_ok=True)
    
    # cria o logger
    logger = logging.getLogger('agrosmart')
    logger.setLevel(logging.INFO)
    
    # cria o manipulador de ficheiros
    log_file = f'logs/agrosmart_{datetime.now().strftime("%Y%m%d")}.log'
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # cria o manipulador de consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # cria o formatador para os logs
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # adiciona os manipuladores ao logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # devolve o logger configurado
    return logger