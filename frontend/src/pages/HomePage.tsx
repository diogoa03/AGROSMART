import React from 'react';
import { useHistory } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCloud, faBell, faLeaf, faHistory } from '@fortawesome/free-solid-svg-icons';

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
                    <div className="home-card" onClick={() => navigateTo('/agrosmart/weather')}>
                        <FontAwesomeIcon icon={faCloud} className="home-icon" />
                        <h2>Meteorologia</h2>
                        <p>Previsões precisas e dados meteorológicos em tempo real para suas culturas</p>
                    </div>
                    
                    <div className="home-card" onClick={() => navigateTo('/agrosmart/alerts')}>
                        <FontAwesomeIcon icon={faBell} className="home-icon" />
                        <h2>Alertas Inteligentes</h2>
                        <p>Notificações personalizadas sobre condições adversas e oportunidades</p>
                    </div>
                    
                    <div className="home-card" onClick={() => navigateTo('/agrosmart/recommendations')}>
                        <FontAwesomeIcon icon={faLeaf} className="home-icon" />
                        <h2>Gestão de Plantação</h2>
                        <p>Acompanhe o ciclo de vida das suas culturas e otimize o rendimento</p>
                    </div>
                    
                    <div className="home-card" onClick={() => navigateTo('/agrosmart/history')}>
                        <FontAwesomeIcon icon={faHistory} className="home-icon" />
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
                <button className="cta-button" onClick={() => navigateTo('/agrosmart/contact')}>
                    Contactos
                </button>
            </section>
        </div>
    );
};

export default HomePage;