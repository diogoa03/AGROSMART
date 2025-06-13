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
                    <svg className="weather-icon" viewBox="0 0 24 24">
                        <path fill="currentColor" d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96z"/>
                    </svg>
                    <div className="weather-label">Descrição</div>
                    <div className="weather-value">{weather?.description}</div>
                </div>
                <div className="weather-item">
                    <svg className="weather-icon" viewBox="0 0 24 24">
                        <path fill="currentColor" d="M12,3.25C12,3.25 6,10 6,14C6,17.32 8.69,20 12,20A6,6 0 0,0 18,14C18,10 12,3.25 12,3.25M14.47,9.97L15.53,11.03L9.53,17.03L8.47,15.97M9.75,10A1.25,1.25 0 0,1 11,11.25A1.25,1.25 0 0,1 9.75,12.5A1.25,1.25 0 0,1 8.5,11.25A1.25,1.25 0 0,1 9.75,10M14.25,14.5A1.25,1.25 0 0,1 15.5,15.75A1.25,1.25 0 0,1 14.25,17A1.25,1.25 0 0,1 13,15.75A1.25,1.25 0 0,1 14.25,14.5Z"/>
                    </svg>
                    <div className="weather-label">Humidade</div>
                    <div className="weather-value">{weather?.humidity}%</div>
                </div>
                <div className="weather-item">
                    <svg className="weather-icon" viewBox="0 0 24 24">
                        <path fill="currentColor" d="M15,13V5A3,3 0 0,0 12,2A3,3 0 0,0 9,5V13A5,5 0 0,0 4,18A5,5 0 0,0 9,23A5,5 0 0,0 14,18A5,5 0 0,0 9,13C9,13 9,13 9,13V5A3,3 0 0,1 12,8V13H15M12,19A1,1 0 0,1 11,18A1,1 0 0,1 12,17A1,1 0 0,1 13,18A1,1 0 0,1 12,19Z"/>
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