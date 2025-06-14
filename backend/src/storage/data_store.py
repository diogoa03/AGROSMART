import json
import os
from ..utils.logger import setup_logger

# Configuração do sistema de registo
logger = setup_logger()

class DataStore:
    def __init__(self):

        # definição da pasta e ficheiro para armazenamento de dados
        self.data_dir = "data"
        self.weather_file = os.path.join(str(self.data_dir), "weather_data.json")

        # cria a pasta de dados se não existir
        os.makedirs(self.data_dir, exist_ok=True)

    def save_weather_data(self, data):
        try:

            # obtém o histórico atual de dados meteorológicos
            history = self.get_weather_history()

            # adiciona os novos dados ao histórico
            history.append(data)
            
            # mantém apenas as últimas 24 entradas (1 dia)
            if len(history) > 24:
                history = history[-24:]
            
            # guarda os dados atualizados no ficheiro
            with open(self.weather_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            # regista o sucesso da operação
            logger.info("Weather data saved successfully")
            return True
        
        except Exception as e:

            # regista o erro em caso de falha
            logger.error(f"Error saving weather data: {str(e)}")
            return False

    def get_weather_history(self):
        try:

            # verifica se o ficheiro de histórico existe
            if not os.path.exists(self.weather_file):
                return []
            
            # lê e devolve os dados do ficheiro
            with open(self.weather_file, 'r') as f:
                return json.load(f)
        except Exception as e:

            # Regista o erro em caso de falha na leitura
            logger.error(f"Error reading weather history: {str(e)}")
            return []