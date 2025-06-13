import json
import os
from ..utils.logger import setup_logger

logger = setup_logger()

class DataStore:
    def __init__(self):
        self.data_dir = "data"
        self.weather_file = os.path.join(self.data_dir, "weather_data.json")
        os.makedirs(self.data_dir, exist_ok=True)

    def save_weather_data(self, data):
        try:
            history = self.get_weather_history()
            history.append(data)
            
            # Keep only last 24 entries
            if len(history) > 24:
                history = history[-24:]
            
            with open(self.weather_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            logger.info("Weather data saved successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving weather data: {str(e)}")
            return False

    def get_weather_history(self):
        try:
            if not os.path.exists(self.weather_file):
                return []
            
            with open(self.weather_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading weather history: {str(e)}")
            return []