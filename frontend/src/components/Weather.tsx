import React, { useEffect, useState } from 'react';
import { fetchWeather } from '../services/api';
import { WeatherData } from '../types';

const Weather: React.FC = () => {
    const [weather, setWeather] = useState<WeatherData | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const getWeather = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    setError('No authentication token found');
                    setLoading(false);
                    return;
                }
                const data = await fetchWeather(token);
                setWeather(data);
            } catch (err) {
                setError('Failed to fetch weather data');
            } finally {
                setLoading(false);
            }
        };

        getWeather();
    }, []);

    if (loading) {
        return <div className="card-container">Loading...</div>;
    }

    if (error) {
        return <div className="card-container">{error}</div>;
    }

    return (
        <div className="card-container">
            <h2 className="card-header">Condições Meteorológicas</h2>
            <div className="weather-display">
                <div className="weather-item">
                    {/* Ícone de sol para descrição */}
                    <svg className="weather-icon" viewBox="0 0 24 24">
                        <circle cx="12" cy="12" r="5" fill="#FFD600"/>
                        <g stroke="#FFD600" strokeWidth="2">
                            <line x1="12" y1="1" x2="12" y2="4"/>
                            <line x1="12" y1="20" x2="12" y2="23"/>
                            <line x1="1" y1="12" x2="4" y2="12"/>
                            <line x1="20" y1="12" x2="23" y2="12"/>
                            <line x1="4.22" y1="4.22" x2="6.34" y2="6.34"/>
                            <line x1="17.66" y1="17.66" x2="19.78" y2="19.78"/>
                            <line x1="4.22" y1="19.78" x2="6.34" y2="17.66"/>
                            <line x1="17.66" y1="6.34" x2="19.78" y2="4.22"/>
                        </g>
                    </svg>
                    <div className="weather-label">Descrição</div>
                    <div className="weather-value">{weather?.description}</div>
                </div>
                <div className="weather-item">
            
                    <svg className="weather-icon" viewBox="0 0 24 24">
                        <path fill="#2196F3" d="M12 2C12 2 5 10 5 15a7 7 0 0 0 14 0C19 10 12 2 12 2zm0 18a5 5 0 0 1-5-5c0-3.07 3.58-7.36 5-9.06C13.42 7.64 17 11.93 17 15a5 5 0 0 1-5 5z"/>
                    </svg>
                    <div className="weather-label">Humidade</div>
                    <div className="weather-value">{weather?.humidity}%</div>
                </div>
                <div className="weather-item">
                    <svg className="weather-icon" viewBox="0 0 24 24">
                        <path fill="#F44336" d="M17 17.5a5 5 0 1 1-10 0c0-2.54 1.92-4.64 4.38-4.96V5a1.62 1.62 0 1 1 3.24 0v7.54A5.01 5.01 0 0 1 17 17.5zm-5 3a3 3 0 0 0 3-3c0-1.31-.84-2.42-2-2.83V5a1 1 0 1 0-2 0v9.67c-1.16.41-2 1.52-2 2.83a3 3 0 0 0 3 3z"/>
                    </svg>
                    <div className="weather-label">Temperatura</div>
                    <div className="weather-value">{weather?.temperature}°C</div>
                </div>
            </div>
            <div className="weather-timestamp">
                <svg width="24" height="24" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M19,19H5V8H19M16,1V3H8V1H6V3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.89 20.1,3 19,3H18V1M17,12H12V17H17V12Z"/>
                </svg>
                <span>{new Date(weather?.timestamp || "").toLocaleString("pt-pt")}</span>
            </div>
        </div>
    );
};

export default Weather;