import React, { useEffect, useState } from 'react';
import { fetchHistory } from '../../services/api';
import socketService from '../../services/socket';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSun, faCloud, faCloudSun, faCloudRain, faCloudShowersHeavy, faBolt, faSnowflake, faSmog, faHistory, faCalendarAlt, faTemperatureHigh, faDroplet } from '@fortawesome/free-solid-svg-icons';

// Componente que mostra o histórico meteorológico
const History = () => {

    // Estados para gerir os dados, carregamento e erros
    const [history, setHistory] = useState([]); 
    const [loading, setLoading] = useState(true); 
    const [error, setError] = useState(null); 

    useEffect(() => {
        // Função para obter os dados históricos da API
        const getHistoryData = async () => {
            try {
                // Obtém o token de autenticação do armazenamento local
                const token = localStorage.getItem('token');
                if (!token) {
                    setError('No authentication token found');
                    setLoading(false);
                    return;
                }
                // Chama a API para obter os dados históricos
                const data = await fetchHistory(token);
                setHistory(data);
            } catch (err) {
                setError('Failed to fetch history data');
            } finally {
                setLoading(false);
            }
        };

        // Carrega os dados quando o componente é montado
        getHistoryData();

        // Configura o listener para atualizações em tempo real usando o serviço de socket
        const unsubscribe = socketService.on('weather_update', () => {
            console.log('Received weather update from server, refreshing history...');
            getHistoryData();
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

    // Mostra indicador de carregamento enquanto os dados estão a ser obtidos
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

    // Mostra mensagem de erro se ocorrer algum problema
    if (error) {
        return (
            <div className="card-container history-card">
                <div className="history-error">
                    <p>{error}</p>
                </div>
            </div>
        );
    }

    // Renderiza a tabela com o histórico meteorológico
    return (
        <div className="card-container history-card">
            <h2 className="card-header">
                <FontAwesomeIcon icon={faHistory} className="header-icon" />
                Histórico Meteorológico
            </h2>
            
            {/* Mostra mensagem se não houver dados históricos */}
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