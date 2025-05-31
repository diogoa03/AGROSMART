"""
Módulo de modelos de dados para o sistema de gestão agrícola.

Este módulo contém as classes que representam e processam
os dados meteorológicos utilizados no sistema.
"""

from .weather import WeatherData, WeatherForecast

__all__ = ['WeatherData', 'WeatherForecast']
