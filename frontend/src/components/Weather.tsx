import React, { useEffect, useState } from 'react';
import { fetchWeather } from '../services/api';
import { WeatherData } from '../types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSun, faDroplet, faTemperatureHigh, faCalendarAlt } from '@fortawesome/free-solid-svg-icons';

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
                    <FontAwesomeIcon icon={faSun} className="weather-icon" />
                    <div className="weather-label">Descrição</div>
                    <div className="weather-value">{weather?.description}</div>
                </div>
                <div className="weather-item">
                    <FontAwesomeIcon icon={faDroplet} className="weather-icon" />
                    <div className="weather-label">Humidade</div>
                    <div className="weather-value">{weather?.humidity}%</div>
                </div>
                <div className="weather-item">
                    <FontAwesomeIcon icon={faTemperatureHigh} className="weather-icon" />
                    <div className="weather-label">Temperatura</div>
                    <div className="weather-value">{weather?.temperature}°C</div>
                </div>
            </div>
            <div className="weather-timestamp">
                <FontAwesomeIcon icon={faCalendarAlt} />
                <span>{new Date(weather?.timestamp || "").toLocaleString("pt-pt")}</span>
            </div>
        </div>
    );
};

export default Weather;