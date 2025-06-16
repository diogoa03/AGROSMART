import React, { useState } from 'react';
import PropTypes from 'prop-types';

// Componente que representa o formulário de login da aplicação
const LoginForm = ({ onLogin }) => {
    // Estados para gerir os dados do formulário
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState('');

    // Função que trata a submissão do formulário
    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // Verifica se todos os campos obrigatórios estão preenchidos
        if (!username || !password) {
            setError('Por favor, preencha todos os campos');
            return;
        }
        
        // Atualiza o estado para mostrar que está a processar
        setIsSubmitting(true);
        setError(''); 
        
        try {
            // Tenta fazer o login com as credenciais fornecidas
            await onLogin(username, password);
        } catch (err) {
            // Em caso de erro, mostra uma mensagem ao utilizador
            setError('Credenciais inválidas. Tente novamente.');
        } finally {
            // Independentemente do resultado, atualiza o estado de submissão
            setIsSubmitting(false);
        }
    };

    // Renderiza o formulário de login
    return (
        <form className="login-form" onSubmit={handleSubmit}>
            <div className="form-group">
                <label htmlFor="username">Nome do Utilizador</label>
                <input
                    id="username"
                    type="text"
                    className="form-control"
                    placeholder="Nome do utilizador"
                    value={username}
                    onChange={e => setUsername(e.target.value)} 
                    disabled={isSubmitting} 
                />
            </div>
            
            <div className="form-group">
                <label htmlFor="password">Password</label>
                <input
                    id="password"
                    type="password" 
                    className="form-control"
                    placeholder="Password"
                    value={password}
                    onChange={e => setPassword(e.target.value)} 
                    disabled={isSubmitting} 
                />
            </div>
            
            {error && <div className="error-message">{error}</div>}
            
            <button 
                type="submit" 
                className="login-btn"
                disabled={isSubmitting}
            >
                {isSubmitting ? 'Logging in...' : 'Login'}
            </button>
        </form>
    );
};

// Validação das propriedades do componente
LoginForm.propTypes = {
    onLogin: PropTypes.func.isRequired
};

export default LoginForm;