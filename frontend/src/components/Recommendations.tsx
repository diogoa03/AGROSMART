import React, { useEffect, useState } from 'react';
import { fetchRecommendations } from '../services/api';
import { Recommendation } from '../types';
import '../styles/recommendations.css';

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

    if (loading) {
        return (
            <div className="card-container">
                <h2 className="card-header">Recomendações de Irrigação</h2>
                <div className="loading-container">
                    <div className="loading-spinner"></div>
                    <p>A carregar recomendações...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="card-container">
                <h2 className="card-header">Recomendações de Irrigação</h2>
                <div style={{ padding: '1rem', textAlign: 'center' }}>
                    <p>{error}</p>
                    <button 
                        onClick={() => window.location.reload()} 
                        style={{ 
                            marginTop: '0.5rem', 
                            padding: '0.5rem 1rem', 
                            backgroundColor: '#1f3c2d',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: 'pointer'
                        }}
                    >
                        Tentar Novamente
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="card-container">
            <h2 className="card-header">Recomendações de Irrigação</h2>
            
            {recommendation ? (
                <div className="recommendation-details">
                    <div className="recommendation-summary">
                        <h3>Resumo</h3>
                        <div className="recommendation-item">
                            <span className="recommendation-label">Deve irrigar:</span>
                            <span className={`irrigation-status ${recommendation.should_irrigate ? 'irrigate-yes' : 'irrigate-no'}`}>
                                {recommendation.should_irrigate ? 'Sim' : 'Não'}
                            </span>
                        </div>
                        <div className="recommendation-item">
                            <span className="recommendation-label">Intensidade:</span>
                            <span>{recommendation.intensity}</span>
                        </div>
                        <div className="recommendation-item">
                            <span className="recommendation-label">Motivo:</span>
                            <span>{recommendation.reason}</span>
                        </div>
                    </div>
                    
                    <div className="recommendation-conditions">
                        <h3>Condições Atuais</h3>
                        <div className="recommendation-item">
                            <span className="recommendation-label">Temperatura:</span>
                            <span>{recommendation.temperature_status}</span>
                        </div>
                        <div className="recommendation-item">
                            <span className="recommendation-label">Humidade:</span>
                            <span>{recommendation.humidity_status}</span>
                        </div>
                    </div>
                    
                    {recommendation.warnings && recommendation.warnings.length > 0 && (
                        <div className="recommendation-warnings">
                            <h3>Avisos</h3>
                            <ul>
                                {recommendation.warnings.map((warning, index) => (
                                    <li key={index}>{warning}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>
            ) : (
                <div style={{ padding: '1rem', textAlign: 'center' }}>
                    Sem recomendações de irrigação neste momento.
                </div>
            )}
        </div>
    );
};

export default Recommendations;