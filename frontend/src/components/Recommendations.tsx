import React, { useEffect, useState } from 'react';
import { fetchRecommendations } from '../services/api';
import { Recommendation } from '../types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
  faDroplet, 
  faThermometerHalf, 
  faTint, 
  faExclamationTriangle,
  faInfoCircle,
  faCheckCircle,
  faTimesCircle,
  faLeaf,
  faSeedling,
  faExclamationCircle
} from '@fortawesome/free-solid-svg-icons';

const Recommendations: React.FC = () => {
    const [recommendation, setRecommendation] = useState<Recommendation | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const getRecommendations = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    setError('No authentication token found');
                    setLoading(false);
                    return;
                }
                const data = await fetchRecommendations(token);
                setRecommendation(data);
            } catch (err) {
                setError('Failed to fetch recommendations');
            } finally {
                setLoading(false);
            }
        };

        getRecommendations();
    }, []);

    const getIrrigationStatus = (shouldIrrigate: boolean, intensity: string) => {
        if (!shouldIrrigate) {
            return {
                className: 'should-not-irrigate',
                icon: faTimesCircle,
                iconClass: 'no-irrigate',
                title: 'Não Precisa Irrigar',
                subtitle: 'As condições atuais não requerem irrigação'
            };
        }
        
        if (intensity === 'elevada') {
            return {
                className: 'should-irrigate',
                icon: faDroplet,
                iconClass: 'irrigate',
                title: 'Irrigação Necessária',
                subtitle: 'Requer irrigação com intensidade elevada'
            };
        }
        
        return {
            className: 'should-irrigate',
            icon: faCheckCircle,
            iconClass: 'irrigate',
            title: 'Irrigação Recomendada',
            subtitle: 'Condições favoráveis para irrigação'
        };
    };

    const getIntensityClass = (intensity: string) => {
        switch(intensity?.toLowerCase()) {
            case 'nenhuma': return 'intensity-nenhuma';
            case 'baixa': return 'intensity-baixa';
            case 'média': case 'media': return 'intensity-media';
            case 'elevada': return 'intensity-elevada';
            default: return 'intensity-nenhuma';
        }
    };

    const getStatusClass = (status: string) => {
        switch(status?.toLowerCase()) {
            case 'normal': return 'status-normal';
            case 'elevada': case 'alta': return 'status-elevada';
            case 'baixa': return 'status-baixa';
            default: return 'status-normal';
        }
    };

    const formatIntensity = (intensity: string) => {
        const intensityMap: { [key: string]: string } = {
            'nenhuma': 'Nenhuma',
            'baixa': 'Baixa',
            'média': 'Média',
            'media': 'Média',
            'elevada': 'Elevada'
        };
        return intensityMap[intensity?.toLowerCase()] || intensity;
    };

    const formatStatus = (status: string) => {
        const statusMap: { [key: string]: string } = {
            'normal': 'Normal',
            'elevada': 'Elevada',
            'alta': 'Alta',
            'baixa': 'Baixa'
        };
        return statusMap[status?.toLowerCase()] || status;
    };

    if (loading) {
        return (
            <div className="card-container recommendations-card">
                <div className="weather-loading">
                    <div className="loading-spinner"></div>
                    <p>A carregar recomendações...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="card-container recommendations-card">
                <div className="weather-error">
                    <p>{error}</p>
                </div>
            </div>
        );
    }

    if (!recommendation) {
        return (
            <div className="card-container recommendations-card">
                <h2 className="card-header">Recomendações de Irrigação</h2>
                <div className="empty-state">
                    <FontAwesomeIcon icon={faSeedling} className="empty-icon" />
                    <div className="empty-message">Sem recomendações disponíveis</div>
                    <div className="empty-subtitle">Aguarde a próxima análise das condições da vinha</div>
                </div>
            </div>
        );
    }

    const irrigationStatus = getIrrigationStatus(recommendation.should_irrigate, recommendation.intensity);

    return (
        <div className="card-container recommendations-card">
            <h2 className="card-header">Recomendações de Irrigação</h2>
            
            {/* Status Principal de Irrigação */}
            <div className={`irrigation-status ${irrigationStatus.className}`}>
                <FontAwesomeIcon 
                    icon={irrigationStatus.icon} 
                    className={`status-icon ${irrigationStatus.iconClass}`} 
                />
                <div className="status-text">
                    <div className="status-title">{irrigationStatus.title}</div>
                    <div className="status-subtitle">{irrigationStatus.subtitle}</div>
                </div>
            </div>

            {/* Grid de Informações */}
            <div className="recommendation-grid">
                {/* Resumo da Recomendação */}
                <div className="recommendation-section">
                    <div className="section-header">
                        <FontAwesomeIcon icon={faInfoCircle} className="section-icon" />
                        <h3 className="section-title">Resumo da Recomendação</h3>
                    </div>
                    
                    <div className="info-item">
                        <span className="info-label">Irrigação:</span>
                        <span className="info-value">
                            {recommendation.should_irrigate ? 'Sim' : 'Não'}
                        </span>
                    </div>
                    
                    <div className="info-item">
                        <span className="info-label">Intensidade:</span>
                        <span className={`intensity-badge ${getIntensityClass(recommendation.intensity)}`}>
                            {formatIntensity(recommendation.intensity)}
                        </span>
                    </div>
                    
                    <div className="info-item">
                        <span className="info-label">Motivo:</span>
                        <span className="info-value">{recommendation.reason}</span>
                    </div>
                </div>

                {/* Condições Atuais */}
                <div className="recommendation-section">
                    <div className="section-header">
                        <FontAwesomeIcon icon={faLeaf} className="section-icon" />
                        <h3 className="section-title">Condições da Vinha</h3>
                    </div>
                    
                    <div className="info-item">
                        <span className="info-label">
                            <FontAwesomeIcon icon={faThermometerHalf} style={{ marginRight: '0.5rem' }} />
                            Temperatura:
                        </span>
                        <span className={`status-badge ${getStatusClass(recommendation.temperature_status)}`}>
                            {formatStatus(recommendation.temperature_status)}
                        </span>
                    </div>
                    
                    <div className="info-item">
                        <span className="info-label">
                            <FontAwesomeIcon icon={faTint} style={{ marginRight: '0.5rem' }} />
                            Humidade:
                        </span>
                        <span className={`status-badge ${getStatusClass(recommendation.humidity_status)}`}>
                            {formatStatus(recommendation.humidity_status)}
                        </span>
                    </div>
                </div>
            </div>

            {/* Avisos (se existirem) */}
            {recommendation.warnings && recommendation.warnings.length > 0 && (
                <div className="warnings-section">
                    <div className="warnings-header">
                        <FontAwesomeIcon icon={faExclamationTriangle} className="warning-icon" />
                        <h3 className="warnings-title">Avisos Importantes</h3>
                    </div>
                    <ul className="warnings-list">
                        {recommendation.warnings.map((warning, index) => (
                            <li key={index} className="warning-item">
                                <span className="warning-bullet">
                                    <FontAwesomeIcon icon={faExclamationCircle} />
                                </span>
                                <span className="warning-text">{warning}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default Recommendations;