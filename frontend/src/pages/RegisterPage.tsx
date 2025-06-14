import React from 'react';
import { useHistory } from 'react-router-dom';
import RegisterForm from '../components/RegisterForm';
import '../styles/login.css';

const RegisterPage: React.FC = () => {
    const history = useHistory();

    const handleRegister = async (username: string, email: string, password: string) => {
        try {
            // Simular registro bem-sucedido
            console.log('Registration successful:', { username, email });
            // Redirecionar para a página de login após registro
            history.push('/');
        } catch (error) {
            console.error("Registration failed:", error);
            throw error;
        }
    };

    const handleBackToLogin = () => {
        history.push('/');
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <div className="login-header">
                    <h2>Registrar</h2>
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