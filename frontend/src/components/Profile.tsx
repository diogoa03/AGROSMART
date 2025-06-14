import React, { useState, useEffect } from 'react';

interface ProfileData {
  username: string;
  email: string;
  region: string;
  country: string;
  joinDate: string;
  lastLogin: string;
}

const Profile: React.FC = () => {
  const [profileData, setProfileData] = useState<ProfileData | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState<Partial<ProfileData>>({});

  useEffect(() => {
    // Simular dados do perfil - em uma aplicação real, isso viria de uma API
    const getUserData = () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const decoded = atob(token);
          const username = decoded.split(':')[0];
          
          // Dados simulados
          const mockData: ProfileData = {
            username: username,
            email: `${username}@agrosmart.com`,
            region: 'São João da Madeira',
            country: 'Portugal',
            joinDate: '2024-01-15',
            lastLogin: new Date().toISOString().split('T')[0]
          };
          
          setProfileData(mockData);
          setEditData(mockData);
        } catch (error) {
          console.error('Erro ao decodificar token:', error);
        }
      }
    };

    getUserData();
  }, []);

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleSave = () => {
    if (editData && profileData) {
      setProfileData({ ...profileData, ...editData });
      setIsEditing(false);
      // Aqui você faria a chamada para a API para salvar os dados
      console.log('Dados salvos:', editData);
    }
  };

  const handleCancel = () => {
    setEditData(profileData || {});
    setIsEditing(false);
  };

  const handleInputChange = (field: keyof ProfileData, value: string) => {
    setEditData(prev => ({ ...prev, [field]: value }));
  };

  if (!profileData) {
    return (
      <div className="card-container">
        <div className="card-header">Carregando perfil...</div>
      </div>
    );
  }

  return (
    <div className="card-container">
      <div className="card-header">
        <svg className="profile-icon" viewBox="0 0 24 24" style={{ width: '32px', height: '32px', marginRight: '10px' }}>
          <path fill="currentColor" d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
        </svg>
        Perfil do Usuário
      </div>

      <div className="profile-content">
        <div className="profile-avatar-large">
          <svg viewBox="0 0 24 24" style={{ width: '80px', height: '80px', color: '#1f3c2d' }}>
            <path fill="currentColor" d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
          </svg>
        </div>

        <div className="profile-info">
          <div className="profile-field">
            <label>Nome de Usuário:</label>
            {isEditing ? (
              <input
                type="text"
                value={editData.username || ''}
                onChange={(e) => handleInputChange('username', e.target.value)}
                className="form-control"
              />
            ) : (
              <span>{profileData.username}</span>
            )}
          </div>

          <div className="profile-field">
            <label>Email:</label>
            {isEditing ? (
              <input
                type="email"
                value={editData.email || ''}
                onChange={(e) => handleInputChange('email', e.target.value)}
                className="form-control"
              />
            ) : (
              <span>{profileData.email}</span>
            )}
          </div>

          <div className="profile-field">
            <label>Região:</label>
            {isEditing ? (
              <input
                type="text"
                value={editData.region || ''}
                onChange={(e) => handleInputChange('region', e.target.value)}
                className="form-control"
              />
            ) : (
              <span>{profileData.region}</span>
            )}
          </div>

          <div className="profile-field">
            <label>País:</label>
            {isEditing ? (
              <input
                type="text"
                value={editData.country || ''}
                onChange={(e) => handleInputChange('country', e.target.value)}
                className="form-control"
              />
            ) : (
              <span>{profileData.country}</span>
            )}
          </div>

          <div className="profile-field">
            <label>Data de Cadastro:</label>
            <span>{new Date(profileData.joinDate).toLocaleDateString('pt-BR')}</span>
          </div>

          <div className="profile-field">
            <label>Último Login:</label>
            <span>{new Date(profileData.lastLogin).toLocaleDateString('pt-BR')}</span>
          </div>
        </div>

        <div className="profile-actions">
          {isEditing ? (
            <div className="edit-actions">
              <button className="save-btn" onClick={handleSave}>
                <svg viewBox="0 0 24 24" style={{ width: '16px', height: '16px', marginRight: '5px' }}>
                  <path fill="currentColor" d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                </svg>
                Salvar
              </button>
              <button className="cancel-btn" onClick={handleCancel}>
                <svg viewBox="0 0 24 24" style={{ width: '16px', height: '16px', marginRight: '5px' }}>
                  <path fill="currentColor" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                </svg>
                Cancelar
              </button>
            </div>
          ) : (
            <button className="edit-btn" onClick={handleEdit}>
              <svg viewBox="0 0 24 24" style={{ width: '16px', height: '16px', marginRight: '5px' }}>
                <path fill="currentColor" d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
              </svg>
              Editar Perfil
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default Profile;