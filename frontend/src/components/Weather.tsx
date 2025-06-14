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
        
        // Auto-refresh every 10 minutes
        const interval = setInterval(getWeather, 600000);
        return () => clearInterval(interval);
    }, []);

    const getWeatherIcon = (description: string) => {
        const desc = description.toLowerCase();
        
        if (desc.includes('céu limpo') || desc.includes('clear')) {
            return (
                <svg className="weather-icon-main" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="5" fill="url(#sunGradient)"/>
                    <g stroke="url(#sunGradient)" strokeWidth="2" strokeLinecap="round">
                        <line x1="12" y1="1" x2="12" y2="4"/>
                        <line x1="12" y1="20" x2="12" y2="23"/>
                        <line x1="1" y1="12" x2="4" y2="12"/>
                        <line x1="20" y1="12" x2="23" y2="12"/>
                        <line x1="4.22" y1="4.22" x2="6.34" y2="6.34"/>
                        <line x1="17.66" y1="17.66" x2="19.78" y2="19.78"/>
                        <line x1="4.22" y1="19.78" x2="6.34" y2="17.66"/>
                        <line x1="17.66" y1="6.34" x2="19.78" y2="4.22"/>
                    </g>
                    <defs>
                        <linearGradient id="sunGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#FFD700"/>
                            <stop offset="100%" stopColor="#FFA500"/>
                        </linearGradient>
                    </defs>
                </svg>
            );
        } else if (desc.includes('nuvens') || desc.includes('cloud')) {
            return (
                <svg className="weather-icon-main" viewBox="0 0 24 24">
                    <path fill="url(#cloudGradient)" d="M19.35 10.04A7.49 7.49 0 0 0 12 4C9.11 4 6.6 5.64 5.35 8.04A5.994 5.994 0 0 0 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96z"/>
                    <defs>
                        <linearGradient id="cloudGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#E3F2FD"/>
                            <stop offset="100%" stopColor="#90CAF9"/>
                        </linearGradient>
                    </defs>
                </svg>
            );
        } else if (desc.includes('chuva') || desc.includes('rain')) {
            return (
                <svg className="weather-icon-main" viewBox="0 0 24 24">
                    <path fill="url(#rainGradient)" d="M19.35 10.04A7.49 7.49 0 0 0 12 4C9.11 4 6.6 5.64 5.35 8.04A5.994 5.994 0 0 0 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96z"/>
                    <g stroke="url(#rainGradient)" strokeWidth="2" strokeLinecap="round">
                        <line x1="8" y1="19" x2="8" y2="21"/>
                        <line x1="8" y1="13" x2="8" y2="15"/>
                        <line x1="16" y1="19" x2="16" y2="21"/>
                        <line x1="16" y1="13" x2="16" y2="15"/>
                        <line x1="12" y1="21" x2="12" y2="23"/>
                        <line x1="12" y1="15" x2="12" y2="17"/>
                    </g>
                    <defs>
                        <linearGradient id="rainGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#42A5F5"/>
                            <stop offset="100%" stopColor="#1976D2"/>
                        </linearGradient>
                    </defs>
                </svg>
            );
        } else {
            return (
                <svg className="weather-icon-main" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="5" fill="url(#defaultGradient)"/>
                    <defs>
                        <linearGradient id="defaultGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#81C784"/>
                            <stop offset="100%" stopColor="#4CAF50"/>
                        </linearGradient>
                    </defs>
                </svg>
            );
        }
    };

    const getTemperatureColor = (temp: number) => {
        if (temp <= 0) return '#2196F3';
        if (temp <= 10) return '#03A9F4';
        if (temp <= 20) return '#4CAF50';
        if (temp <= 25) return '#8BC34A';
        if (temp <= 30) return '#FFEB3B';
        if (temp <= 35) return '#FF9800';
        return '#F44336';
    };

    const getHumidityColor = (humidity: number) => {
        if (humidity <= 30) return '#FF5722';
        if (humidity <= 50) return '#FF9800';
        if (humidity <= 70) return '#4CAF50';
        return '#2196F3';
    };

    if (loading) {
        return (
            <div className="weather-card-modern">
                <div className="weather-header-modern">
                    <h2>Condições Meteorológicas</h2>
                </div>
                <div className="weather-loading">
                    <div className="loading-spinner"></div>
                    <p>Carregando dados meteorológicos...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="weather-card-modern error">
                <div className="weather-header-modern">
                    <h2>Condições Meteorológicas</h2>
                </div>
                <div className="weather-error">
                    <svg className="error-icon" viewBox="0 0 24 24">
                        <path fill="#F44336" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                    </svg>
                    <p>{error}</p>
                </div>
            </div>
        );
    }

    return (
        <>
            <style jsx>{`
                .weather-card-modern {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 20px;
                    padding: 0;
                    margin: 1rem;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    overflow: hidden;
                    position: relative;
                    color: white;
                    backdrop-filter: blur(10px);
                }

                .weather-card-modern::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="75" cy="25" r="1" fill="rgba(255,255,255,0.05)"/><circle cx="50" cy="50" r="1" fill="rgba(255,255,255,0.08)"/><circle cx="25" cy="75" r="1" fill="rgba(255,255,255,0.03)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
                    pointer-events: none;
                }

                .weather-header-modern {
                    background: rgba(255,255,255,0.1);
                    backdrop-filter: blur(20px);
                    padding: 1.5rem 2rem;
                    border-bottom: 1px solid rgba(255,255,255,0.2);
                    position: relative;
                    z-index: 2;
                }

                .weather-header-modern h2 {
                    margin: 0;
                    font-size: 1.8rem;
                    font-weight: 600;
                    text-align: center;
                    color: white;
                    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
                }

                .weather-main-display {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    padding: 2rem;
                    position: relative;
                    z-index: 2;
                }

                .weather-icon-main {
                    width: 120px;
                    height: 120px;
                    margin-bottom: 1rem;
                    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
                    animation: float 3s ease-in-out infinite;
                }

                @keyframes float {
                    0%, 100% { transform: translateY(0px); }
                    50% { transform: translateY(-10px); }
                }

                .weather-description {
                    font-size: 1.5rem;
                    font-weight: 500;
                    margin-bottom: 2rem;
                    text-align: center;
                    text-transform: capitalize;
                    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
                }

                .weather-metrics {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 2rem;
                    width: 100%;
                    max-width: 400px;
                }

                .weather-metric {
                    background: rgba(255,255,255,0.15);
                    backdrop-filter: blur(20px);
                    border-radius: 15px;
                    padding: 1.5rem;
                    text-align: center;
                    border: 1px solid rgba(255,255,255,0.2);
                    transition: all 0.3s ease;
                    position: relative;
                    overflow: hidden;
                }

                .weather-metric::before {
                    content: '';
                    position: absolute;
                    top: -50%;
                    left: -50%;
                    width: 200%;
                    height: 200%;
                    background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
                    transform: rotate(45deg);
                    transition: all 0.5s ease;
                    opacity: 0;
                }

                .weather-metric:hover::before {
                    opacity: 1;
                    animation: shimmer 1.5s ease-in-out;
                }

                @keyframes shimmer {
                    0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
                    100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
                }

                .weather-metric:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                }

                .metric-icon {
                    width: 40px;
                    height: 40px;
                    margin-bottom: 0.8rem;
                    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
                }

                .metric-label {
                    font-size: 0.9rem;
                    opacity: 0.9;
                    margin-bottom: 0.5rem;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    font-weight: 500;
                }

                .metric-value {
                    font-size: 2.2rem;
                    font-weight: 700;
                    color: white;
                    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
                }

                .weather-footer {
                    background: rgba(0,0,0,0.2);
                    padding: 1rem 2rem;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    gap: 0.5rem;
                    position: relative;
                    z-index: 2;
                }

                .timestamp-icon {
                    width: 18px;
                    height: 18px;
                    opacity: 0.8;
                }

                .timestamp-text {
                    font-size: 0.9rem;
                    opacity: 0.9;
                    font-weight: 500;
                }

                .weather-loading, .weather-error {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    padding: 3rem 2rem;
                    text-align: center;
                }

                .loading-spinner {
                    width: 50px;
                    height: 50px;
                    border: 3px solid rgba(255,255,255,0.3);
                    border-radius: 50%;
                    border-top-color: white;
                    animation: spin 1s ease-in-out infinite;
                    margin-bottom: 1rem;
                }

                @keyframes spin {
                    to { transform: rotate(360deg); }
                }

                .error-icon {
                    width: 60px;
                    height: 60px;
                    margin-bottom: 1rem;
                }

                .weather-card-modern.error {
                    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
                }

                @media (max-width: 768px) {
                    .weather-card-modern {
                        margin: 0.5rem;
                        border-radius: 15px;
                    }
                    
                    .weather-header-modern {
                        padding: 1rem 1.5rem;
                    }
                    
                    .weather-header-modern h2 {
                        font-size: 1.5rem;
                    }
                    
                    .weather-main-display {
                        padding: 1.5rem;
                    }
                    
                    .weather-icon-main {
                        width: 100px;
                        height: 100px;
                    }
                    
                    .weather-description {
                        font-size: 1.3rem;
                        margin-bottom: 1.5rem;
                    }
                    
                    .weather-metrics {
                        gap: 1rem;
                        max-width: 100%;
                    }
                    
                    .weather-metric {
                        padding: 1rem;
                    }
                    
                    .metric-value {
                        font-size: 1.8rem;
                    }
                    
                    .weather-footer {
                        padding: 0.8rem 1.5rem;
                    }
                }

                @media (max-width: 480px) {
                    .weather-metrics {
                        grid-template-columns: 1fr;
                        gap: 1rem;
                    }
                    
                    .weather-metric {
                        max-width: 200px;
                        margin: 0 auto;
                    }
                }
            `}</style>
            
            <div className="weather-card-modern">
                <div className="weather-header-modern">
                    <h2>Condições Meteorológicas</h2>
                </div>
                
                <div className="weather-main-display">
                    {getWeatherIcon(weather?.description || '')}
                    <div className="weather-description">
                        {weather?.description}
                    </div>
                    
                    <div className="weather-metrics">
                        <div className="weather-metric">
                            <svg className="metric-icon" viewBox="0 0 24 24">
                                <path fill={getTemperatureColor(weather?.temperature || 0)} d="M17 17.5a5 5 0 1 1-10 0c0-2.54 1.92-4.64 4.38-4.96V5a1.62 1.62 0 1 1 3.24 0v7.54A5.01 5.01 0 0 1 17 17.5zm-5 3a3 3 0 0 0 3-3c0-1.31-.84-2.42-2-2.83V5a1 1 0 1 0-2 0v9.67c-1.16.41-2 1.52-2 2.83a3 3 0 0 0 3 3z"/>
                            </svg>
                            <div className="metric-label">Temperatura</div>
                            <div className="metric-value">{weather?.temperature}°C</div>
                        </div>
                        
                        <div className="weather-metric">
                            <svg className="metric-icon" viewBox="0 0 24 24">
                                <path fill={getHumidityColor(weather?.humidity || 0)} d="M12 2C12 2 5 10 5 15a7 7 0 0 0 14 0C19 10 12 2 12 2zm0 18a5 5 0 0 1-5-5c0-3.07 3.58-7.36 5-9.06C13.42 7.64 17 11.93 17 15a5 5 0 0 1-5 5z"/>
                            </svg>
                            <div className="metric-label">Humidade</div>
                            <div className="metric-value">{weather?.humidity}%</div>
                        </div>
                    </div>
                </div>
                
                <div className="weather-footer">
                    <svg className="timestamp-icon" viewBox="0 0 24 24">
                        <path fill="currentColor" d="M19,19H5V8H19M16,1V3H8V1H6V3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.89 20.1,3 19,3H18V1M17,12H12V17H17V12Z"/>
                    </svg>
                    <span className="timestamp-text">
                        {new Date(weather?.timestamp || "").toLocaleString("pt-pt", {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                        })}
                    </span>
                </div>
            </div>
        </>
    );
};

export default Weather;