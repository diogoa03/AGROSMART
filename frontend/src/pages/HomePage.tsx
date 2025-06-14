import React from 'react';
import { useHistory } from 'react-router-dom';

const HomePage: React.FC = () => {
    const history = useHistory();

    const navigateTo = (path: string) => {
        history.push(path);
    };

    return (
        <div className="home-container">
            <section className="hero-section">
                <h1 className="welcome-title">Agricultura Inteligente para o Futuro</h1>
                <p className="welcome-subtitle">Gerencie suas culturas com tecnologia avançada. Monitore condições meteorológicas, 
                receba alertas personalizados e otimize sua produção agrícola.</p>
            </section>

            <section className="features-section">
                <h2 className="section-title">Funcionalidades Principais</h2>
                <p className="section-subtitle">Uma plataforma completa para gestão agrícola moderna, 
                combinando dados meteorológicos em tempo real com ferramentas intuitivas.</p>
                
                <div className="home-grid">
                    <div className="home-card" onClick={() => navigateTo('/dashboard/weather')}>
                        <svg className="home-icon" viewBox="0 0 24 24">
                            <path fill="currentColor" d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96z"/>
                        </svg>
                        <h2>Meteorologia</h2>
                        <p>Previsões precisas e dados meteorológicos em tempo real para suas culturas</p>
                    </div>
                    
                    <div className="home-card" onClick={() => navigateTo('/dashboard/alerts')}>
                        <svg className="home-icon" viewBox="0 0 24 24">
                            <path fill="currentColor" d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2zm6-6v-5c0-3.07-1.63-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.64 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2zm-2 1H8v-6c0-2.48 1.51-4.5 4-4.5s4 2.02 4 4.5v6z"/>
                        </svg>
                        <h2>Alertas Inteligentes</h2>
                        <p>Notificações personalizadas sobre condições adversas e oportunidades</p>
                    </div>
                    
                    <div className="home-card" onClick={() => navigateTo('/dashboard/recommendations')}>
                        <svg className="home-icon" viewBox="0 0 24 24">
                            <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm4.17-5.24l-1.1-1.1c.71-1.33.53-3.01-.59-4.13C13.79 8.84 12.9 8.5 12 8.5c-.03 0-.06.01-.09.01L13 9.6l-1.06 1.06-2.83-2.83L11.94 5 13 6.06l-.96.96c1.27-.01 2.53.47 3.5 1.44 1.42 1.42 1.74 3.49.93 5.2l1.11 1.11-1.41 1.99z"/>
                        </svg>
                        <h2>Gestão de Plantação</h2>
                        <p>Acompanhe o ciclo de vida das suas culturas e otimize o rendimento</p>
                    </div>
                    
                    <div className="home-card" onClick={() => navigateTo('/dashboard/history')}>
                        <svg className="home-icon" viewBox="0 0 24 24">
                            <path fill="currentColor" d="M13 3c-4.97 0-9 4.03-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42C8.27 19.99 10.51 21 13 21c4.97 0 9-4.03 9-9s-4.03-9-9-9zm-1 5v5l4.28 2.54.72-1.21-3.5-2.08V8H12z"/>
                        </svg>
                        <h2>Histórico Detalhado</h2>
                        <p>Analise dados históricos para tomar decisões mais informadas</p>
                    </div>
                </div>
            </section>

            <section className="about-section">
                <div className="about-content">
                    <h2 className="section-title">Tecnologia ao Serviço da Agricultura</h2>
                    <p>O AgroSmart combina sensores IoT, inteligência artificial e análise de dados 
                    para revolucionar a forma como gere as suas culturas. Tome decisões baseadas 
                    em dados precisos e aumente a produtividade da sua exploração agrícola.</p>
                    
                    <ul className="about-features">
                        <li>Monitorização em tempo real</li>
                        <li>Previsões meteorológicas precisas</li>
                        <li>Alertas personalizados</li>
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
                <h2>Pronto para Revolucionar a Sua Agricultura?</h2>
                <p>Otimize suas colheitas e aumente a produtividade com o AgroSmart</p>
                <button className="cta-button" onClick={() => navigateTo('/dashboard/weather')}>
                    Começar agora
                </button>
            </section>
        </div>
    );
};

export default HomePage;