import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from ..utils.logger import setup_logger
from ..storage.data_store import DataStore

load_dotenv()
logger = setup_logger()

class WeatherService:
    def __init__(self, socketio):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.city = "Porto"
        self.country = "PT"
        self.data_store = DataStore()
        self.socketio = socketio  # Salve a instância recebida

    def get_current_weather(self):
        try:
            params = {
                'q': f"{self.city},{self.country}",
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            weather_data = response.json()
            # Tradução manual das descrições meteorológicas mais comuns
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

            simplified_data = {
                'temperature': weather_data['main']['temp'],
                'humidity': weather_data['main']['humidity'],
                'description': description_pt,
                'timestamp': datetime.now().isoformat()
            }
            
            self.data_store.save_weather_data(simplified_data)
            self.socketio.emit('weather_update', simplified_data)
            return simplified_data

        except Exception as e:
            logger.error(f"Error fetching weather data: {str(e)}")
            raise

    def get_weather_history(self):
        return self.data_store.get_weather_history()