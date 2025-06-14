import axios from 'axios';
import { useEffect } from 'react';

const API_URL = 'http://localhost:5000/api';

export async function fetchHistory(token: string) {
    const response = await axios.get(`${API_URL}/history/weather`, {
        headers: {
            Authorization: `Basic ${token}`,
        },
    });
    return response.data;
}

export async function fetchWeather(token: string) {
    const response = await axios.get(`${API_URL}/weather`, {
        headers: {
            Authorization: `Basic ${token}`,
        },
    });
    return response.data;
}

export async function fetchRecommendations(token: string) {
    const response = await axios.get(`${API_URL}/recommendations`, {
        headers: {
            Authorization: `Basic ${token}`,
        },
    });
    return response.data;
}

export async function fetchNotifications(token: string) {
    const response = await axios.get(`${API_URL}/notifications`, {
        headers: {
            Authorization: `Basic ${token}`,
        },
    });
    return response.data;
}

export async function clearNotifications(token: string) {
    const response = await axios.delete(`${API_URL}/notifications`, {
        headers: {
            Authorization: `Basic ${token}`,
        },
    });
    return response.data;
}

export async function deleteNotification(token: string, notificationId: string) {
    const response = await axios.delete(`${API_URL}/notifications/${notificationId}`, {
        headers: {
            Authorization: `Basic ${token}`,
        },
    });
    return response.data;
}
