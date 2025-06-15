import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import UserProfileEdit from '../components/UserProfileEdit';
import '../styles/login.css';

const UserProfilePage: React.FC = () => {
    const history = useHistory();
    const [successMessage, setSuccessMessage] = useState('');
    
    // Dados fictícios do utilizador
    const mockUserData = {
        name: 'admin',
        email: 'admin@agrosmart.pt',
    };

    const handleSave = async (name: string, email: string, password: string) => {
        // Simula uma chamada de API para salvar os dados
        return new Promise<void>((resolve) => {
            setTimeout(() => {
                console.log('Saved user data:', { name, email, password: password ? '********' : '[unchanged]' });
                setSuccessMessage('Dados atualizados com sucesso!');
                resolve();
            }, 1000);
        });
    };

    const handleBackToHome = () => {
        history.push('/agrosmart');
    };

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