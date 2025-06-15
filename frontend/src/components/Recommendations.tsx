import React, { useEffect, useState } from 'react';
import { fetchRecommendations } from '../services/api';
import { Recommendation } from '../types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
    faDroplet, 
    faTemperatureHigh, 
    faExclamationTriangle, 
    faCheckCircle, 
    faTimesCircle,
    faSeedling,
    faCloudRain,
    faThermometerHalf,
    faExclamationCircle,
    faInfoCircle
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

    const getIntensityColor = (intensity: string) => {
        switch(intensity.toLowerCase()) {
            case 'elevada': return '#e74c3c';
            case 'média': return '#f39c12';
            case 'baixa': return '#27ae60';
            case 'nenhuma': return '#95a5a6';
            default: return '#3498db';
        }
    };

    const getStatusColor = (status: string) => {
        switch(status.toLowerCase()) {
            case 'elevada': return '#e74c3c';
            case 'baixa': return '#3498db';
            case 'normal': return '#27ae60';
            default: return '#95a5a6';
        }
    };

    const getIntensityIcon = (intensity: string) => {
        switch(intensity.toLowerCase()) {
            case 'elevada': return faCloudRain;
            case 'média': return faDroplet;
            case 'baixa': return faDroplet;
            case 'nenhuma': return faTimesCircle;
            default: return faDroplet;
        }
    };

    if (loading) {
        return (
            <div className="recommendations-container">
                <div className="recommendations-loading">
                    <div className="loading-spinner"></div>
                    <p>A carregar recomendações...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="recommendations-container">
                <div className="recommendations-error">
                    <FontAwesomeIcon icon={faExclamationCircle} className="error-icon" />
                    <p>{error}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="recommendations-container">
            <div className="recommendations-header">
                <FontAwesomeIcon icon={faSeedling} className="header-icon" />
                <h2>Recomendações de Irrigação para Vinhas</h2>
            </div>
            
            {recommendation ? (
                <div className="recommendations-content">
                    {/* Main Recommendation Card */}
                    <div className={`main-recommendation-card ${recommendation.should_irrigate ? 'irrigate-yes' : 'irrigate-no'}`}>
                        <div className="recommendation-icon">
                            <FontAwesomeIcon 
                                icon={recommendation.should_irrigate ? faCheckCircle : faTimesCircle} 
                                className={`main-icon ${recommendation.should_irrigate ? 'yes' : 'no'}`}
                            />
                        </div>
                        <div className="recommendation-main-content">
                            <h3 className="irrigation-decision">
                                {recommendation.should_irrigate ? 'Recomenda-se Irrigação' : 'Irrigação Não Necessária'}
                            </h3>
                            <p className="irrigation-reason">{recommendation.reason}</p>
                        </div>
                        <div className="intensity-badge">
                            <FontAwesomeIcon 
                                icon={getIntensityIcon(recommendation.intensity)} 
                                style={{ color: getIntensityColor(recommendation.intensity) }}
                            />
                            <span style={{ color: getIntensityColor(recommendation.intensity) }}>
                                Intensidade: {recommendation.intensity}
                            </span>
                        </div>
                    </div>

                    {/* Current Conditions */}
                    <div className="conditions-grid">
                        <div className="condition-card temperature">
                            <div className="condition-header">
                                <FontAwesomeIcon icon={faTemperatureHigh} className="condition-icon temp-icon" />
                                <h4>Temperatura</h4>
                            </div>
                            <div className="condition-content">
                                <span 
                                    className="condition-status"
                                    style={{ color: getStatusColor(recommendation.temperature_status) }}
                                >
                                    {recommendation.temperature_status.charAt(0).toUpperCase() + recommendation.temperature_status.slice(1)}
                                </span>
                            </div>
                        </div>

                        <div className="condition-card humidity">
                            <div className="condition-header">
                                <FontAwesomeIcon icon={faDroplet} className="condition-icon humidity-icon" />
                                <h4>Humidade</h4>
                            </div>
                            <div className="condition-content">
                                <span 
                                    className="condition-status"
                                    style={{ color: getStatusColor(recommendation.humidity_status) }}
                                >
                                    {recommendation.humidity_status.charAt(0).toUpperCase() + recommendation.humidity_status.slice(1)}
                                </span>
                            </div>
                        </div>
                    </div>

                    {/* Warnings Section */}
                    {recommendation.warnings && recommendation.warnings.length > 0 && (
                        <div className="warnings-section">
                            <div className="warnings-header">
                                <FontAwesomeIcon icon={faExclamationTriangle} className="warning-icon" />
                                <h4>Avisos Importantes</h4>
                            </div>
                            <div className="warnings-list">
                                {recommendation.warnings.map((warning, index) => (
                                    <div key={index} className="warning-item">
                                        <FontAwesomeIcon icon={faInfoCircle} className="warning-bullet" />
                                        <span>{warning}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Action Summary */}
                    <div className="action-summary">
                        <div className="summary-content">
                            <h4>Resumo da Ação</h4>
                            <div className="summary-details">
                                <div className="summary-item">
                                    <strong>Irrigação:</strong> 
                                    <span className={recommendation.should_irrigate ? 'yes' : 'no'}>
                                        {recommendation.should_irrigate ? 'Necessária' : 'Não necessária'}
                                    </span>
                                </div>
                                <div className="summary-item">
                                    <strong>Intensidade:</strong> 
                                    <span style={{ color: getIntensityColor(recommendation.intensity) }}>
                                        {recommendation.intensity}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            ) : (
                <div className="no-recommendations">
                    <FontAwesomeIcon icon={faInfoCircle} className="info-icon" />
                    <p>Sem recomendações de irrigação neste momento.</p>
                </div>
            )}
        </div>
    );
};

export default Recommendations;