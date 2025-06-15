import React, { useState } from 'react';
import PropTypes from 'prop-types';

// Componente que representa o formulário de registo para novos utilizadores
const RegisterForm = ({ onRegister }) => {

    // Estados para gerir os dados do formulário
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState(''); 
    const [confirmPassword, setConfirmPassword] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState('');

    // Função para validar o formato do email usando expressão regular
    const validateEmail = (email) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    };

    // Função que trata a submissão do formulário
    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        // Verifica se todos os campos obrigatórios estão preenchidos
        if (!username || !email || !password || !confirmPassword) {
            setError('Todos os campos são obrigatórios');
            return;
        }

        // Valida o formato do email
        if (!validateEmail(email)) {
            setError('Por favor, insira um email válido');
            return;
        }

        // Verifica se a password tem pelo menos 6 caracteres
        if (password.length < 6) {
            setError('A password deve ter pelo menos 6 caracteres');
            return;
        }

        // Verifica se as passwords coincidem
        if (password !== confirmPassword) {
            setError('As passwords não coincidem');
            return;
        }

        // Atualiza o estado para mostrar que está a processar
        setIsSubmitting(true);

        try {

            // Tenta registar o utilizador com os dados fornecidos
            await onRegister(username, email, password);
        } catch (err) {

            // Em caso de erro, mostra uma mensagem ao utilizador
            setError('Erro ao criar conta. Tente novamente.');
        } finally {

            // Independentemente do resultado, atualiza o estado de submissão
            setIsSubmitting(false);
        }
    };

    // Renderiza o formulário de registo
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
                <label htmlFor="email">Email</label>
                <input
                    id="email"
                    type="email"
                    className="form-control"
                    placeholder="Email"
                    value={email}
                    onChange={e => setEmail(e.target.value)} 
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
            
            <div className="form-group">
                <label htmlFor="confirmPassword">Confirmar Password</label>
                <input
                    id="confirmPassword"
                    type="password" 
                    className="form-control"
                    placeholder="Confirmar password"
                    value={confirmPassword}
                    onChange={e => setConfirmPassword(e.target.value)}
                    disabled={isSubmitting}
                />
            </div>
            
            {error && <div className="error-message">{error}</div>}
            
            <button 
                type="submit" 
                className="login-btn"
                disabled={isSubmitting}
            >
                {isSubmitting ? 'Registrando...' : 'Registar'}
            </button>
        </form>
    );
};

// Validação das propriedades do componente
RegisterForm.propTypes = {
    onRegister: PropTypes.func.isRequired
};

export default RegisterForm;