import React, { useEffect, useState } from 'react';
import { fetchHistory } from '../services/api';
import { WeatherData } from '../types';
import io from 'socket.io-client';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSun, faCloud, faCloudSun, faCloudRain, faCloudShowersHeavy, faBolt, faSnowflake, faSmog, faHistory,faCalendarAlt,faTemperatureHigh,faDroplet
} from '@fortawesome/free-solid-svg-icons';

const History: React.FC = () => {
    const [history, setHistory] = useState<WeatherData[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const getHistoryData = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    setError('No authentication token found');
                    setLoading(false);
                    return;
                }
                const data = await fetchHistory(token);
                setHistory(data);
            } catch (err) {
                setError('Failed to fetch history data');
            } finally {
                setLoading(false);
            }
        };

        getHistoryData();

        const socket = io('http://localhost:5000'); 
        
        socket.on('weather_update', () => {
            console.log('Received weather update from server, refreshing history...');
            getHistoryData();
        });

        return () => {
            socket.disconnect();
        };
    }, []);

    // Função para selecionar o ícone com base na descrição do tempo
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
    
    // Função para obter a classe de cor com base na temperatura
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

    if (loading) {
        return (
            <div className="card-container history-card">
                <div className="history-loading">
                    <div className="loading-spinner"></div>
                    <p>A carregar histórico meteorológico...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="card-container history-card">
                <div className="history-error">
                    <p>{error}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="card-container history-card">
            <h2 className="card-header">
                <FontAwesomeIcon icon={faHistory} className="header-icon" />
                Histórico Meteorológico
            </h2>
            
            {history.length === 0 ? (
                <div className="empty-history">
                    <p>Sem dados históricos disponíveis</p>
                </div>
            ) : (
                <div className="history-table-container">
                    <table className="history-table">
                        <thead>
                            <tr>
                                <th>Condição</th>
                                <th>
                                    <FontAwesomeIcon icon={faTemperatureHigh} /> Temperatura
                                </th>
                                <th>
                                    <FontAwesomeIcon icon={faDroplet} /> Humidade
                                </th>
                                <th>
                                    <FontAwesomeIcon icon={faCalendarAlt} /> Data/Hora
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            {history.map((entry, index) => (
                                <tr key={index}>
                                    <td className="weather-icon-cell">
                                        <FontAwesomeIcon 
                                            icon={getWeatherIcon(entry.description)} 
                                            className={`weather-history-icon ${getTemperatureClass(entry.temperature)}`} 
                                        />
                                        <span>{entry.description}</span>
                                    </td>
                                    <td className={getTemperatureClass(entry.temperature)}>
                                        {entry.temperature.toFixed(1)}°C
                                    </td>
                                    <td className={getHumidityClass(entry.humidity)}>
                                        {entry.humidity}%
                                    </td>
                                    <td>
                                        {new Date(entry.timestamp).toLocaleString('pt-PT')}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default History;