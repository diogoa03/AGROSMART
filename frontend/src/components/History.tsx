import React, { useEffect, useState } from 'react';
import { fetchHistory } from '../services/api';
import { WeatherData } from '../types';
import io from 'socket.io-client';

const History: React.FC = () => {
    const [history, setHistory] = useState<WeatherData[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const getHistoryData = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    setError('No authentication token found');
                    setLoading(false);
                    return;
                }
                const data = await fetchHistory(token);
                setHistory(data);
            } catch (err) {
                setError('Failed to fetch history data');
            } finally {
                setLoading(false);
            }
        };

        // Initial data fetch
        getHistoryData();

        // Connect to Socket.IO
        const socket = io('http://localhost:5000'); // Replace with your backend URL
        
        // Listen for weather updates
        socket.on('weather_update', () => {
            console.log('Received weather update from server, refreshing history...');
            getHistoryData();
        });

        // Clean up socket connection when component unmounts
        return () => {
            socket.disconnect();
        };
    }, []);

    if (loading) {
        return <div className="card-container">A carregar histórico...</div>;
    }

    if (error) {
        return <div className="card-container">{error}</div>;
    }

    return (
        <div className="card-container">
            <h2 className="card-header">Histórico Meteorológico</h2>
            <table>
                <thead>
                    <tr>
                        <th>Temperature</th>
                        <th>Humidity</th>
                        <th>Description</th>
                        <th>Timestamp</th>
                    </tr>
                </thead>
                <tbody>
                    {history.map((entry, index) => (
                        <tr key={index}>
                            <td>{entry.temperature}°C</td>
                            <td>{entry.humidity}%</td>
                            <td>{entry.description}</td>
                            <td>{new Date(entry.timestamp).toLocaleString('pt-PT')}</td>
                        </tr>
                    ))}
                    {history.length === 0 && (
                        <tr>
                            <td colSpan={4}>No historical data available.</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default History;