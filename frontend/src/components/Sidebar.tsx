import React from 'react';
import { useHistory } from 'react-router-dom';
import { logout } from '../services/auth';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHome, faCloud, faBell, faLeaf, faHistory, faSignOutAlt } from '@fortawesome/free-solid-svg-icons';

interface SidebarProps {
    isOpen: boolean;
    toggleSidebar: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, toggleSidebar }) => {
    const history = useHistory();

    const handleLogout = () => {
        logout();
        history.push('/');
    };

    const handleNavigation = (path: string) => {
        history.push(path);
        toggleSidebar();
    };

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
                        Recomendacao
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

export default Sidebar;