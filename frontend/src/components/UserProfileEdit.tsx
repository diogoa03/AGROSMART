import React, { useState } from 'react';

interface UserProfileEditProps {
    onSave: (name: string, email: string, password: string) => Promise<void>;
    userData: {
        name: string;
        email: string;
    };
}

const UserProfileEdit: React.FC<UserProfileEditProps> = ({ onSave, userData }) => {
    const [name, setName] = useState(userData.name || '');
    const [email, setEmail] = useState(userData.email || '');
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

        if (!name || !email) {
            setError('Nome e Email são obrigatórios');
            return;
        }

        if (!validateEmail(email)) {
            setError('Por favor, insira um email válido');
            return;
        }

        // Se o utilizador inserir uma password, verifica se tem pelo menos 6 caracteres e se coincide
        if (password) {
            if (password.length < 6) {
                setError('A password deve ter pelo menos 6 caracteres');
                return;
            }

            if (password !== confirmPassword) {
                setError('As passwords não coincidem');
                return;
            }
        }

        setIsSubmitting(true);

        try {
            await onSave(name, email, password);
        } catch (err) {
            setError('Erro ao guardar alterações. Tente novamente.');
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <form className="login-form" onSubmit={handleSubmit}>
            <div className="form-group">
                <label htmlFor="name">Nome</label>
                <input
                    id="name"
                    type="text"
                    className="form-control"
                    placeholder="Nome completo"
                    value={name}
                    onChange={e => setName(e.target.value)}
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
                <label htmlFor="password">Password (deixar em branco para manter atual)</label>
                <input
                    id="password"
                    type="password"
                    className="form-control"
                    placeholder="Nova password"
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
                {isSubmitting ? 'A guardar...' : 'Guardar'}
            </button>
        </form>
    );
};

export default UserProfileEdit;