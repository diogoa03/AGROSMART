import React, { useEffect, useState } from 'react';
import { fetchNotifications, clearNotifications, deleteNotification } from '../services/api';
import { Notification } from '../types';

interface EnhancedNotification extends Notification {
  id: string;
  read: boolean;
  ignored: boolean;
}

const Notifications: React.FC = () => {
    const [notifications, setNotifications] = useState<EnhancedNotification[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const getNotifications = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    setError('No authentication token found');
                    setLoading(false);
                    return;
                }
                const response = await fetchNotifications(token);

                setNotifications(
                    (response || []).map((notification: Notification) => ({
                        ...notification,
                        read: false,
                        ignored: false
                    }))
                );
            } catch (err) {
                setError('Failed to fetch notifications');
            } finally {
                setLoading(false);
            }
        };

        getNotifications();
    }, []);

    const markAsRead = (id: string) => {
        setNotifications(prevNotifications => 
            prevNotifications.map(notification => 
                notification.id === id ? { ...notification, read: true } : notification
            )
        );
    };

    const ignoreNotification = async (id: string) => {
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                setError('No authentication token found');
                return;
            }
            await deleteNotification(token, id);
            setNotifications(prevNotifications =>
                prevNotifications.filter(notification => notification.id !== id)
            );
        } catch (err) {
            setError('Falha ao ignorar notificação');
        }
    };

    const handleClearNotifications = async () => {
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                setError('No authentication token found');
                return;
            }
            await clearNotifications(token);
            setNotifications([]); 
        } catch (err) {
            setError('Falha ao limpar notificações');
        }
    };

    const getSeverityLabel = (severity: string) => {
        switch(severity) {
            case 'HIGH':
                return 'Crítico';
            case 'MEDIUM':
                return 'Moderado';
            case 'LOW':
                return 'Baixo';
            default:
                return severity;
        }
    };

    const activeNotifications = notifications.filter(notification => !notification.ignored);

    if (loading) {
        return <div className="card-container">A carregar notificações...</div>;
    }

    if (error) {
        return <div className="card-container">{error}</div>;
    }

    return (
        <div className="card-container">
            <h2 className="card-header">Alertas</h2>
            <button 
                className="action-button ignore" 
                style={{ marginBottom: '1rem' }}
                onClick={handleClearNotifications}
            >
                Limpar todas as notificações
            </button>
            <div>
                {activeNotifications.length === 0 ? (
                    <div className="empty-state">Sem notificações neste momento.</div>
                ) : (
                    activeNotifications.map((notification: EnhancedNotification) => (
                        <div 
                            key={notification.id} 
                            className={`notification-item severity-${notification.severity} ${notification.read ? 'read' : 'unread'}`}
                        >
                            <div className="notification-header">
                                <div className="notification-type">{notification.type}</div>
                                <div className={`severity-badge severity-${notification.severity}`}>
                                    {getSeverityLabel(notification.severity)}
                                </div>
                            </div>
                            <div className="notification-message">{notification.message}</div>
                            {notification.details && (
                                <div className="notification-details">{notification.details}</div>
                            )}
                            <div className="notification-footer">
                                <small className="timestamp">
                                    {new Date(notification.timestamp).toLocaleString('pt-PT')}
                                </small>
                                <div className="notification-actions">
                                    {!notification.read && (
                                        <button 
                                            className="action-button mark-read" 
                                            onClick={() => markAsRead(notification.id)}
                                        >
                                            Marcar como lido
                                        </button>
                                    )}
                                    <button 
                                        className="action-button ignore" 
                                        onClick={() => ignoreNotification(notification.id)}
                                    >
                                        Ignorar
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default Notifications;