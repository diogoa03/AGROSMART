import React from 'react';
import { useHistory } from 'react-router-dom';
import RegisterForm from '../components/forms/RegisterForm';  // Use o caminho correto

// Componente que representa a página de registo de novos utilizadores
const RegisterPage = () => {
    
    // Hook para gerir a navegação entre páginas
    const history = useHistory();

    // Função para processar o registo de um novo utilizador
    const handleRegister = async (username, email, password) => {
        try {
            console.log('Registration successful:', { username, email });
            history.push('/');
        } catch (error) {
            console.error("Registration failed:", error);
            throw error;
        }
    };

    // Função para redirecionar o utilizador de volta à página de login
    const handleBackToLogin = () => {
        history.push('/');
    };

    // Renderiza a página de registo completa
    return (
        <div className="login-container">
            <div className="login-card">
                <div className="login-header">
                    <h2>Registar</h2>
                    <div className="separator">|</div>
                    <img src="/agrosmart-logo.svg" alt="AgroSmart" height="80" />
                </div>
                
                <RegisterForm onRegister={handleRegister} />
                
                <div className="back-to-login">
                    <p>Já tem uma conta?</p>
                    <button 
                        type="button" 
                        className="back-to-login-btn"
                        onClick={handleBackToLogin}
                    >
                        Voltar ao Login
                    </button>
                </div>
            </div>
        </div>
    );
};

export default RegisterPage;