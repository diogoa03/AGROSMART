import React, { useEffect, useState } from 'react';
import { fetchHistory } from '../services/api';
import { WeatherData } from '../types';
import io from 'socket.io-client';

const History: React.FC = () => {
    const [history, setHistory] = useState<WeatherData[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const [filter, setFilter] = useState<string>('all');
    const [sortBy, setSortBy] = useState<'date' | 'temperature' | 'humidity'>('date');
    const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

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

    // Função para obter ícone baseado na descrição
    const getWeatherIcon = (description: string) => {
        const desc = description.toLowerCase();
        if (desc.includes('limpo') || desc.includes('clear')) return '☀️';
        if (desc.includes('nuvens') || desc.includes('cloud')) return '☁️';
        if (desc.includes('chuva') || desc.includes('rain')) return '🌧️';
        if (desc.includes('trovoada') || desc.includes('thunder')) return '⛈️';
        if (desc.includes('neve') || desc.includes('snow')) return '🌨️';
        if (desc.includes('nevoeiro') || desc.includes('fog')) return '🌫️';
        return '🌤️';
    };

    // Função para obter cor baseada na temperatura
    const getTemperatureColor = (temp: number) => {
        if (temp >= 30) return '#ff4444';
        if (temp >= 25) return '#ff8800';
        if (temp >= 20) return '#ffaa00';
        if (temp >= 15) return '#88cc00';
        if (temp >= 10) return '#00ccaa';
        if (temp >= 5) return '#0088cc';
        return '#4444cc';
    };

    // Função para obter cor baseada na humidade
    const getHumidityColor = (humidity: number) => {
        if (humidity >= 80) return '#0066cc';
        if (humidity >= 60) return '#0088aa';
        if (humidity >= 40) return '#00aa88';
        if (humidity >= 20) return '#88aa00';
        return '#cc6600';
    };

    // Filtrar dados baseado no período
    const getFilteredData = () => {
        let filtered = [...history];
        const now = new Date();
        
        switch (filter) {
            case 'today':
                filtered = history.filter(entry => {
                    const entryDate = new Date(entry.timestamp);
                    return entryDate.toDateString() === now.toDateString();
                });
                break;
            case 'week':
                const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
                filtered = history.filter(entry => 
                    new Date(entry.timestamp) >= weekAgo
                );
                break;
            case 'month':
                const monthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
                filtered = history.filter(entry => 
                    new Date(entry.timestamp) >= monthAgo
                );
                break;
        }

        // Ordenar dados
        filtered.sort((a, b) => {
            let aValue, bValue;
            
            switch (sortBy) {
                case 'temperature':
                    aValue = a.temperature;
                    bValue = b.temperature;
                    break;
                case 'humidity':
                    aValue = a.humidity;
                    bValue = b.humidity;
                    break;
                case 'date':
                default:
                    aValue = new Date(a.timestamp).getTime();
                    bValue = new Date(b.timestamp).getTime();
                    break;
            }

            if (sortOrder === 'asc') {
                return aValue - bValue;
            } else {
                return bValue - aValue;
            }
        });

        return filtered;
    };

    const filteredHistory = getFilteredData();

    if (loading) {
        return (
            <div className="card-container">
                <div className="loading-spinner">
                    <div className="spinner"></div>
                    <p>A carregar histórico...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="card-container">
                <div className="error-message">
                    <span className="error-icon">⚠️</span>
                    <p>{error}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="card-container">
            <div className="history-header">
                <h2 className="card-header">Histórico Meteorológico</h2>
                
                {/* Controles de filtro e ordenação */}
                <div className="history-controls">
                    <div className="filter-group">
                        <label>Período:</label>
                        <select 
                            value={filter} 
                            onChange={(e) => setFilter(e.target.value)}
                            className="filter-select"
                        >
                            <option value="all">Todos</option>
                            <option value="today">Hoje</option>
                            <option value="week">Última Semana</option>
                            <option value="month">Último Mês</option>
                        </select>
                    </div>
                    
                    <div className="filter-group">
                        <label>Ordenar por:</label>
                        <select 
                            value={sortBy} 
                            onChange={(e) => setSortBy(e.target.value as 'date' | 'temperature' | 'humidity')}
                            className="filter-select"
                        >
                            <option value="date">Data/Hora</option>
                            <option value="temperature">Temperatura</option>
                            <option value="humidity">Humidade</option>
                        </select>
                    </div>
                    
                    <button 
                        onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
                        className="sort-button"
                        title={`Ordenação ${sortOrder === 'asc' ? 'Crescente' : 'Decrescente'}`}
                    >
                        {sortOrder === 'asc' ? '↑' : '↓'}
                    </button>
                </div>
            </div>

            {/* Estatísticas resumidas */}
            {filteredHistory.length > 0 && (
                <div className="history-stats">
                    <div className="stat-card">
                        <span className="stat-icon">🌡️</span>
                        <div className="stat-info">
                            <span className="stat-label">Temp. Média</span>
                            <span className="stat-value">
                                {(filteredHistory.reduce((sum, entry) => sum + entry.temperature, 0) / filteredHistory.length).toFixed(1)}°C
                            </span>
                        </div>
                    </div>
                    
                    <div className="stat-card">
                        <span className="stat-icon">💧</span>
                        <div className="stat-info">
                            <span className="stat-label">Humidade Média</span>
                            <span className="stat-value">
                                {Math.round(filteredHistory.reduce((sum, entry) => sum + entry.humidity, 0) / filteredHistory.length)}%
                            </span>
                        </div>
                    </div>
                    
                    <div className="stat-card">
                        <span className="stat-icon">📊</span>
                        <div className="stat-info">
                            <span className="stat-label">Total Registos</span>
                            <span className="stat-value">{filteredHistory.length}</span>
                        </div>
                    </div>
                </div>
            )}

            {/* Lista de dados históricos */}
            <div className="history-timeline">
                {filteredHistory.length === 0 ? (
                    <div className="empty-state">
                        <span className="empty-icon">📭</span>
                        <p>Nenhum dado histórico disponível para o período selecionado.</p>
                    </div>
                ) : (
                    filteredHistory.map((entry, index) => (
                        <div key={index} className="history-entry">
                            <div className="entry-icon">
                                <span className="weather-emoji">{getWeatherIcon(entry.description)}</span>
                            </div>
                            
                            <div className="entry-content">
                                <div className="entry-main">
                                    <div className="entry-weather">
                                        <span 
                                            className="temperature"
                                            style={{ color: getTemperatureColor(entry.temperature) }}
                                        >
                                            {entry.temperature}°C
                                        </span>
                                        <span 
                                            className="humidity"
                                            style={{ color: getHumidityColor(entry.humidity) }}
                                        >
                                            {entry.humidity}%
                                        </span>
                                    </div>
                                    
                                    <div className="entry-description">
                                        {entry.description}
                                    </div>
                                </div>
                                
                                <div className="entry-timestamp">
                                    {new Date(entry.timestamp).toLocaleString('pt-PT', {
                                        day: '2-digit',
                                        month: '2-digit',
                                        year: 'numeric',
                                        hour: '2-digit',
                                        minute: '2-digit'
                                    })}
                                </div>
                            </div>
                        </div>
                    ))
                )}
            </div>

            <style jsx>{`
                .history-header {
                    display: flex;
                    flex-direction: column;
                    gap: 1rem;
                    margin-bottom: 2rem;
                }

                .history-controls {
                    display: flex;
                    gap: 1rem;
                    align-items: end;
                    flex-wrap: wrap;
                }

                .filter-group {
                    display: flex;
                    flex-direction: column;
                    gap: 0.3rem;
                }

                .filter-group label {
                    font-size: 0.9rem;
                    font-weight: 500;
                    color: #1f3c2d;
                }

                .filter-select {
                    padding: 0.5rem;
                    border: 2px solid #1f3c2d;
                    border-radius: 4px;
                    background-color: white;
                    color: #1f3c2d;
                    font-size: 0.9rem;
                    cursor: pointer;
                }

                .filter-select:focus {
                    outline: none;
                    border-color: #2e5c42;
                    box-shadow: 0 0 0 3px rgba(31, 60, 45, 0.1);
                }

                .sort-button {
                    padding: 0.5rem 0.8rem;
                    border: 2px solid #1f3c2d;
                    border-radius: 4px;
                    background-color: white;
                    color: #1f3c2d;
                    font-size: 1.2rem;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }

                .sort-button:hover {
                    background-color: #1f3c2d;
                    color: white;
                    transform: translateY(-1px);
                }

                .history-stats {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 1rem;
                    margin-bottom: 2rem;
                }

                .stat-card {
                    display: flex;
                    align-items: center;
                    gap: 1rem;
                    padding: 1rem;
                    background-color: #f8f5ea;
                    border: 2px solid #1f3c2d;
                    border-radius: 8px;
                    transition: transform 0.3s ease;
                }

                .stat-card:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(31, 60, 45, 0.1);
                }

                .stat-icon {
                    font-size: 2rem;
                }

                .stat-info {
                    display: flex;
                    flex-direction: column;
                }

                .stat-label {
                    font-size: 0.9rem;
                    color: #666;
                    margin-bottom: 0.2rem;
                }

                .stat-value {
                    font-size: 1.3rem;
                    font-weight: bold;
                    color: #1f3c2d;
                }

                .history-timeline {
                    display: flex;
                    flex-direction: column;
                    gap: 1rem;
                }

                .history-entry {
                    display: flex;
                    gap: 1rem;
                    padding: 1.5rem;
                    background-color: #f8f5ea;
                    border: 2px solid #1f3c2d;
                    border-radius: 8px;
                    transition: all 0.3s ease;
                    position: relative;
                }

                .history-entry:hover {
                    transform: translateX(5px);
                    box-shadow: -4px 4px 8px rgba(31, 60, 45, 0.1);
                }

                .entry-icon {
                    flex-shrink: 0;
                    width: 60px;
                    height: 60px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background-color: white;
                    border: 2px solid #1f3c2d;
                    border-radius: 50%;
                }

                .weather-emoji {
                    font-size: 2rem;
                }

                .entry-content {
                    flex: 1;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                }

                .entry-main {
                    display: flex;
                    flex-direction: column;
                    gap: 0.5rem;
                }

                .entry-weather {
                    display: flex;
                    gap: 2rem;
                    align-items: center;
                }

                .temperature {
                    font-size: 1.8rem;
                    font-weight: bold;
                    display: flex;
                    align-items: center;
                }

                .humidity {
                    font-size: 1.4rem;
                    font-weight: 500;
                    display: flex;
                    align-items: center;
                }

                .entry-description {
                    font-size: 1.1rem;
                    color: #1f3c2d;
                    font-weight: 500;
                    text-transform: capitalize;
                }

                .entry-timestamp {
                    font-size: 0.9rem;
                    color: #666;
                    margin-top: 0.5rem;
                    font-weight: 500;
                }

                .empty-state {
                    text-align: center;
                    padding: 3rem 1rem;
                    color: #666;
                }

                .empty-icon {
                    font-size: 4rem;
                    display: block;
                    margin-bottom: 1rem;
                }

                .loading-spinner {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 1rem;
                    padding: 3rem 1rem;
                }

                .spinner {
                    width: 40px;
                    height: 40px;
                    border: 4px solid #f3f3f3;
                    border-top: 4px solid #1f3c2d;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                }

                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }

                .error-message {
                    display: flex;
                    align-items: center;
                    gap: 1rem;
                    padding: 2rem;
                    background-color: #ffe6e6;
                    border: 2px solid #ff4444;
                    border-radius: 8px;
                    color: #cc0000;
                }

                .error-icon {
                    font-size: 2rem;
                }

                /* Responsividade */
                @media (max-width: 768px) {
                    .history-controls {
                        flex-direction: column;
                        align-items: stretch;
                    }

                    .filter-group {
                        flex-direction: row;
                        align-items: center;
                        justify-content: space-between;
                    }

                    .sort-button {
                        align-self: center;
                        width: fit-content;
                        margin: 0 auto;
                    }

                    .history-stats {
                        grid-template-columns: 1fr;
                    }

                    .entry-weather {
                        gap: 1rem;
                    }

                    .temperature {
                        font-size: 1.5rem;
                    }

                    .humidity {
                        font-size: 1.2rem;
                    }

                    .history-entry {
                        padding: 1rem;
                    }

                    .entry-icon {
                        width: 50px;
                        height: 50px;
                    }

                    .weather-emoji {
                        font-size: 1.5rem;
                    }
                }

                @media (max-width: 480px) {
                    .history-entry {
                        flex-direction: column;
                        align-items: center;
                        text-align: center;
                    }

                    .entry-content {
                        width: 100%;
                    }

                    .entry-weather {
                        justify-content: center;
                    }
                }
            `}</style>
        </div>
    );
};

export default History;