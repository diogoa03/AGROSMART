import React, { useState, useEffect } from 'react';
import { fetchRecommendations } from '../../services/api';

// Componente que apresenta recomendações de irrigação com base nas condições meteorológicas
const Recommendations = () => {

    // Estados para gerir as recomendações, carregamento e erros
    const [recommendation, setRecommendation] = useState(null); 
    const [loading, setLoading] = useState(true); 
    const [error, setError] = useState(null);

    useEffect(() => {

        // Função assíncrona para obter as recomendações da API
        const fetchData = async () => {
            try {
                // Obtém o token de autenticação do armazenamento local
                const token = localStorage.getItem('token');
                if (!token) {
                    setError('No authentication token found');
                    setLoading(false);
                    return;
                }

                // Chama a API para obter as recomendações
                const data = await fetchRecommendations(token);
                setRecommendation(data);
                setError(null);
            } catch (err) {

                // Define mensagem de erro em caso de falha
                setError('Failed to fetch recommendations');
            } finally {
                
                // Independentemente do resultado, termina o estado de carregamento
                setLoading(false);
            }
        };

        // Executa a função de obtenção de dados quando o componente é montado
        fetchData();
    }, []);

    // Apresenta um indicador de carregamento enquanto os dados estão a ser obtidos
    if (loading) {
        return (
            <div className="card-container">
                <h2 className="card-header">Recomendação</h2>
                <div className="loading-container">
                    <div className="loading-spinner"></div>
                    <p>A carregar recomendações...</p>
                </div>
            </div>
        );
    }

    // Apresenta uma mensagem de erro se ocorrer algum problema
    if (error) {
        return (
            <div className="card-container">
                <h2 className="card-header">Recomendação</h2>
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

    // Renderiza as recomendações quando os dados estão disponíveis
    return (
        <div className="card-container">
            <h2 className="card-header">Recomendação</h2>
            
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
                            <h3>Recomendação</h3>
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