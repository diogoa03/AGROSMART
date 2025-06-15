import React, { useEffect, useState } from 'react';
import { fetchNotifications, clearNotifications, deleteNotification } from '../../services/api'; 

// Componente que gere e apresenta as notificações e alertas do sistema
const Notifications = () => {
    
    // Estados para gerir as notificações, carregamento e erros
    const [notifications, setNotifications] = useState([]); 
    const [loading, setLoading] = useState(true); 
    const [error, setError] = useState(null); 

    useEffect(() => {

        // Função para obter as notificações da API
        const getNotifications = async () => {
            try {

                // Obtém o token de autenticação do armazenamento local
                const token = localStorage.getItem('token');
                if (!token) {
                    setError('No authentication token found');
                    setLoading(false);
                    return;
                }

                // Chama a API para obter as notificações
                const response = await fetchNotifications(token);

                // Processa as notificações e adiciona propriedades adicionais
                setNotifications(
                    (response || []).map((notification) => ({
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

        // Carrega as notificações quando o componente é montado
        getNotifications();
    }, []);

    // Função para marcar uma notificação como lida
    const markAsRead = (id) => {
        setNotifications(prevNotifications => 
            prevNotifications.map(notification => 
                notification.id === id ? { ...notification, read: true } : notification
            )
        );
    };

    // Função para ignorar/eliminar uma notificação
    const ignoreNotification = async (id) => {
        try {
            // Obtém o token de autenticação
            const token = localStorage.getItem('token');
            if (!token) {
                setError('No authentication token found');
                return;
            }

            // Chama a API para eliminar a notificação
            await deleteNotification(token, id);

            // Remove a notificação da lista
            setNotifications(prevNotifications =>
                prevNotifications.filter(notification => notification.id !== id)
            );
        } catch (err) {
            setError('Falha ao ignorar notificação');
        }
    };

    // Função para limpar todas as notificações
    const handleClearNotifications = async () => {
        try {
            // Obtém o token de autenticação
            const token = localStorage.getItem('token');
            if (!token) {
                setError('No authentication token found');
                return;
            }

            // Chama a API para limpar todas as notificações
            await clearNotifications(token);

            // Limpa a lista de notificações
            setNotifications([]); 
        } catch (err) {
            setError('Falha ao limpar notificações');
        }
    };

    // Função para converter o nível de gravidade para português
    const getSeverityLabel = (severity) => {
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

    // Filtra apenas as notificações que não foram ignoradas
    const activeNotifications = notifications.filter(notification => !notification.ignored);

    // Mostra indicador de carregamento enquanto os dados estão a ser obtidos
    if (loading) {
        return <div className="card-container">A carregar notificações...</div>;
    }

    // Mostra mensagem de erro se ocorrer algum problema
    if (error) {
        return <div className="card-container">{error}</div>;
    }
    
    // Renderiza o componente com os dados meteorológicos
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
                    activeNotifications.map((notification) => (
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