import React, { useState } from 'react';
import PropTypes from 'prop-types';

// Componente que permite ao utilizador editar os seus dados de perfil
const UserProfileEdit = ({ onSave, userData }) => {
    // Estados para gerir os dados do formulário
    const [name, setName] = useState(userData.name || '');
    const [email, setEmail] = useState(userData.email || '');
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

        // Verifica se os campos obrigatórios estão preenchidos
        if (!name || !email) {
            setError('Nome e Email são obrigatórios');
            return;
        }

        // Valida o formato do email
        if (!validateEmail(email)) {
            setError('Por favor, insira um email válido');
            return;
        }

        // Só verifica a password se o utilizador estiver a tentar alterá-la
        if (password) {
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
        }

        // Atualiza o estado para mostrar que está a processar
        setIsSubmitting(true);

        try {
            // Tenta guardar as alterações do perfil do utilizador
            await onSave(name, email, password);
        } catch (err) {
            // Em caso de erro, mostra uma mensagem ao utilizador
            setError('Erro ao guardar alterações. Tente novamente.');
        } finally {
            // Independentemente do resultado, atualiza o estado de submissão
            setIsSubmitting(false);
        }
    };

    // Renderiza o formulário de edição de perfil
    return (
        <form className="login-form" onSubmit={handleSubmit}>
            <div className="form-group">
                <label htmlFor="name">Nome do utilizador</label>
                <input
                    id="name"
                    type="text"
                    className="form-control"
                    placeholder="Novo nome do utilizador"
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
                    placeholder="Novo email"
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
                className="submit-button" 
                disabled={isSubmitting}
            >
                {isSubmitting ? 'A guardar...' : 'Guardar Alterações'}
            </button>
        </form>
    );
};

// Validação das propriedades do componente
UserProfileEdit.propTypes = {
    onSave: PropTypes.func.isRequired,
    userData: PropTypes.shape({
        name: PropTypes.string,
        email: PropTypes.string
    }).isRequired
};

export default UserProfileEdit;

