from flask import Flask, jsonify
from src.config.settings import Settings
from src.services.weather_service import WeatherService

app = Flask(__name__)
app.config['SECRET_KEY'] = 'algum_segredo'

@app.route('/')
def home():
    return jsonify({"mensagem": "Bem-vindo ao sistema agrícola inteligente!"})

@app.route('/api/weather')
def weather():
    city = "Lisbon"  # Pode ser dinâmico futuramente
    data = WeatherService.get_weather(city)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)