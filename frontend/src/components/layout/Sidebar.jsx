import React from 'react';
import { useHistory } from 'react-router-dom';
import { logout } from '../../services/auth';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHome, faCloud, faBell, faLeaf, faHistory, faSignOutAlt, faUserEdit } from '@fortawesome/free-solid-svg-icons';
import PropTypes from 'prop-types';

// Componente que representa a barra lateral de navegação da aplicação
const Sidebar = ({ isOpen, toggleSidebar }) => {
    // Hook para gerir a navegação entre páginas
    const history = useHistory();

    // Função para processar o logout do utilizador
    const handleLogout = () => {
        logout();
        history.push('/');
    };

    // Função para navegar para diferentes páginas da aplicação
    const handleNavigation = (path) => {
        history.push(path);
        toggleSidebar();
    };

    // Renderiza a barra lateral com todas as opções de navegação
    return (
        <aside className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
            <div className="sidebar-header">
                <button className="close-button" onClick={toggleSidebar}>✕</button>
            </div>
            <nav>
                <ul>
                    <li onClick={() => handleNavigation('/agrosmart')}>
                        <FontAwesomeIcon icon={faHome} className="sidebar-icon" />
                        Início
                    </li>
                    <li onClick={() => handleNavigation('/agrosmart/profile')}>
                        <FontAwesomeIcon icon={faUserEdit} className="sidebar-icon" />
                        Perfil
                    </li>
                    <li onClick={() => handleNavigation('/agrosmart/weather')}>
                        <FontAwesomeIcon icon={faCloud} className="sidebar-icon" />
                        Meteorologia
                    </li>
                    <li onClick={() => handleNavigation('/agrosmart/alerts')}>
                        <FontAwesomeIcon icon={faBell} className="sidebar-icon" />
                        Alertas
                    </li>
                    <li onClick={() => handleNavigation('/agrosmart/recommendations')}>
                        <FontAwesomeIcon icon={faLeaf} className="sidebar-icon" />
                        Recomendação
                    </li>
                    <li onClick={() => handleNavigation('/agrosmart/history')}>
                        <FontAwesomeIcon icon={faHistory} className="sidebar-icon" />
                        Histórico
                    </li>
                    <li onClick={handleLogout} className="logout-item">
                        <FontAwesomeIcon icon={faSignOutAlt} className="sidebar-icon" />
                        Sair
                    </li>
                </ul>
            </nav>
        </aside>
    );
};

// Validação das propriedades do componente
Sidebar.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    toggleSidebar: PropTypes.func.isRequired 
};

export default Sidebar;