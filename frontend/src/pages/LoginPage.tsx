import React from 'react';
import { useHistory } from 'react-router-dom';
import LoginForm from '../components/LoginForm';
import { login } from '../services/auth';

const LoginPage: React.FC = () => {
    const history = useHistory();

    const handleLogin = async (username: string, password: string) => {
        try {
            await login(username, password);
            history.push('/dashboard'); // Redirect to the dashboard after successful login
        } catch (error) {
            console.error("Login failed:", error);
            throw error; // Throw the error to be handled by the form
        }
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
            </div>
        </div>
    );
};

export default LoginPage;