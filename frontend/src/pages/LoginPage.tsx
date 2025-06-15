import React from 'react';
import { useHistory } from 'react-router-dom';
import LoginForm from '../components/LoginForm';
import { login } from '../services/auth';
import '../styles/login.css';

const LoginPage: React.FC = () => {
    const history = useHistory();

    const handleLogin = async (username: string, password: string) => {
        try {
            await login(username, password);
            history.push('/agrosmart'); 
        } catch (error) {
            console.error("Login failed:", error);
            throw error; 
        }
    };

    const handleGoToRegister = () => {
        history.push('/register');
    };

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
                        Registrar
                    </button>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;