import axios from 'axios';

// Define o endereço base da API para todos os pedidos
const API_BASE_URL = 'http://localhost:5000/api';

// Obtém os dados meteorológicos atuais do servidor
export const fetchWeather = async (token) => {
    const response = await fetch(`${API_BASE_URL}/weather`, {
        headers: {
            'Authorization': 'Basic ' + token
        }
    });
    if (!response.ok) {
        throw new Error('Failed to fetch weather data');
    }
    return response.json();
};

// Obtém o histórico de dados meteorológicos armazenados
export const fetchHistory = async (token) => {
    const response = await fetch(`${API_BASE_URL}/history/weather`, {
        headers: {
            'Authorization': 'Basic ' + token
        }
    });
    if (!response.ok) {
        throw new Error('Failed to fetch history data');
    }
    return response.json();
};

// Obtém recomendações para irrigação com base nos dados meteorológicos
export const fetchRecommendations = async (token) => {
    const response = await fetch(`${API_BASE_URL}/recommendations`, {
        headers: {
            'Authorization': 'Basic ' + token
        }
    });
    if (!response.ok) {
        throw new Error('Failed to fetch recommendations');
    }
    return response.json();
};

// Obtém as notificações e alertas do utilizador
export const fetchNotifications = async (token) => {
    const response = await fetch(`${API_BASE_URL}/notifications`, {
        headers: {
            'Authorization': 'Basic ' + token
        }
    });
    if (!response.ok) {
        throw new Error('Failed to fetch notifications');
    }
    return response.json();
};

// Apaga uma notificação específica usando o seu identificador
export const deleteNotification = async (token, id) => {
    const response = await fetch(`${API_BASE_URL}/notifications/${id}`, {
        method: 'DELETE',
        headers: {
            'Authorization': 'Basic ' + token
        }
    });
    if (!response.ok) {
        throw new Error('Failed to delete notification');
    }
    return response.json();
};

// Apaga todas as notificações do utilizador de uma só vez
export const clearNotifications = async (token) => {
    const response = await fetch(`${API_BASE_URL}/notifications`, {
        method: 'DELETE',
        headers: {
            'Authorization': 'Basic ' + token
        }
    });
    if (!response.ok) {
        throw new Error('Failed to clear notifications');
    }
    return response.json();
};