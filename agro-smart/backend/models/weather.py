"""
Modelo de dados meteorológicos para o sistema de gestão agrícola.

Este módulo define as classes que representam os dados meteorológicos
obtidos da API OpenWeatherMap, incluindo validação e formatação.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any


class WeatherData:
    """
    Classe que representa os dados meteorológicos atuais.
    
    Armazena informações como temperatura, humidade, precipitação
    e outras métricas relevantes para decisões agrícolas.
    """
    
    def __init__(self, raw_data: Dict[str, Any]):
        """
        Inicializa os dados meteorológicos.
        
        Args:
            raw_data: Dados brutos da API OpenWeatherMap
        """
        self.raw_data = raw_data
        self.timestamp = datetime.now()
        
        # Extrai dados principais
        self.temperature = self._extract_temperature()
        self.humidity = self._extract_humidity()
        self.pressure = self._extract_pressure()
        self.wind_speed = self._extract_wind_speed()
        self.wind_direction = self._extract_wind_direction()
        self.cloudiness = self._extract_cloudiness()
        self.visibility = self._extract_visibility()
        self.weather_condition = self._extract_weather_condition()
        self.weather_description = self._extract_weather_description()
        
        # Dados de localização
        self.city_name = raw_data.get('name', 'Desconhecida')
        self.country = raw_data.get('sys', {}).get('country', '')
        self.coordinates = self._extract_coordinates()
        
        # Dados de precipitação
        self.rain_1h = self._extract_rain_1h()
        self.rain_3h = self._extract_rain_3h()
        self.snow_1h = self._extract_snow_1h()
        self.snow_3h = self._extract_snow_3h()
    
    def _extract_temperature(self) -> Dict[str, float]:
        """Extrai dados de temperatura em Celsius."""
        main = self.raw_data.get('main', {})
        return {
            'current': round(main.get('temp', 0) - 273.15, 1),  # Kelvin para Celsius
            'feels_like': round(main.get('feels_like', 0) - 273.15, 1),
            'min': round(main.get('temp_min', 0) - 273.15, 1),
            'max': round(main.get('temp_max', 0) - 273.15, 1)
        }
    
    def _extract_humidity(self) -> float:
        """Extrai humidade relativa em percentagem."""
        return self.raw_data.get('main', {}).get('humidity', 0)
    
    def _extract_pressure(self) -> Dict[str, float]:
        """Extrai dados de pressão atmosférica."""
        main = self.raw_data.get('main', {})
        return {
            'sea_level': main.get('pressure', 0),
            'ground_level': main.get('grnd_level', main.get('pressure', 0))
        }
    
    def _extract_wind_speed(self) -> float:
        """Extrai velocidade do vento em m/s."""
        return self.raw_data.get('wind', {}).get('speed', 0)
    
    def _extract_wind_direction(self) -> float:
        """Extrai direção do vento em graus."""
        return self.raw_data.get('wind', {}).get('deg', 0)
    
    def _extract_cloudiness(self) -> float:
        """Extrai percentagem de nebulosidade."""
        return self.raw_data.get('clouds', {}).get('all', 0)
    
    def _extract_visibility(self) -> float:
        """Extrai visibilidade em metros."""
        return self.raw_data.get('visibility', 0)
    
    def _extract_weather_condition(self) -> str:
        """Extrai condição meteorológica principal."""
        weather = self.raw_data.get('weather', [{}])
        return weather[0].get('main', 'Unknown') if weather else 'Unknown'
    
    def _extract_weather_description(self) -> str:
        """Extrai descrição detalhada do tempo."""
        weather = self.raw_data.get('weather', [{}])
        return weather[0].get('description', 'Sem descrição') if weather else 'Sem descrição'
    
    def _extract_coordinates(self) -> Dict[str, float]:
        """Extrai coordenadas geográficas."""
        coord = self.raw_data.get('coord', {})
        return {
            'latitude': coord.get('lat', 0),
            'longitude': coord.get('lon', 0)
        }
    
    def _extract_rain_1h(self) -> float:
        """Extrai precipitação de chuva na última hora (mm)."""
        return self.raw_data.get('rain', {}).get('1h', 0)
    
    def _extract_rain_3h(self) -> float:
        """Extrai precipitação de chuva nas últimas 3 horas (mm)."""
        return self.raw_data.get('rain', {}).get('3h', 0)
    
    def _extract_snow_1h(self) -> float:
        """Extrai precipitação de neve na última hora (mm)."""
        return self.raw_data.get('snow', {}).get('1h', 0)
    
    def _extract_snow_3h(self) -> float:
        """Extrai precipitação de neve nas últimas 3 horas (mm)."""
        return self.raw_data.get('snow', {}).get('3h', 0)
    
    def is_raining(self) -> bool:
        """Verifica se está a chover atualmente."""
        return self.rain_1h > 0 or 'rain' in self.weather_condition.lower()
    
    def is_sunny(self) -> bool:
        """Verifica se está sol."""
        return self.weather_condition.lower() in ['clear', 'sunny']
    
    def is_cloudy(self) -> bool:
        """Verifica se está nublado."""
        return self.cloudiness > 50
    
    def get_comfort_index(self) -> str:
        """
        Calcula índice de conforto baseado em temperatura e humidade.
        
        Returns:
            str: 'Confortável', 'Quente', 'Frio', 'Húmido', etc.
        """
        temp = self.temperature['current']
        humidity = self.humidity
        
        if temp < 10:
            return 'Muito Frio'
        elif temp < 15:
            return 'Frio'
        elif temp > 30:
            return 'Muito Quente'
        elif temp > 25:
            return 'Quente'
        elif humidity > 80:
            return 'Muito Húmido'
        elif humidity < 40:
            return 'Seco'
        else:
            return 'Confortável'
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte os dados meteorológicos para dicionário.
        
        Returns:
            Dict: Dados formatados para JSON/API
        """
        return {
            'timestamp': self.timestamp.isoformat(),
            'location': {
                'city': self.city_name,
                'country': self.country,
                'coordinates': self.coordinates
            },
            'temperature': self.temperature,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'wind': {
                'speed': self.wind_speed,
                'direction': self.wind_direction
            },
            'precipitation': {
                'rain_1h': self.rain_1h,
                'rain_3h': self.rain_3h,
                'snow_1h': self.snow_1h,
                'snow_3h': self.snow_3h,
                'is_raining': self.is_raining()
            },
            'atmosphere': {
                'cloudiness': self.cloudiness,
                'visibility': self.visibility,
                'comfort_index': self.get_comfort_index()
            },
            'weather': {
                'condition': self.weather_condition,
                'description': self.weather_description,
                'is_sunny': self.is_sunny(),
                'is_cloudy': self.is_cloudy()
            }
        }
    
    def __str__(self) -> str:
        """Representação em string dos dados meteorológicos."""
        return (f"WeatherData({self.city_name}: {self.temperature['current']}°C, "
                f"{self.humidity}% humidade, {self.weather_description})")


class WeatherForecast:
    """
    Classe que representa previsões meteorológicas.
    
    Armazena dados de previsão para os próximos dias,
    essencial para planeamento agrícola.
    """
    
    def __init__(self, raw_forecast_data: Dict[str, Any]):
        """
        Inicializa dados de previsão meteorológica.
        
        Args:
            raw_forecast_data: Dados brutos da API de previsão
        """
        self.raw_data = raw_forecast_data
        self.forecasts = self._parse_forecasts()
        self.city_name = raw_forecast_data.get('city', {}).get('name', 'Desconhecida')
    
    def _parse_forecasts(self) -> List[Dict[str, Any]]:
        """Processa lista de previsões."""
        forecasts = []
        forecast_list = self.raw_data.get('list', [])
        
        for forecast in forecast_list:
            parsed_forecast = {
                'datetime': datetime.fromtimestamp(forecast.get('dt', 0)),
                'temperature': {
                    'current': round(forecast.get('main', {}).get('temp', 0) - 273.15, 1),
                    'min': round(forecast.get('main', {}).get('temp_min', 0) - 273.15, 1),
                    'max': round(forecast.get('main', {}).get('temp_max', 0) - 273.15, 1)
                },
                'humidity': forecast.get('main', {}).get('humidity', 0),
                'rain_probability': forecast.get('pop', 0) * 100,  # Probabilidade de chuva
                'rain_volume': forecast.get('rain', {}).get('3h', 0),
                'weather_condition': forecast.get('weather', [{}])[0].get('main', 'Unknown'),
                'weather_description': forecast.get('weather', [{}])[0].get('description', ''),
                'wind_speed': forecast.get('wind', {}).get('speed', 0),
                'cloudiness': forecast.get('clouds', {}).get('all', 0)
            }
            forecasts.append(parsed_forecast)
        
        return forecasts
    
    def get_daily_summary(self) -> List[Dict[str, Any]]:
        """
        Agrupa previsões por dia.
        
        Returns:
            List: Resumo diário das previsões
        """
        daily_data = {}
        
        for forecast in self.forecasts:
            date_key = forecast['datetime'].date()
            
            if date_key not in daily_data:
                daily_data[date_key] = {
                    'date': date_key,
                    'temp_min': forecast['temperature']['min'],
                    'temp_max': forecast['temperature']['max'],
                    'humidity_avg': [],
                    'rain_total': 0,
                    'rain_probability_max': 0,
                    'conditions': []
                }
            
            day_data = daily_data[date_key]
            day_data['temp_min'] = min(day_data['temp_min'], forecast['temperature']['min'])
            day_data['temp_max'] = max(day_data['temp_max'], forecast['temperature']['max'])
            day_data['humidity_avg'].append(forecast['humidity'])
            day_data['rain_total'] += forecast['rain_volume']
            day_data['rain_probability_max'] = max(day_data['rain_probability_max'], 
                                                 forecast['rain_probability'])
            day_data['conditions'].append(forecast['weather_condition'])
        
        # Processa médias e condições mais frequentes
        for day_data in daily_data.values():
            day_data['humidity_avg'] = round(sum(day_data['humidity_avg']) / 
                                           len(day_data['humidity_avg']), 1)
            # Condição mais frequente do dia
            day_data['main_condition'] = max(set(day_data['conditions']), 
                                           key=day_data['conditions'].count)
        
        return list(daily_data.values())
    
    def will_rain_next_24h(self) -> Dict[str, Any]:
        """
        Verifica se vai chover nas próximas 24 horas.
        
        Returns:
            Dict: Informações sobre chuva prevista
        """
        next_24h = [f for f in self.forecasts 
                   if f['datetime'] <= datetime.now().replace(hour=23, minute=59) 
                   and f['datetime'] >= datetime.now()]
        
        if not next_24h:
            return {'will_rain': False, 'probability': 0, 'volume': 0}
        
        max_probability = max(f['rain_probability'] for f in next_24h)
        total_volume = sum(f['rain_volume'] for f in next_24h)
        
        return {
            'will_rain': max_probability > 30,  # 30% threshold
            'probability': max_probability,
            'volume': total_volume,
            'hours_until_rain': self._hours_until_rain(next_24h)
        }
    
    def _hours_until_rain(self, forecasts: List[Dict]) -> Optional[int]:
        """Calcula horas até próxima chuva significativa."""
        now = datetime.now()
        for forecast in forecasts:
            if forecast['rain_probability'] > 50:
                delta = forecast['datetime'] - now
                return int(delta.total_seconds() / 3600)
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte previsão para dicionário."""
        return {
            'city': self.city_name,
            'daily_summary': self.get_daily_summary(),
            'rain_forecast_24h': self.will_rain_next_24h(),
            'detailed_forecasts': [
                {
                    **forecast,
                    'datetime': forecast['datetime'].isoformat()
                }
                for forecast in self.forecasts[:8]  # Próximas 24h (intervalos de 3h)
            ]
        }