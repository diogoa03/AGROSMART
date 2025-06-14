import React, { useState } from 'react';

interface RegisterFormProps {
    onRegister: (username: string, email: string, password: string) => Promise<void>;
}

const RegisterForm: React.FC<RegisterFormProps> = ({ onRegister }) => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState('');

    const validateEmail = (email: string) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        // Validações
        if (!username || !email || !password || !confirmPassword) {
            setError('Todos os campos são obrigatórios');
            return;
        }

        if (!validateEmail(email)) {
            setError('Por favor, insira um email válido');
            return;
        }

        if (password.length < 6) {
            setError('A password deve ter pelo menos 6 caracteres');
            return;
        }

        if (password !== confirmPassword) {
            setError('As passwords não coincidem');
            return;
        }

        setIsSubmitting(true);

        try {
            await onRegister(username, email, password);
        } catch (err) {
            setError('Erro ao criar conta. Tente novamente.');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <form className="login-form" onSubmit={handleSubmit}>
            <div className="form-group">
                <label htmlFor="username">Nome de Utilizador</label>
                <input
                    id="username"
                    type="text"
                    className="form-control"
                    placeholder="Nome de utilizador"
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
                {isSubmitting ? 'Registrando...' : 'Registrar'}
            </button>
        </form>
    );
};

export default RegisterForm;