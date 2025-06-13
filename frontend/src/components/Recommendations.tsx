import React, { useEffect, useState } from 'react';
import { fetchRecommendations } from '../services/api';
import { Recommendation } from '../types';

const Recommendations: React.FC = () => {
    const [recommendations, setRecommendations] = useState<Recommendation | null>(null);
    const [notifications, setNotifications] = useState<any[]>([]);
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
                setRecommendations(data);
                
                // Set example notifications if none exist
                const exampleNotifications = [
                    {
                        type: 'HUMIDITY_ALERT',
                        message: 'WARNING',
                        severity: 'HIGH',
                        details: 'Solo com níveis baixos de umidade detectado. Irrigação recomendada urgentemente.'
                    }
                ];
                
                setNotifications(data.notifications || exampleNotifications);
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
            <div>
                {notifications.map((notification, index) => (
                    <div key={index} className={`notification-item severity-${notification.severity}`}>
                        <div className="notification-type">{notification.type}:</div>
                        <div>{notification.message}</div>
                        {notification.details && <div className="notification-details">{notification.details}</div>}
                    </div>
                ))}
                {notifications.length === 0 && (
                    <div>Sem recomendações de irrigação neste momento.</div>
                )}
            </div>
        </div>
    );
};

export default Recommendations;