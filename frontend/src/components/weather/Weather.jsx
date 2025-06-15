import React, { useEffect, useState } from 'react';
import { fetchWeather } from '../../services/api';
import socketService from '../../services/socket';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSun, faCloud, faCloudSun, faCloudRain, faCloudShowersHeavy, faBolt, faSnowflake, faSmog, faDroplet, faTemperatureHigh, faCalendarAlt } from '@fortawesome/free-solid-svg-icons';

// Componente que apresenta as condições meteorológicas atuais
const Weather = () => {
    // Estados para gerir os dados meteorológicos, carregamento e erros
    const [weather, setWeather] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [refreshing, setRefreshing] = useState(false);

    // Função para obter os dados meteorológicos da API
    const getWeather = async () => {
        try {
            setRefreshing(true);
            // Obtém o token de autenticação do armazenamento local
            const token = localStorage.getItem('token');
            if (!token) {
                setError('No authentication token found');
                setLoading(false);
                return;
            }

            // Chama a API para obter os dados meteorológicos
            const data = await fetchWeather(token);
            setWeather(data);
            setError(null);
        } catch (err) {
            setError('Failed to fetch weather data');
        } finally {

            // Independentemente do resultado, atualiza os estados de carregamento
            setLoading(false);
            setRefreshing(false);
        }
    };

    useEffect(() => {
        // Carrega os dados meteorológicos quando o componente é montado
        getWeather();

        // Configura o listener para atualizações em tempo real usando o serviço de socket
        const unsubscribe = socketService.on('weather_update', (data) => {
            console.log('Received weather update from server, refreshing weather data...');
            setWeather(data);
        });

        // Limpa o listener quando o componente é desmontado
        return unsubscribe;
    }, []);

    // Função para selecionar o ícone adequado com base na descrição do tempo
    const getWeatherIcon = (description) => {
        const desc = description.toLowerCase();
        
        // Mapeia as descrições meteorológicas para os ícones correspondentes
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
        
        // Ícone predefinido caso não haja correspondência
        return faSun;
    };
    
    // Função para obter a classe CSS com base na temperatura
    const getTemperatureClass = (temperature) => {
        if (temperature >= 35) return 'temp-hot';      
        if (temperature >= 25) return 'temp-warm';  
        if (temperature <= 10) return 'temp-cold';    
        return 'temp-normal';                       
    };
    
    // Função para obter a classe CSS com base na humidade
    const getHumidityClass = (humidity) => {
        if (humidity >= 85) return 'humidity-high';  
        if (humidity <= 60) return 'humidity-low';  
        return 'humidity-normal';                  
    };

    // Mostra indicador de carregamento durante o carregamento inicial
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

    // Mostra mensagem de erro se ocorrer algum problema e não houver dados
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

    // Renderiza o componente com os dados meteorológicos
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