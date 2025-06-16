import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import UserProfileEdit from '../components/forms/UserProfileEdit';  // Use o caminho correto
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowLeft } from '@fortawesome/free-solid-svg-icons';

// Componente que representa a página de edição do perfil do utilizador
const UserProfilePage = () => {
    const history = useHistory();
    const [successMessage, setSuccessMessage] = useState('');
    
    // Dados fictícios do utilizador para demonstração
    const mockUserData = {
        name: 'admin',
        email: 'admin@agrosmart.pt',
    };

    // Função para processar a gravação dos dados do perfil
    const handleSave = async (name, email, password) => {
        // Simula uma chamada à API com um tempo de espera
        return new Promise((resolve) => {
            setTimeout(() => {
                console.log('Saved user data:', { name, email, password: password ? '********' : '[unchanged]' });
                setSuccessMessage('Dados atualizados com sucesso!');
                resolve();
            }, 1000);
        });
    };

    // Função para voltar à página inicial da aplicação
    const handleBackToHome = () => {
        history.push('/agrosmart');
    };

    // Renderiza a página de perfil do utilizador
    return (
        <div className="profile-container">
            <h2 className="section-title">Editar Perfil</h2>
            
            {successMessage && (
                <div className="success-message">
                    {successMessage}
                </div>
            )}
            
            <div className="profile-form-container">
                <UserProfileEdit onSave={handleSave} userData={mockUserData} />
            </div>
            
            <div className="back-button-container">
                <button 
                    type="button" 
                    className="back-button"
                    onClick={handleBackToHome}
                >
                    <i className="fas fa-arrow-left back-icon"></i>
                    Voltar à Página Inicial
                </button>
            </div>
        </div>
    );
};

export default UserProfilePage;