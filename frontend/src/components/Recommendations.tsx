import React, { useEffect, useState } from 'react';
import { fetchRecommendations } from '../services/api';
import { Recommendation } from '../types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
    faDroplet, 
    faThermometerHalf, 
    faExclamationTriangle, 
    faCheckCircle, 
    faTimesCircle,
    faLeaf,
    faWater,
    faSeedling
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

    const getIntensityIcon = (intensity: string) => {
        switch(intensity.toLowerCase()) {
            case 'elevada': return faWater;
            case 'média': return faDroplet;
            case 'baixa': return faSeedling;
            default: return faLeaf;
        }
    };

    const getIntensityClass = (intensity: string) => {
        switch(intensity.toLowerCase()) {
            case 'elevada': return 'intensity-high';
            case 'média': return 'intensity-medium';
            case 'baixa': return 'intensity-low';
            default: return 'intensity-none';
        }
    };

    const getStatusClass = (status: string) => {
        switch(status.toLowerCase()) {
            case 'elevada': return 'status-high';
            case 'baixa': return 'status-low';
            default: return 'status-normal';
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
                    <FontAwesomeIcon icon={faExclamationTriangle} />
                    <p>{error}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="recommendations-container">
            <h2 className="recommendations-header">
                <FontAwesomeIcon icon={faLeaf} className="header-icon" />
                Recomendações de Irrigação
            </h2>
            
            {recommendation ? (
                <div className="recommendations-content">
                    {/* Cartão Principal de Recomendação */}
                    <div className={`recommendation-main-card ${recommendation.should_irrigate ? 'irrigate-yes' : 'irrigate-no'}`}>
                        <div className="main-card-icon">
                            <FontAwesomeIcon 
                                icon={recommendation.should_irrigate ? faCheckCircle : faTimesCircle} 
                                className="irrigation-icon"
                            />
                        </div>
                        <div className="main-card-content">
                            <h3 className="irrigation-decision">
                                {recommendation.should_irrigate ? 'Deve Irrigar' : 'Não Precisa Irrigar'}
                            </h3>
                            <div className="irrigation-reason">
                                {recommendation.reason}
                            </div>
                        </div>
                    </div>

                    {/* Cartão de Intensidade */}
                    <div className={`intensity-card ${getIntensityClass(recommendation.intensity)}`}>
                        <div className="intensity-icon">
                            <FontAwesomeIcon icon={getIntensityIcon(recommendation.intensity)} />
                        </div>
                        <div className="intensity-content">
                            <h4>Intensidade de Irrigação</h4>
                            <span className="intensity-value">{recommendation.intensity}</span>
                        </div>
                    </div>

                    {/* Condições Atuais */}
                    <div className="conditions-grid">
                        <div className={`condition-card temperature ${getStatusClass(recommendation.temperature_status)}`}>
                            <div className="condition-icon">
                                <FontAwesomeIcon icon={faThermometerHalf} />
                            </div>
                            <div className="condition-content">
                                <h4>Temperatura</h4>
                                <span className="condition-status">{recommendation.temperature_status}</span>
                            </div>
                        </div>

                        <div className={`condition-card humidity ${getStatusClass(recommendation.humidity_status)}`}>
                            <div className="condition-icon">
                                <FontAwesomeIcon icon={faDroplet} />
                            </div>
                            <div className="condition-content">
                                <h4>Humidade</h4>
                                <span className="condition-status">{recommendation.humidity_status}</span>
                            </div>
                        </div>
                    </div>
                    
                    {/* Avisos */}
                    {recommendation.warnings && recommendation.warnings.length > 0 && (
                        <div className="warnings-section">
                            <div className="warnings-header">
                                <FontAwesomeIcon icon={faExclamationTriangle} className="warning-icon" />
                                <h4>Avisos Importantes</h4>
                            </div>
                            <div className="warnings-list">
                                {recommendation.warnings.map((warning, index) => (
                                    <div key={index} className="warning-item">
                                        <FontAwesomeIcon icon={faExclamationTriangle} className="warning-bullet" />
                                        <span>{warning}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            ) : (
                <div className="no-recommendations">
                    <FontAwesomeIcon icon={faLeaf} className="no-data-icon" />
                    <p>Sem recomendações de irrigação neste momento.</p>
                </div>
            )}
        </div>
    );
};

export default Recommendations;