import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from ..utils.logger import setup_logger
from ..storage.data_store import DataStore

# carrega as variáveis de ambiente e configura o logger
load_dotenv()
logger = setup_logger()

class WeatherService:
    def __init__(self, socketio):

        # inicialização com chave API e configurações base
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.city = "Porto"
        self.country = "PT"
        self.data_store = DataStore()
        self.socketio = socketio  # guarda a instância socketio para atualizações em tempo real

    def get_current_weather(self):
        try:
            # prepara os parâmetros para a chamada à API
            params = {
                'q': f"{self.city},{self.country}",
                'appid': self.api_key,
                'units': 'metric'
            }
            # faz a chamada à API do OpenWeather
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            weather_data = response.json()
            
            # dicionário para tradução das descrições meteorológicas de inglês para português
            description_en_pt = {
                'clear sky': 'céu limpo',
                'few clouds': 'poucas nuvens',
                'scattered clouds': 'nuvens dispersas',
                'broken clouds': 'nuvens fragmentadas',
                'shower rain': 'aguaceiros',
                'rain': 'chuva',
                'thunderstorm': 'trovoada',
                'snow': 'neve',
                'mist': 'nevoeiro'
            }
            description_original = weather_data['weather'][0]['description']
            description_pt = description_en_pt.get(description_original.lower(), description_original)

            # simplifica e estrutura os dados meteorológicos relevantes
            simplified_data = {
                'temperature': weather_data['main']['temp'],
                'humidity': weather_data['main']['humidity'],
                'description': description_pt,
                'timestamp': datetime.now().isoformat()
            }
            
            # guarda os dados e emite um evento com as atualizações
            self.data_store.save_weather_data(simplified_data)
            self.socketio.emit('weather_update', simplified_data)
            return simplified_data

        except Exception as e:

            # regista o erro e propaga a exceção
            logger.error(f"Error fetching weather data: {str(e)}")
            raise

    def get_weather_history(self):

        # obtém o histórico de dados meteorológicos do armazenamento
        return self.data_store.get_weather_history()