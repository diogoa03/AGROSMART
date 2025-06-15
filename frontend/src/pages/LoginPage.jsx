import React from 'react';
import { useHistory } from 'react-router-dom';
import LoginForm from '../components/forms/LoginForm';  // Use o caminho correto
import { login } from '../services/auth';

// Componente que representa a página de login da aplicação
const LoginPage = () => {
    // Hook para gerir a navegação entre páginas
    const history = useHistory();

    // Função para processar o login do utilizador
    const handleLogin = async (username, password) => {
        try {
            await login(username, password);
            history.push('/agrosmart'); 
        } catch (error) {
            console.error("Login failed:", error);
            throw error; 
        }
    };

    // Função para redirecionar o utilizador para a página de registo
    const handleGoToRegister = () => {
        history.push('/register');
    };

    // Renderiza a página de login completa
    return (
        <div className="login-container">
            <div className="login-card">
                <div className="login-header">
                    <h2>Login</h2>
                    <div className="separator">|</div>
                    <img src="/agrosmart-logo.svg" alt="AgroSmart" height="80" />
                </div>
                <LoginForm onLogin={handleLogin} />
                <div className="back-to-login">
                    <p>Não tem uma conta?</p>
                    <button 
                        type="button" 
                        className="back-to-login-btn"
                        onClick={handleGoToRegister}
                    >
                        Registar
                    </button>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;