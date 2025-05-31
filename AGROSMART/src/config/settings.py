import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
    DEBUG = os.getenv("DEBUG", "True") == "True"
    PORT = int(os.getenv("PORT", 5000))
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")