import React from 'react';
import { useHistory } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCloud, faBell, faLeaf, faHistory } from '@fortawesome/free-solid-svg-icons';

// Componente que representa a página inicial da aplicação
const HomePage = () => {
    // Hook para gerir a navegação entre páginas
    const history = useHistory();

    // Função para navegar para uma página específica
    const navigateTo = (path) => {
        history.push(path);
    };

    // Renderiza a página inicial completa
    return (
        <div className="home-container">
            <section className="hero-section">
                <h1 className="welcome-title">AgroSmart</h1>
                <p className="welcome-subtitle">AGROSMART é um sistema de gestão agrícola que utiliza Flask e React 
                    para fornecer monitorização meteorológica em tempo real e recomendações inteligentes de irrigação.</p>
            </section>

            <section className="features-section">
                <h2 className="section-title">Funcionalidades Principais</h2>
                <p className="section-subtitle">Uma plataforma completa para gestão agrícola com os seguintes serviços:</p>
                
                <div className="home-grid">
                    <div className="home-card" onClick={() => navigateTo('/agrosmart/weather')}>
                        <FontAwesomeIcon icon={faCloud} className="home-icon" />
                        <h2>Meteorologia</h2>
                        <p>Previsões metereológicos, de temperatura e humidade</p>
                    </div>
                    
                    <div className="home-card" onClick={() => navigateTo('/agrosmart/alerts')}>
                        <FontAwesomeIcon icon={faBell} className="home-icon" /> 
                        <h2>Alertas</h2>
                        <p>Notificações personalizadas sobre condições adversas e oportunidades</p>
                    </div>
                    
                    <div className="home-card" onClick={() => navigateTo('/agrosmart/recommendations')}>
                        <FontAwesomeIcon icon={faLeaf} className="home-icon" />
                        <h2>Recomendação</h2>
                        <p>Resumo, Condições Atuais e Recomendação para as vinhas</p>
                    </div>
                    
                    <div className="home-card" onClick={() => navigateTo('/agrosmart/history')}>
                        <FontAwesomeIcon icon={faHistory} className="home-icon" />
                        <h2>Histórico</h2>
                        <p>Analise dados históricos da Metereologia</p>
                    </div>
                </div>
            </section>

            <section className="about-section">
                <div className="about-content">
                    <h2 className="section-title">O serviço que mais cresce no país!</h2>
                    <p>A AgroSmart já é o serviço de agricultura que mais cresce no país pelas suas incríveis funcionalidades:</p>
                    
                    <ul className="about-features">
                        <li>Monitorização em tempo real</li>
                        <li>Previsões meteorológicas</li>
                        <li>Alertas</li>
                        <li>Interface intuitiva e responsiva</li>
                    </ul>
                </div>
                
                <div className="stats-container">
                    <div className="stat-card">
                        <div className="stat-value">98%</div>
                        <div className="stat-label">Precisão</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-value">5000+</div>
                        <div className="stat-label">Utilizadores</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-value">24/7</div>
                        <div className="stat-label">Monitorização</div>
                    </div>
                    <div className="stat-card">
                        <div className="stat-value">30%</div>
                        <div className="stat-label">+ Produção</div>
                    </div>
                </div>
            </section>

            <section className="cta-section">
                <h2>Tem alguma sugestão ou problema com o nosso serviço?</h2>
                <button className="cta-button" onClick={() => navigateTo('/agrosmart/contact')}>
                    Contactos
                </button>
            </section>
        </div>
    );
};

export default HomePage;