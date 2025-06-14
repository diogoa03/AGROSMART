import React, { useEffect, useState } from 'react';
import { fetchWeather } from '../services/api';
import { WeatherData } from '../types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSun, faCloud, faCloudSun, faCloudRain, faCloudShowersHeavy, faBolt, faSnowflake, faSmog, faDroplet, faTemperatureHigh, faCalendarAlt
} from '@fortawesome/free-solid-svg-icons';

const Weather: React.FC = () => {
    const [weather, setWeather] = useState<WeatherData | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const [refreshing, setRefreshing] = useState<boolean>(false);

    const getWeather = async () => {
        try {
            setRefreshing(true);
            const token = localStorage.getItem('token');
            if (!token) {
                setError('No authentication token found');
                setLoading(false);
                return;
            }
            const data = await fetchWeather(token);
            setWeather(data);
            setError(null);
        } catch (err) {
            setError('Failed to fetch weather data');
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    };

    useEffect(() => {
        // Carrega os dados apenas uma vez ao montar o componente
        getWeather();
    }, []);

    // Função para selecionar o ícone com base na descrição do tempo
    // Atualizada para corresponder exatamente às descrições usadas no backend
    const getWeatherIcon = (description: string) => {
        const desc = description.toLowerCase();
        
        if (desc === 'céu limpo') return faSun;
        if (desc === 'poucas nuvens') return faCloudSun;
        if (desc === 'nuvens dispersas') return faCloud;
        if (desc === 'nuvens fragmentadas') return faCloud;
        if (desc === 'chuva fraca') return faCloudRain;
        if (desc === 'aguaceiros') return faCloudShowersHeavy;
        if (desc === 'chuva') return faCloudRain;
        if (desc === 'trovoada') return faBolt;
        if (desc === 'neve') return faSnowflake;
        if (desc === 'nevoeiro') return faSmog;
        
        // Ícone padrão caso não haja correspondência
        return faSun;
    };
    

    const getTemperatureClass = (temperature: number) => {
        if (temperature >= 35) return 'temp-hot';      
        if (temperature >= 25) return 'temp-warm';    
        if (temperature <= 10) return 'temp-cold';     
        return 'temp-normal';
    };
    
    // Função para obter a classe de cor com base na humidade
    const getHumidityClass = (humidity: number) => {
        if (humidity >= 85) return 'humidity-high';    
        if (humidity <= 60) return 'humidity-low';     
        return 'humidity-normal';
    };

    if (loading && !refreshing) {
        return (
            <div className="card-container weather-card">
                <div className="weather-loading">
                    <div className="loading-spinner"></div>
                    <p>A carregar dados meteorológicos...</p>
                </div>
            </div>
        );
    }

    if (error && !weather) {
        return (
            <div className="card-container weather-card">
                <div className="weather-error">
                    <p>{error}</p>
                    <button onClick={getWeather} className="refresh-button">
                        Tentar Novamente
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="card-container weather-card">
            <h2 className="card-header">Condições Meteorológicas</h2>
            
            {refreshing && (
                <div className="refreshing-indicator">
                    <div className="loading-spinner-small"></div>
                    <span>A atualizar...</span>
                </div>
            )}
            
            <div className="weather-main">
                <div className="weather-icon-large">
                    <FontAwesomeIcon 
                        icon={weather ? getWeatherIcon(weather.description) : faSun} 
                        className="weather-condition-icon"
                    />
                    <div className="weather-description">{weather?.description}</div>
                </div>
                
                <div className="weather-metrics">
                    <div className={`weather-item ${weather ? getTemperatureClass(weather.temperature) : ''}`}>
                        <FontAwesomeIcon icon={faTemperatureHigh} className="weather-metric-icon" />
                        <div className="weather-label">Temperatura</div>
                        <div className="weather-value">{weather?.temperature?.toFixed(1)}°C</div>
                    </div>
                    
                    <div className={`weather-item ${weather ? getHumidityClass(weather.humidity) : ''}`}>
                        <FontAwesomeIcon icon={faDroplet} className="weather-metric-icon" />
                        <div className="weather-label">Humidade</div>
                        <div className="weather-value">{weather?.humidity}%</div>
                    </div>
                </div>
            </div>
            
            <div className="weather-footer">
                <div className="weather-timestamp">
                    <FontAwesomeIcon icon={faCalendarAlt} />
                    <span>Atualizado: {weather ? new Date(weather.timestamp).toLocaleString("pt-PT") : ''}</span>
                </div>
            </div>
        </div>
    );
};

export default Weather;