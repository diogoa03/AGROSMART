import React, { useEffect, useState } from 'react';
import { fetchRecommendations } from '../services/api';
import { Recommendation } from '../types';

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
        return <div className="card-container">A carregar recomendações...</div>;
    }

    if (error) {
        return <div className="card-container">{error}</div>;
    }

    return (
        <div className="card-container">
            <h2 className="card-header">Recomendações de Irrigação</h2>
            
            {recommendation ? (
                <div className="recommendation-details">
                    <div className="recommendation-summary">
                        <h3>Resumo:</h3>
                        <p><strong>Deve irrigar:</strong> {recommendation.should_irrigate ? 'Sim' : 'Não'}</p>
                        <p><strong>Intensidade:</strong> {recommendation.intensity}</p>
                        <p><strong>Motivo:</strong> {recommendation.reason}</p>
                    </div>
                    
                    <div className="recommendation-conditions">
                        <h3>Condições Atuais:</h3>
                        <p><strong>Temperatura:</strong> {recommendation.temperature_status}</p>
                        <p><strong>Humidade:</strong> {recommendation.humidity_status}</p>
                    </div>
                    
                    {recommendation.warnings && recommendation.warnings.length > 0 && (
                        <div className="recommendation-warnings">
                            <h3>Avisos:</h3>
                            <ul>
                                {recommendation.warnings.map((warning, index) => (
                                    <li key={index}>{warning}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>
            ) : (
                <div>Sem recomendações de irrigação neste momento.</div>
            )}
        </div>
    );
};

export default Recommendations;