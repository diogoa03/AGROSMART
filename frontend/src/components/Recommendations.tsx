import React, { useEffect, useState } from 'react';
import { fetchRecommendations } from '../services/api';
import { Recommendation } from '../types';
import RecommendationDisplay from '../components/Feature/RecommendationDisplay';
import './RecommendationsPage.css';

const RecommendationsPage: React.FC = () => {
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
                <RecommendationDisplay recommendation={recommendation} />
            ) : (
                <div>Sem recomendações de irrigação neste momento.</div>
            )}
        </div>
    );
};

export default RecommendationsPage;